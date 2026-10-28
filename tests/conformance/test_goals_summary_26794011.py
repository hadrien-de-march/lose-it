"""Regression guard for the ``GoalsSummary/26794011`` schema (web build BFC488B2…).

Lose It!'s 2026-10-28 redeploy changed ``GoalsSummary`` from ``/907689655``
(23 fields) to ``/26794011`` (22 fields: one of the two adjacent booleans at
positions 11-12 is gone). Every daily-details response carries one, so a
missing or misaligned schema leaves the whole range response ``__partial__``
and no entry is read.

The stream below is synthetic (no captured account data): an ``ArrayList``
holding one ``GoalsSummary`` followed by an ``Integer`` sentinel. If the
schema reads one token too many or too few, the sentinel comes out wrong.
"""

from __future__ import annotations

from lose_it.core._decoder import decode_response

_ARRAY_LIST = "java.util.ArrayList/4159755760"
_GOALS_SUMMARY = "com.loseit.core.client.model.GoalsSummary/26794011"
_INTEGER = "java.lang.Integer/3438268394"

# Field kinds in declaration order, read from deserializer ``nPg`` of the
# BFC488B2F9DCB4070D92CF9DD2B23810 permutation, with the token each one gets.
_FIELDS: list[tuple[str, object]] = [
    ("OBJECT", 0), ("OBJECT", 0), ("BOOLEAN", 1), ("DOUBLE", 1.5),
    ("OBJECT", 0), ("OBJECT", 0), ("DOUBLE", 2.5), ("OBJECT", 0),
    ("OBJECT", 0), ("OBJECT", 0), ("DOUBLE", 3.5), ("BOOLEAN", 0),
    ("DOUBLE", 4.5), ("OBJECT", 0), ("OBJECT", 0), ("OBJECT", 0),
    ("OBJECT", 0), ("OBJECT", 0), ("OBJECT", 0), ("OBJECT", 0),
    ("DOUBLE", 5.5), ("BOOLEAN", 1),
]
_SENTINEL = 42


def _body() -> str:
    # Read order: list type, length, GoalsSummary type, its fields, Integer type, sentinel.
    read_order: list[object] = [1, 2, 2, *(token for _, token in _FIELDS), 3, _SENTINEL]
    data = ",".join(str(token) for token in reversed(read_order))
    strings = ",".join(f'"{s}"' for s in (_ARRAY_LIST, _GOALS_SUMMARY, _INTEGER))
    return f"//OK[{data},[{strings}],0,7]"


def test_goals_summary_26794011_reads_exactly_its_fields() -> None:
    decoded = decode_response(_body(), strict=True)

    summary, sentinel = decoded["items"]
    assert summary["__type__"] == _GOALS_SUMMARY
    assert sentinel == _SENTINEL
    assert [summary[f"f{i}"] for i in (3, 6, 10, 12, 20)] == [1.5, 2.5, 3.5, 4.5, 5.5]
    assert [summary[f"f{i}"] for i in (2, 11, 21)] == [True, False, True]
    assert "f22" not in summary
