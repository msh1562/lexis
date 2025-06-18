from fastapi import FastAPI

from .routes import (
    user,
    summary,
    block,
    auth,
    book,
    citation,
    topic,
    history,
    trust,
)

app = FastAPI(title="Lexis API")

app.include_router(user.router)
app.include_router(summary.router)
app.include_router(block.router)
app.include_router(auth.router)
app.include_router(book.router)
app.include_router(citation.router)
app.include_router(topic.router)
app.include_router(history.router)
app.include_router(trust.router)

@app.get("/")
def read_root():
    return {"message": "Hello Lexis API"}