"""SDK clients for all three model tiers.

Teacher:  Claude Opus 4.6 (Anthropic) — streaming, produces G_ref
Student1: GPT-5 (OpenAI) — frontier student, no statutory context
Student2: Llama-3.2-3B-Instruct (OpenRouter) — small student <7B, no statutory context

Fixes (v3):
  - Teacher uses streaming API to avoid Anthropic 10-min non-streaming limit
    when max_tokens=24576 on hard cases (H1 in particular).
"""
from __future__ import annotations

import os
import time
from dataclasses import dataclass

from anthropic import Anthropic
from openai import OpenAI

from .cache import cached_call


@dataclass
class LLMResponse:
    text: str
    model: str
    input_tokens: int
    output_tokens: int

    @property
    def total_tokens(self) -> int:
        return self.input_tokens + self.output_tokens


# ──────────────────────────────────────────────
# Teacher: Claude Opus 4.6 — streaming, 24K tokens
# ──────────────────────────────────────────────

class TeacherClient:
    """Claude Opus 4.6 (teacher / reference model) via Anthropic streaming API."""

    def __init__(self, model: str | None = None):
        self.client = Anthropic()
        self.model = model or os.environ.get("TEACHER_MODEL", "claude-opus-4-6")

    @cached_call(namespace="teacher")
    def generate(
        self,
        system: str,
        user: str,
        max_tokens: int = 24576,
        temperature: float = 0.0,
    ) -> LLMResponse:
        # Streaming is required for long requests (>10 min wall clock).
        # We collect all chunks and return the assembled response,
        # so the calling code doesn't need to know about streaming.
        text_chunks: list[str] = []
        input_tokens = 0
        output_tokens = 0

        with self.client.messages.stream(
            model=self.model,
            max_tokens=max_tokens,
            temperature=temperature,
            system=system,
            messages=[{"role": "user", "content": user}],
        ) as stream:
            for event in stream:
                # Collect text deltas as they arrive
                if hasattr(event, "type"):
                    if event.type == "content_block_delta" and hasattr(event, "delta"):
                        if hasattr(event.delta, "text"):
                            text_chunks.append(event.delta.text)

            # Final message contains usage info
            final = stream.get_final_message()
            input_tokens = final.usage.input_tokens
            output_tokens = final.usage.output_tokens

        return LLMResponse(
            text="".join(text_chunks),
            model=self.model,
            input_tokens=input_tokens,
            output_tokens=output_tokens,
        )


# ──────────────────────────────────────────────
# Student 1: GPT-5 (frontier)
# ──────────────────────────────────────────────

class AgentClient:
    """GPT-5 (Student 1 — frontier) via OpenAI SDK."""

    def __init__(self, model: str | None = None):
        self.client = OpenAI()
        self.model = model or os.environ.get("AGENT_MODEL", "gpt-5")

    @cached_call(namespace="agent_gpt5")
    def generate(
        self,
        system: str,
        user: str,
        max_tokens: int = 16384,
        temperature: float = 0.0,
        run_tag: str = "",  # salts the cache key (variance repeats); ignored by the API
    ) -> LLMResponse:
        resp = self.client.chat.completions.create(
            model=self.model,
            max_completion_tokens=max_tokens,
            messages=[
                {"role": "system", "content": system},
                {"role": "user", "content": user},
            ],
        )
        usage = resp.usage
        return LLMResponse(
            text=resp.choices[0].message.content or "",
            model=self.model,
            input_tokens=usage.prompt_tokens if usage else 0,
            output_tokens=usage.completion_tokens if usage else 0,
        )


# ──────────────────────────────────────────────
# Student 2: Llama-3.2-3B-Instruct via OpenRouter
# ──────────────────────────────────────────────

