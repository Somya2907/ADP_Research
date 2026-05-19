"""Disk-backed response cache keyed on (namespace, model, system, user, params).

Saves real money during prompt iteration. Each call to teacher or agent on E1
costs ~$0.10-0.30; during prompt development you may run 20+ iterations.

Invalidation: delete .cache/ directory to force fresh calls.
"""
from __future__ import annotations

import hashlib
import json
from functools import wraps
from pathlib import Path
from typing import Any, Callable

import diskcache

CACHE_DIR = Path(".cache") / "llm"
CACHE_DIR.mkdir(parents=True, exist_ok=True)
_cache = diskcache.Cache(str(CACHE_DIR))


def _hash_key(namespace: str, model: str, system: str, user: str, params: dict) -> str:
    blob = json.dumps(
        {"ns": namespace, "model": model, "sys": system, "usr": user, "p": params},
        sort_keys=True,
    )
    return hashlib.sha256(blob.encode()).hexdigest()


def cached_call(namespace: str) -> Callable:
    """Decorator that caches LLM responses by (model, system, user, kwargs).

    Usage:
        @cached_call(namespace="teacher")
        def generate(self, system: str, user: str, **kwargs) -> LLMResponse:
            ...
    """

    def decorator(fn: Callable) -> Callable:
        @wraps(fn)
        def wrapper(self: Any, system: str, user: str, **kwargs) -> Any:
            key = _hash_key(namespace, self.model, system, user, kwargs)
            hit = _cache.get(key)
            if hit is not None:
                return hit
            result = fn(self, system=system, user=user, **kwargs)
            _cache.set(key, result)
            return result

        return wrapper

    return decorator


def clear_cache() -> int:
    """Clear all cached responses. Returns number of items cleared."""
    count = len(_cache)
    _cache.clear()
    return count


def cache_stats() -> dict[str, int]:
    """Return basic cache statistics."""
    return {
        "entries": len(_cache),
        "size_bytes": _cache.volume(),
    }
