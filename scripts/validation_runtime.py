#!/usr/bin/env python3
"""Runtime invariants shared by release-critical validators."""

from __future__ import annotations

import sys


def require_assertions_enabled() -> None:
    """Fail closed when optimization would remove validation assertions."""
    if sys.flags.optimize != 0 or not __debug__:
        raise SystemExit(
            "Validation requires assertions; unset PYTHONOPTIMIZE and do not use -O/-OO."
        )