class SmallModelClient:
    """Llama-3.2-3B-Instruct (Student 2 — small, <7B parameters) via OpenRouter."""

    def __init__(self, model: str | None = None):
        api_key = os.environ.get("OPENROUTER_API_KEY")
        if not api_key:
            raise ValueError(
                "OPENROUTER_API_KEY not found in environment. "
                "Add it to .env: OPENROUTER_API_KEY=sk-or-..."
            )
        self.client = OpenAI(
            base_url="https://openrouter.ai/api/v1",
            api_key=api_key,
        )
        self.model = model or os.environ.get("SMALL_MODEL", "meta-llama/llama-3.2-3b-instruct")

    @cached_call(namespace="agent_llama3_2b")
    def generate(
        self,
        system: str,
        user: str,
        max_tokens: int = 8192,
        temperature: float = 0.0,
        max_retries: int = 5,
        run_tag: str = "",  # salts the cache key (variance repeats); ignored by the API
    ) -> LLMResponse:
        # The working free provider (Venice) is heavily 429-throttled; retry with
        # backoff to push through. (The paid route for this model is Cloudflare-only,
        # which returns empty tool_calls — unusable — so :free is the real path.)
        from openai import RateLimitError

        last_err: Exception | None = None
        for attempt in range(max_retries):
            try:
                resp = self.client.chat.completions.create(
                    model=self.model,
                    max_tokens=max_tokens,
                    temperature=temperature,
                    messages=[
                        {"role": "system", "content": system},
                        {"role": "user", "content": user},
                    ],
                    extra_headers={
                        "HTTP-Referer": "https://github.com/cmu-heinz/l-drl-us-ai-law",
                        "X-Title": "L-DRL Policy Reasoning Sprint",
                    },
                )
                usage = resp.usage
                return LLMResponse(
                    text=resp.choices[0].message.content or "",
                    model=self.model,
                    input_tokens=usage.prompt_tokens if usage else 0,
                    output_tokens=usage.completion_tokens if usage else 0,
                )
            except RateLimitError as e:
                last_err = e
                if attempt < max_retries - 1:
                    time.sleep(min(15 * (attempt + 1), 60))  # 15,30,45,60s
        raise last_err  # exhausted retries


# ──────────────────────────────────────────────
# Student 2 (local): Llama-3.2-3B-Instruct via HF transformers (MPS/CPU)
# ──────────────────────────────────────────────

_LOCAL_MODEL = None  # (tokenizer, model, device) singleton — loaded once


def _add_time_cap(gen_kwargs: dict) -> None:
    """Stop one generation after LEX_DRL_MAX_GEN_SECONDS (unset = no cap).

    On this 16 GB Mac a few long prompts make the model's memory balloon into
    swap and a single answer can take hours. A cap keeps a long run moving; an
    answer stopped by it is written up to that point (and is cached as such).
    """
    secs = os.environ.get("LEX_DRL_MAX_GEN_SECONDS")
    if not secs:
        return
    from transformers import MaxTimeCriteria, StoppingCriteriaList

    crit = gen_kwargs.get("stopping_criteria") or StoppingCriteriaList()
    crit.append(MaxTimeCriteria(max_time=float(secs)))
    gen_kwargs["stopping_criteria"] = crit


