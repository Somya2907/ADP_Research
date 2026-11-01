"""Stop a small model that has started repeating itself.

With greedy decoding, Llama-3.2-3B sometimes falls into a loop when the prompt
is long: it writes the same JSON node again and again with only the id
changing ("R10 … §20-873", "R13 … §20-873", …) until it hits the token limit,
and the graph never gets its applications or conclusions.

A loop is detected when one JSON node line, with its id removed, has appeared
``repeats`` times, or when one node type passes ``MAX_PER_TYPE`` lines (the
other failure: inventing §20-923, §20-924, … one after another). The teacher
never writes more than 27 nodes of one type; edges are not capped. The answer is cut just before the
offending line. Because decoding is
greedy, stopping generation there (``LoopGuard``) and cutting a finished answer
there (``truncate_loop``) give the same text, so cached answers can be guarded
after the fact without regenerating them.
"""
from __future__ import annotations

import re
from typing import Optional

_ID_FIELD = re.compile(r'"(fid|iid|rid|aid|cid|oid|eid)"\s*:\s*"[A-Z]\d+"')
MIN_LINE = 40          # shorter lines ("],", "{") repeat legitimately
REPEATS = 3
MAX_PER_TYPE = 30


def _norm(line: str) -> str:
    return _ID_FIELD.sub('"id"', line.strip()).rstrip(",")


def loop_start(text: str, repeats: int = REPEATS,
               max_per_type: int = MAX_PER_TYPE) -> Optional[int]:
    """Character offset of the line where a loop is detected, or None.

    Only complete JSON node lines (ones carrying an id field) are counted, so
    repeated prose or brackets never trigger it.
    """
    counts: dict[str, int] = {}
    per_type: dict[str, int] = {}
    pos = 0
    for line in text.splitlines(keepends=True):
        m = _ID_FIELD.search(line)
        if m and line.endswith("\n"):
            kind = m.group(1)
            per_type[kind] = per_type.get(kind, 0) + 1
            if kind != "eid" and per_type[kind] > max_per_type:   # edges are legitimately many
                return pos
            key = _norm(line)
            if len(key) >= MIN_LINE:
                counts[key] = counts.get(key, 0) + 1
                if counts[key] >= repeats:
                    return pos
        pos += len(line)
    return None


def truncate_loop(text: str, repeats: int = REPEATS) -> tuple[str, bool]:
    """(text cut before the looping line, whether a loop was found)."""
    cut = loop_start(text, repeats)
    return (text, False) if cut is None else (text[:cut], True)


class LoopGuard:
    """transformers StoppingCriteria: stop once ``loop_start`` fires.

    Only checks when the newest token contains a newline, so the cost is one
    decode per generated line.
    """

    def __init__(self, tokenizer, prompt_len: int, repeats: int = REPEATS, preamble: str = ""):
        # ``preamble``: answer text already written before this generation (when
        # continuing a repaired answer), so a loop spanning both is still caught.
        self.tok, self.prompt_len, self.repeats = tokenizer, prompt_len, repeats
        self.preamble = preamble
        self.fired = False

    def __call__(self, input_ids, scores, **kwargs) -> bool:
        last = self.tok.decode(input_ids[0, -1:], skip_special_tokens=True)
        if "\n" not in last:
            return False
        text = self.tok.decode(input_ids[0, self.prompt_len:], skip_special_tokens=True,
                               clean_up_tokenization_spaces=False)
        self.fired = loop_start(self.preamble + text, self.repeats) is not None
        return self.fired


__all__ = ["loop_start", "truncate_loop", "LoopGuard", "REPEATS", "MAX_PER_TYPE"]
