class TrieNode:
    """Simple trie node storing children and end‑of‑word flag."""

    def __init__(self) -> None:
        self.children: dict[str, 'TrieNode'] = {}
        self.is_end: bool = False


class Autocomplete:
    """Trie‑based prefix suggester."""

    def __init__(self) -> None:
        self.root = TrieNode()

    def insert(self, word: str) -> None:
        if not word:
            return
        node = self.root
        for c in word:
            node = node.children.setdefault(c, TrieNode())
        node.is_end = True

    def _dfs(self, node: TrieNode, prefix: str, results: list[str], k: int) -> None:
        if len(results) >= k:
            return
        if node.is_end:
            results.append(prefix)
        for c in sorted(node.children.keys()):
            self._dfs(node.children[c], prefix + c, results, k)

    def suggest(self, prefix: str, k: int = 5) -> list[str]:
        if not prefix:
            return []
        node = self.root
        for c in prefix:
            if c not in node.children:
                return []
            node = node.children[c]
        results: list[str] = []
        self._dfs(node, prefix, results, k)
        return results