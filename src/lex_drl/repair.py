"""Finish an answer that fell into a loop, instead of only cutting it.

The loop guard (lex_drl.loopguard) cuts a looping answer where the loop
begins. That keeps the answer from running away, but it also ends it: a model
stuck repeating Rule nodes never writes its Applications or Conclusions.

The student writes its JSON sections in a fixed order (facts, issues, rules,
applications, conclusions, obligations, edges), so the answer can be resumed:
close the list it was stuck in, open the next section, and let the model carry
on from there (greedy, loop guard on). Only JSON brackets and a section name
are added — no content — so the model writes everything that follows itself.
At most ``MAX_REPAIRS`` repairs per answer.

The same applies to the other way a small model fails to finish: it writes its
analysis and the "=== JSON GRAPH ===" marker, then stops with no JSON at all.
Such an answer is resumed with just an opening brace.

An answer that neither loops nor stops at the marker is returned unchanged, so
unpatched baselines and cached answers are not affected.
"""
from __future__ import annotations

import re
from dataclasses import dataclass
from typing import Optional

from .loopguard import _ID_FIELD, truncate_loop

SECTIONS = ["facts", "issues", "rules", "applications", "conclusions", "obligations", "edges"]
_ID_SECTION = {"fid": "facts", "iid": "issues", "rid": "rules", "aid": "applications",
               "cid": "conclusions", "oid": "obligations", "eid": "edges"}
MAX_REPAIRS = 3
MARKER = "=== JSON GRAPH ==="


@dataclass
class Repaired:
    text: str
    looped: bool          # the original answer looped
    repairs: int          # continuations generated
    still_looped: bool    # gave up after MAX_REPAIRS (text is cut there)
    empty_json: bool = False   # the original answer stopped at the marker with no JSON


def stopped_at_marker(text: str) -> bool:
    """True if the answer wrote the JSON marker and then nothing that starts a JSON object."""
    return MARKER in text and "{" not in text.split(MARKER, 1)[1]


def resume_prefix(cut_text: str) -> Optional[str]:
    """The cut answer plus scaffolding that closes the looping list and opens the next.

    None if the loop was in the last section (nothing left to resume) or the
    looping section cannot be identified.
    """
    json_part = cut_text.split(MARKER, 1)[-1]
    kinds = [m.group(1) for m in _ID_FIELD.finditer(json_part)]
    if not kinds:
        return None
    i = SECTIONS.index(_ID_SECTION[kinds[-1]])
    if i + 1 >= len(SECTIONS):
        return None
    body = re.sub(r",\s*$", "", cut_text.rstrip())
    return f'{body}\n  ],\n  "{SECTIONS[i + 1]}": [\n'


def generate_with_repair(client, system: str, user: str,
                         max_repairs: int = MAX_REPAIRS) -> Repaired:
    """``client.generate``, with looping answers resumed past the loop.

    ``client`` needs ``generate(system=, user=)`` and, for repairs,
    ``continue_from(system=, user=, prefix=)``; both are cached.
    """
    text = client.generate(system=system, user=user).text
    empty = stopped_at_marker(text)
    if empty and hasattr(client, "continue_from"):
        prefix = text.rstrip() + "\n{\n"
        text = prefix + client.continue_from(system=system, user=user, prefix=prefix).text
    rep = _repair_loops(client, system, user, text, max_repairs)
    rep.empty_json = empty
    return rep


def _repair_loops(client, system: str, user: str, text: str, max_repairs: int) -> Repaired:
    looped_at_all = False
    for n in range(max_repairs + 1):
        cut, looped = truncate_loop(text)
        if not looped:
            return Repaired(text, looped_at_all, n, False)
        looped_at_all = True
        prefix = resume_prefix(cut)
        if prefix is None or n == max_repairs or not hasattr(client, "continue_from"):
            return Repaired(cut, True, n, True)
        text = prefix + client.continue_from(system=system, user=user, prefix=prefix).text
    return Repaired(truncate_loop(text)[0], True, max_repairs, True)


__all__ = ["Repaired", "resume_prefix", "stopped_at_marker", "generate_with_repair",
           "SECTIONS", "MAX_REPAIRS"]