class LocalSmallModelClient:
    """Llama-3.2-3B-Instruct run locally via HF transformers.

    Used when OpenRouter can't serve the model (its only paid provider returns
    empty tool_calls; the free provider is 429-throttled). Greedy decoding at
    temperature 0 → deterministic, so ``@cached_call`` stays reproducible.
    Needs HF_TOKEN in the environment (the official repo is gated).
    """

    def __init__(self, repo: str | None = None):
        self.model = repo or os.environ.get(
            "SMALL_MODEL_LOCAL_REPO", "meta-llama/Llama-3.2-3B-Instruct"
        )

    def _ensure_loaded(self):
        global _LOCAL_MODEL
        if _LOCAL_MODEL is None:
            import torch
            from transformers import AutoModelForCausalLM, AutoTokenizer

            token = os.environ.get("HF_TOKEN")
            tok = AutoTokenizer.from_pretrained(self.model, token=token)
            mdl = AutoModelForCausalLM.from_pretrained(
                self.model, token=token, dtype=torch.float16
            )
            device = "mps" if torch.backends.mps.is_available() else "cpu"
            mdl.to(device)
            mdl.eval()
            _LOCAL_MODEL = (tok, mdl, device)
        return _LOCAL_MODEL

    @cached_call(namespace="agent_llama3_2b")
    def generate(
        self,
        system: str,
        user: str,
        max_tokens: int = 4096,
        temperature: float = 0.0,
        run_tag: str = "",  # salts the cache key (variance repeats); ignored by generation
    ) -> LLMResponse:
        import torch

        tok, mdl, device = self._ensure_loaded()
        messages = [
            {"role": "system", "content": system},
            {"role": "user", "content": user},
        ]
        enc = tok.apply_chat_template(
            messages, add_generation_prompt=True, return_tensors="pt", return_dict=True,
        )
        enc = {k: v.to(device) for k, v in enc.items()}
        in_len = enc["input_ids"].shape[-1]
        gen_kwargs = {"max_new_tokens": max_tokens, "pad_token_id": tok.eos_token_id}
        if os.environ.get("LEX_DRL_LOOP_GUARD", "") == "1":
            # Stops a runaway answer early. Greedy decoding makes the result the
            # same as cutting the full answer with truncate_loop, so this only
            # saves time and is deliberately not part of the cache key.
            from transformers import StoppingCriteriaList

            from .loopguard import LoopGuard
            gen_kwargs["stopping_criteria"] = StoppingCriteriaList([LoopGuard(tok, in_len)])
        _add_time_cap(gen_kwargs)
        if temperature and temperature > 0:
            gen_kwargs.update(do_sample=True, temperature=temperature)
        else:
            gen_kwargs.update(do_sample=False)  # greedy → deterministic
        with torch.no_grad():
            out = mdl.generate(**enc, **gen_kwargs)
        gen_tokens = out[0][in_len:]
        # clean_up_tokenization_spaces=False: the cleanup is destructive for BPE
        # (strips spaces before punctuation) and can corrupt JSON output.
        text = tok.decode(gen_tokens, skip_special_tokens=True,
                          clean_up_tokenization_spaces=False)
        return LLMResponse(
            text=text, model=self.model,
            input_tokens=int(in_len), output_tokens=int(gen_tokens.shape[-1]),
        )


    @cached_call(namespace="agent_llama3_2b_continue")
    def continue_from(
        self,
        system: str,
        user: str,
        prefix: str = "",
        max_tokens: int = 4096,
    ) -> LLMResponse:
        """Greedy continuation of an answer that already starts with ``prefix``.

        Used to repair an answer that fell into a loop (see lex_drl.repair): the
        prefix is the answer cut before the loop plus JSON scaffolding that
        closes the looping list. The loop guard is always on here.
        """
        import torch
        from transformers import StoppingCriteriaList

        from .loopguard import LoopGuard

        tok, mdl, device = self._ensure_loaded()
        messages = [
            {"role": "system", "content": system},
            {"role": "user", "content": user},
        ]
        enc = tok.apply_chat_template(
            messages, add_generation_prompt=True, return_tensors="pt", return_dict=True,
        )
        pre = tok(prefix, add_special_tokens=False, return_tensors="pt")
        ids = torch.cat([enc["input_ids"], pre["input_ids"]], dim=-1).to(device)
        mask = torch.ones_like(ids)
        in_len = ids.shape[-1]
        budget = max(768, max_tokens - pre["input_ids"].shape[-1])
        kw = {"stopping_criteria": StoppingCriteriaList([LoopGuard(tok, in_len, preamble=prefix)])}
        _add_time_cap(kw)
        with torch.no_grad():
            out = mdl.generate(
                input_ids=ids, attention_mask=mask, max_new_tokens=budget, do_sample=False,
                pad_token_id=tok.eos_token_id, **kw,
            )
        gen_tokens = out[0][in_len:]
        text = tok.decode(gen_tokens, skip_special_tokens=True,
                          clean_up_tokenization_spaces=False)
        return LLMResponse(
            text=text, model=self.model,
            input_tokens=int(in_len), output_tokens=int(gen_tokens.shape[-1]),
        )


# ──────────────────────────────────────────────
# Student 2 (remote GPU): the same model served from a Colab T4
# ──────────────────────────────────────────────

