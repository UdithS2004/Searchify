# Searchify

Searchify is a simple yet realistic full‑text search backend built as a learning exercise.
It demonstrates how a miniature “search engine” can be assembled using only Python, FastAPI
and in‑memory data structures.  The goal is to keep the code approachable while still
providing enough features to feel like a real system.

## What it does

Searchify lets you upload plain‑text documents, automatically builds an inverted index
over the words they contain and exposes a tiny API to query that index.  You can

* **Index** documents by sending them to the `/index` endpoint.
* **Search** for keywords using a simple TF‑IDF ranking algorithm via the `/search` endpoint.
* **Autocomplete** on partial words using a trie via the `/suggest` endpoint.
* **Remove** documents with the `/documents/{id}` endpoint.
* **Inspect** the number of indexed documents and terms using `/stats`.

Everything runs entirely in memory—no external databases or services are required.

## Installation & running

1. Clone or unpack this repository.
2. Install the dependencies into a Python 3.13 environment:

   ```bash
   pip install -r requirements.txt
   ```

3. Start the API using Uvicorn:

   ```bash
   uvicorn app.main:app --reload
   ```

   The `--reload` flag restarts the server whenever you edit the code.

4. Open http://127.0.0.1:8000/docs in your browser to explore the automatically generated
   interactive API documentation provided by FastAPI.

## Example usage

Below are example `curl` commands demonstrating the core functionality.  Feel free to
adapt the JSON payloads to suit your own documents.

### Indexing documents

```bash
curl -X POST "http://127.0.0.1:8000/index" \
     -H "Content-Type: application/json" \
     -d '{"documents": [
       {"id": 1, "title": "First doc", "text": "The quick brown fox jumps over the lazy dog."},
       {"id": 2, "title": "Second doc", "text": "Pack my box with five dozen liquor jugs."}
     ]}'
```

### Searching for keywords

```bash
curl "http://127.0.0.1:8000/search?q=quick+brown&k=2"
```

The response will include the top‑k documents ranked by TF‑IDF score.  Each result
contains the document `id`, its `title` and a numeric `score`.

### Getting autocomplete suggestions

```bash
curl "http://127.0.0.1:8000/suggest?prefix=qu&k=5"
```

Returns up to five words beginning with the given prefix.

### Removing a document

```bash
curl -X DELETE "http://127.0.0.1:8000/documents/1"
```

### Viewing stats

```bash
curl "http://127.0.0.1:8000/stats"
```

## Testing

Searchify includes a small pytest suite in the `tests/` directory.  To run the tests
simply execute:

```bash
pytest
```

The tests cover tokenisation, indexing/removal, ranking and autocomplete behaviour.

## Project layout

```
searchify/
  app/
    __init__.py         # marks the package
    main.py             # FastAPI entrypoint and routing
    index.py            # inverted index and TF‑IDF ranking logic
    tokenizer.py        # text cleanup and tokenisation utilities
    autocomplete.py     # trie based autocomplete implementation
  tests/
    test_index.py       # unit tests for indexing and removal
    test_search.py      # unit tests for search and autocomplete
  requirements.txt      # project dependencies
  README.md             # this file
```

All Python files together contain fewer than 300 lines of code, emphasising clarity over
complexity.  While Searchify should not be used as a production search engine, it serves
as a compact example of core concepts such as inverted indices, TF‑IDF ranking and tries.
