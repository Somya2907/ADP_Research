"""Verify both API keys are configured and working."""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "src"))

from dotenv import load_dotenv
load_dotenv()

from rich import print as rprint

def check_anthropic():
    try:
        from anthropic import Anthropic
        client = Anthropic()
        r = client.messages.create(
            model="claude-opus-4-6",
            max_tokens=20,
            messages=[{"role": "user", "content": "say hi"}],
        )
        rprint(f"[green]✓ Anthropic[/green] — {r.content[0].text.strip()}")
        rprint(f"  Model: {r.model}")
    except Exception as e:
        rprint(f"[red]✗ Anthropic FAILED[/red] — {e}")

def check_openai():
    try:
        from openai import OpenAI
        client = OpenAI()
        r = client.chat.completions.create(
            model="gpt-4o",
            max_tokens=20,
            messages=[{"role": "user", "content": "say hi"}],
        )
        rprint(f"[green]✓ OpenAI[/green] — {r.choices[0].message.content.strip()}")
        rprint(f"  Model: {r.model}")
    except Exception as e:
        rprint(f"[red]✗ OpenAI FAILED[/red] — {e}")

def check_openrouter():
    try:
        import os
        from openai import OpenAI
        client = OpenAI(
            base_url="https://openrouter.ai/api/v1",
            api_key=os.environ.get("OPENROUTER_API_KEY", "missing"),
        )
        r = client.chat.completions.create(
            model="openai/gpt-4o-mini",
            max_tokens=20,
            messages=[{"role": "user", "content": "say hi"}],
        )
        rprint(f"[green]✓ OpenRouter[/green] — {r.choices[0].message.content.strip()}")
        rprint(f"  Model: {r.model}")
    except Exception as e:
        rprint(f"[red]✗ OpenRouter FAILED[/red] — {e}")

if __name__ == "__main__":
    rprint("[bold]Checking API keys...[/bold]\n")
    check_anthropic()
    check_openai()
    check_openrouter()
    rprint("\n[bold]Done.[/bold]")