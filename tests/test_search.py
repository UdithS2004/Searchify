"""Tests for search ranking and autocomplete functionality."""

from app.index import InvertedIndex
from app.autocomplete import Autocomplete


def test_ranking_order() -> None:
    idx = InvertedIndex()
    # Doc 1 contains one apple, doc 2 contains two apples, doc 3 no apples
    idx.upsert(1, "Doc1", "apple banana")
    idx.upsert(2, "Doc2", "apple apple banana")
    idx.upsert(3, "Doc3", "banana banana banana")
    results = idx.search("apple", k=3)
    # Document 2 should rank highest due to higher tf
    assert results[0]["id"] == 2
    assert results[1]["id"] == 1
    # Doc3 does not contain apple, so should either not appear or be last
    ids = [r["id"] for r in results]
    assert 3 not in ids or ids[-1] == 3


def test_autocomplete_suggestions() -> None:
    ac = Autocomplete()
    words = ["app", "apple", "apply", "banana", "band"]
    for w in words:
        ac.insert(w)
    # Suggestions for 'app' should include app, apple and apply
    sugg = ac.suggest("app", k=5)
    assert set([s for s in sugg if s.startswith("app")]) >= {"app", "apple", "apply"}
    # Suggestions for 'ban' should return banana and band in order
    ban = ac.suggest("ban", k=2)
    assert ban == sorted([w for w in words if w.startswith("ban")])[:2]
