"""Verify the local environment is ready for P-DRL experiments.

Checks:
  1. Python version (3.11+)
  2. Poetry environment is active
  3. All required environment variables present
  4. All required directories exist
  5. F-I-R-A-C-O schema imports and a minimal graph round-trips through
     model_validate and model_dump_json without loss
  6. A test API call succeeds for each of the three model providers

Usage:
    poetry run python scripts/check_setup.py

Exit code 0 on full success; 1 otherwise.
"""
from __future__ import annotations

import json
import os
import shutil
import subprocess
import sys
from pathlib import Path

from dotenv import load_dotenv
from rich.console import Console
from rich.table import Table

console = Console()


REQUIRED_ENV_VARS = [
    "ANTHROPIC_API_KEY",
    "OPENAI_API_KEY",
    "OPENROUTER_API_KEY",
    "TEACHER_MODEL",
    "AGENT_MODEL",
    "SMALL_MODEL",
]

REQUIRED_DIRS = [
    "src/lex_drl",
    "configs/prompts",
    "data/cases",
    "data/statutes",
    "data/outputs/graphs",
    "data/outputs/analysis",
    "scripts",
    "tests",
]


def check_python_version() -> tuple[bool, str]:
    v = sys.version_info
    if v >= (3, 11):
        return True, f"Python {v.major}.{v.minor}.{v.micro}"
    return False, f"Python {v.major}.{v.minor} — need 3.11+"


def check_poetry_active() -> tuple[bool, str]:
    venv = os.environ.get("VIRTUAL_ENV", "")
    if "pypoetry" in venv:
        return True, f"Poetry venv active: {Path(venv).name}"
    if venv:
        return True, f"Some venv active (not Poetry): {Path(venv).name}"
    if shutil.which("poetry"):
        try:
            r = subprocess.run(
                ["poetry", "env", "info", "--path"],
                capture_output=True, text=True, timeout=10,
            )
            if r.returncode == 0 and r.stdout.strip():
                return True, f"Poetry env path: {r.stdout.strip()}"
        except (subprocess.TimeoutExpired, FileNotFoundError):
            pass
    return False, "No venv detected — run via 'poetry run'"


def check_env_vars() -> tuple[bool, str]:
    load_dotenv()
    missing = [v for v in REQUIRED_ENV_VARS if not os.environ.get(v)]
    if missing:
        return False, f"Missing: {', '.join(missing)}"
    return True, f"All {len(REQUIRED_ENV_VARS)} env vars present"


def check_directories() -> tuple[bool, str]:
    missing = [d for d in REQUIRED_DIRS if not Path(d).is_dir()]
    if missing:
        return False, f"Missing: {', '.join(missing)}"
    return True, f"All {len(REQUIRED_DIRS)} dirs present"


def check_schema_roundtrip() -> tuple[bool, str]:
    try:
        sys.path.insert(0, str(Path("src").resolve()))
        from lex_drl.schema import LegalReasoningGraph

        minimal = {
            "case_id": "TEST",
            "source": "reference",
            "model_name": "test-model",
            "agent_id": None,
            "facts": [
                {"fid": "F1", "label": "test fact", "polarity": "present"}
            ],
            "issues": [
                {"iid": "I1", "label": "test issue", "status": "dispositive"}
            ],
            "rules": [
                {
                    "rid": "R1",
                    "citation": "Test §1",
                    "label": "test rule",
                    "authority": "binding",
                    "jurisdiction": "Test",
                }
            ],
            "applications": [],
            "conclusions": [],
            "obligations": [],
            "edges": [
                {"eid": "E1", "src": "F1", "dst": "I1",
                 "type": "triggers", "justification": "test"}
            ],
        }

        graph = LegalReasoningGraph.model_validate(minimal)
        roundtripped = json.loads(graph.model_dump_json())
        regraph = LegalReasoningGraph.model_validate(roundtripped)

        if (
            regraph.case_id == "TEST"
            and len(regraph.facts) == 1
            and regraph.facts[0].fid == "F1"
            and regraph.node_count() == 3
            and len(regraph.edges) == 1
        ):
            return True, "Schema round-trip OK (1F, 1I, 1R, 1 edge)"
        return False, "Round-trip data mismatch"
    except Exception as e:
        return False, f"Round-trip failed: {type(e).__name__}: {e}"


def check_teacher_call() -> tuple[bool, str]:
    try:
        from lex_drl.clients import TeacherClient
        c = TeacherClient()
        r = c.generate(
            system="Answer in exactly 3 words.",
            user="Say hello briefly.",
            max_tokens=50,
        )
        if r.text and len(r.text) < 300:
            return True, f"{c.model}: {r.text.strip()!r}"
        return False, f"Unexpected response: {r.text[:80]}"
    except Exception as e:
        return False, f"{type(e).__name__}: {e}"


def check_agent_call() -> tuple[bool, str]:
    try:
        from lex_drl.clients import AgentClient
        c = AgentClient()
        r = c.generate(
            system="Answer in exactly 3 words.",
            user="Say hello briefly.",
            max_tokens=50,
        )
        if r.text:
            return True, f"{c.model}: {r.text.strip()!r}"
        return False, "Empty response"
    except Exception as e:
        return False, f"{type(e).__name__}: {e}"


def check_small_model_call() -> tuple[bool, str]:
    try:
        from lex_drl.clients import SmallModelClient
        c = SmallModelClient()
        r = c.generate(
            system="Answer in exactly 3 words.",
            user="Say hello briefly.",
            max_tokens=50,
        )
        if r.text:
            return True, f"{c.model}: {r.text.strip()!r}"
        return False, "Empty response"
    except Exception as e:
        return False, f"{type(e).__name__}: {e}"


def main() -> None:
    console.print("\n[bold cyan]P-DRL Environment Check[/bold cyan]\n")

    checks = [
        ("Python version", check_python_version),
        ("Poetry venv", check_poetry_active),
        ("Environment variables", check_env_vars),
        ("Required directories", check_directories),
        ("Schema round-trip", check_schema_roundtrip),
        ("Teacher API (Claude Opus)", check_teacher_call),
        ("Agent API (GPT-5)", check_agent_call),
        ("Small model API (OpenRouter)", check_small_model_call),
    ]

    table = Table(show_header=True, header_style="bold")
    table.add_column("Check", style="bold")
    table.add_column("Status", justify="center")
    table.add_column("Detail")

    all_ok = True
    for name, fn in checks:
        try:
            ok, detail = fn()
        except Exception as e:
            ok, detail = False, f"Unhandled {type(e).__name__}: {e}"
        marker = "[green]✓[/green]" if ok else "[red]✗[/red]"
        table.add_row(name, marker, detail)
        all_ok = all_ok and ok

    console.print(table)

    if all_ok:
        console.print(
            "\n[bold green]All checks passed.[/bold green] "
            "You can run extractions.\n"
        )
        sys.exit(0)
    else:
        console.print(
            "\n[bold red]Some checks failed.[/bold red] "
            "Fix the failures above before running experiments.\n"
        )
        sys.exit(1)


if __name__ == "__main__":
    main()
