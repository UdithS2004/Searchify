"""Tests for the inverted index and tokenisation logic."""

from app.index import InvertedIndex
from app.tokenizer import tokenize


def test_tokenize_basic() -> None:
    assert tokenize("Hello, World!") == ["hello", "world"]
    assert tokenize("Mixed CASE text.") == ["mixed", "case", "text"]
    assert tokenize("123 ABC!") == ["abc"]
    assert tokenize("") == []


def test_upsert_and_remove() -> None:
    idx = InvertedIndex()
    idx.upsert(1, "A", "apple banana")
    idx.upsert(2, "B", "apple apple banana")
    # two docs inserted
    assert idx.N == 2
    assert idx.doc_len[1] == 2
    assert idx.doc_len[2] == 3
    # inverted postings should contain both docs for 'apple'
    assert set(idx.inverted["apple"].keys()) == {1, 2}
    # remove first doc
    idx.remove(1)
    assert idx.N == 1
    assert 1 not in idx.doc_store
    # posting for 'apple' should only have doc 2
    assert set(idx.inverted["apple"].keys()) == {2}