class RemoteSmallModelClient:
    """Llama-3.2-3B-Instruct served by notebooks/colab_t4_server.ipynb.

    The notebook runs the same weights with the same greedy decoding, loop
    guard and time cap as ``LocalSmallModelClient``, on a GPU instead of this
    Mac. Requests go through a public tunnel that cuts off slow responses, so
    a call submits a job and then polls for its result.

    Answers from a different GPU are not bit-identical to local ones, so the
    model name carries the backend (``…@colab-t4``): its cache entries never
    mix with the local ones, and its results are compared only with each other.

    Needs SMALL_MODEL_REMOTE_URL (the tunnel URL the notebook prints) and
    SMALL_MODEL_REMOTE_KEY (the key it prints).
    """

    POLL_SECONDS = 4.0
    MAX_WAIT_SECONDS = 12 * 3600     # includes time waiting for a restarted notebook

    def __init__(self, repo: str | None = None):
        self.url = os.environ.get("SMALL_MODEL_REMOTE_URL", "").rstrip("/")
        self.key = os.environ.get("SMALL_MODEL_REMOTE_KEY", "")
        if not self.url or not self.key:
            raise ValueError("set SMALL_MODEL_REMOTE_URL and SMALL_MODEL_REMOTE_KEY "
                             "(printed by notebooks/colab_t4_server.ipynb)")
        repo = repo or os.environ.get("SMALL_MODEL_LOCAL_REPO", "unsloth/Llama-3.2-3B-Instruct")
        self.model = f"{repo}@{os.environ.get('SMALL_MODEL_REMOTE_TAG', 'colab-t4')}"

    def _reload_endpoint(self) -> bool:
        """Re-read .env; True if the URL or key changed (a restarted notebook)."""
        from dotenv import dotenv_values

        env = dotenv_values(".env")
        url = (env.get("SMALL_MODEL_REMOTE_URL") or "").strip().rstrip("/")
        key = (env.get("SMALL_MODEL_REMOTE_KEY") or "").strip()
        if url and key and (url, key) != (self.url, self.key):
            self.url, self.key = url, key
            print(f"    [remote] new endpoint from .env: {url}", flush=True)
            return True
        return False

    def _call(self, payload: dict) -> LLMResponse:
        """Submit a job and poll for it, surviving a notebook restart.

        If the server stops answering (Colab disconnected), keep waiting and
        re-read .env: once the notebook is restarted and its new URL and key are
        in .env, the job is resubmitted there. A job the server no longer knows
        (404 after a restart) is resubmitted too.
        """
        import httpx

        payload = payload | {
            "loop_guard": os.environ.get("LEX_DRL_LOOP_GUARD", "") == "1" or payload.get("kind") == "continue",
            "max_seconds": float(os.environ.get("LEX_DRL_MAX_GEN_SECONDS", "0") or 0),
        }
        job: str | None = None
        down_since: float | None = None
        warned = False
        deadline = time.time() + self.MAX_WAIT_SECONDS
        while time.time() < deadline:
            headers = {"X-API-Key": self.key}
            try:
                if job is None:
                    r = httpx.post(f"{self.url}/submit", json=payload, headers=headers, timeout=60)
                    r.raise_for_status()
                    job = r.json()["id"]
                else:
                    time.sleep(self.POLL_SECONDS)
                    r = httpx.get(f"{self.url}/result/{job}", headers=headers, timeout=60)
                    if r.status_code == 404:
                        job = None                # server restarted: the job is gone
                        continue
                    r.raise_for_status()
                    res = r.json()
                    if res["status"] == "done":
                        return LLMResponse(text=res["text"], model=self.model,
                                           input_tokens=res["input_tokens"],
                                           output_tokens=res["output_tokens"])
                    if res["status"] == "error":
                        raise RuntimeError(f"remote generation failed: {res.get('error')}")
                down_since, warned = None, False
            except (httpx.HTTPError, KeyError, ValueError):
                down_since = down_since or time.time()
                if self._reload_endpoint():
                    job, down_since, warned = None, None, False
                    continue
                if time.time() - down_since > 120 and not warned:
                    print("    [remote] server unreachable — restart notebooks/colab_t4_server.ipynb "
                          "and put its new URL/KEY in .env; the run will resume", flush=True)
                    warned = True
                time.sleep(15)
        raise TimeoutError(f"remote job not finished within {self.MAX_WAIT_SECONDS}s")

    @cached_call(namespace="agent_llama3_2b")
    def generate(
        self,
        system: str,
        user: str,
        max_tokens: int = 4096,
        temperature: float = 0.0,
        run_tag: str = "",
    ) -> LLMResponse:
        return self._call({"kind": "generate", "system": system, "user": user,
                           "max_tokens": max_tokens})

    @cached_call(namespace="agent_llama3_2b_continue")
    def continue_from(
        self,
        system: str,
        user: str,
        prefix: str = "",
        max_tokens: int = 4096,
    ) -> LLMResponse:
        return self._call({"kind": "continue", "system": system, "user": user,
                           "prefix": prefix, "max_tokens": max_tokens})


# ──────────────────────────────────────────────
# Factory
# ──────────────────────────────────────────────

def get_agent_client(model_key: str):
    if model_key == "gpt5":
        return AgentClient()
    elif model_key == "llama3_2b":
        # SMALL_MODEL_BACKEND=local → run Llama-3.2-3B locally via transformers;
        # =remote → the same model on a Colab GPU (RemoteSmallModelClient);
        # otherwise the OpenRouter-hosted route.
        backend = os.environ.get("SMALL_MODEL_BACKEND", "").lower()
        if backend == "local":
            return LocalSmallModelClient()
        if backend == "remote":
            return RemoteSmallModelClient()
        return SmallModelClient()
    else:
        raise ValueError(
            f"Unknown model_key '{model_key}'. "
            f"Valid options: 'gpt5', 'llama3_2b'"
        )
