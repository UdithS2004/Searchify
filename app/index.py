import math

from .tokenizer import tokenize


class InvertedIndex:
    """A minimal in‑memory inverted index with TF‑IDF ranking."""

    def __init__(self) -> None:
        self.inverted: dict[str, dict[int, int]] = {}
        self.doc_store: dict[int, dict[str, str]] = {}
        self.doc_len: dict[int, int] = {}
        self.N: int = 0

    def upsert(self, doc_id: int, title: str, text: str) -> None:
        # remove existing entry if present
        if doc_id in self.doc_store:
            self.remove(doc_id)
        tokens = tokenize(text)
        freq: dict[str, int] = {}
        for t in tokens:
            freq[t] = freq.get(t, 0) + 1
        self.doc_store[doc_id] = {"title": title, "text": text}
        self.doc_len[doc_id] = len(tokens)
        for term, f in freq.items():
            postings = self.inverted.setdefault(term, {})
            postings[doc_id] = f
        self.N += 1

    def remove(self, doc_id: int) -> None:
        if doc_id not in self.doc_store:
            return
        entry = self.doc_store.pop(doc_id)
        tokens = tokenize(entry["text"])
        freq: dict[str, int] = {}
        for t in tokens:
            freq[t] = freq.get(t, 0) + 1
        for term in freq:
            postings = self.inverted.get(term)
            if postings and doc_id in postings:
                postings.pop(doc_id)
                if not postings:
                    self.inverted.pop(term)
        self.doc_len.pop(doc_id, None)
        self.N -= 1

    def search(self, query: str, k: int = 10) -> list[dict]:
        tokens = tokenize(query)
        if not tokens or self.N <= 0:
            return []
        scores: dict[int, float] = {}
        for term in tokens:
            postings = self.inverted.get(term)
            if not postings:
                continue
            df = len(postings)
            idf = math.log((self.N + 1) / (df + 1)) + 1.0
            for doc_id, freq in postings.items():
                tf = freq / (self.doc_len.get(doc_id) or 1)
                scores[doc_id] = scores.get(doc_id, 0.0) + tf * idf
        ranked = sorted(scores.items(), key=lambda p: p[1], reverse=True)[:k]
        return [
            {"id": doc_id, "title": self.doc_store[doc_id]["title"], "score": score}
            for doc_id, score in ranked
        ]