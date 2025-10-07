from typing import List

from fastapi import FastAPI, HTTPException, Query
from pydantic import BaseModel

from .index import InvertedIndex
from .autocomplete import Autocomplete
from .tokenizer import tokenize

app = FastAPI(title="Searchify API")

_index = InvertedIndex()
_autocomplete = Autocomplete()

class Document(BaseModel):
    id: int
    title: str
    text: str

class IndexRequest(BaseModel):
    documents: List[Document]

@app.post("/index")
def index_documents(request: IndexRequest) -> dict:
    count = 0
    for doc in request.documents:
        _index.upsert(doc.id, doc.title, doc.text)
        for tok in set(tokenize(doc.text)):
            _autocomplete.insert(tok)
        count += 1
    return {"indexed": count}

@app.get("/search")
def search(q: str = Query(...), k: int = 10) -> dict:
    return {"results": _index.search(q, k)}

@app.get("/suggest")
def suggest(prefix: str = Query(...), k: int = 5) -> dict:
    return {"suggestions": _autocomplete.suggest(prefix, k)}

@app.delete("/documents/{doc_id}")
def delete_document(doc_id: int) -> dict:
    if doc_id not in _index.doc_store:
        raise HTTPException(status_code=404, detail="Document not found")
    _index.remove(doc_id)
    return {"removed": doc_id}

@app.get("/stats")
def stats() -> dict:
    return {"documents": _index.N, "terms": len(_index.inverted)}