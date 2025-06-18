from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool
import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parents[1]))
from app.main import app
from app.database import Base, get_db

engine = create_engine(
    "sqlite://",
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base.metadata.create_all(bind=engine)


def reset_db():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)


def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()

app.dependency_overrides[get_db] = override_get_db
client = TestClient(app)


def test_create_and_read_block():
    reset_db()
    resp = client.post(
        "/api/block/",
        json={
            "title": "Example",
            "content": "Content",
            "trust_score": 0.9,
            "topic": "news",
            "source_url": "http://source",
        },
    )
    assert resp.status_code == 200
    data = resp.json()
    assert data["id"] == 1
    assert data["title"] == "Example"
    assert data["trust_score"] == 0.9

    get_resp = client.get(f"/api/block/{data['id']}")
    assert get_resp.status_code == 200
    fetched = get_resp.json()
    assert fetched["title"] == "Example"
    assert fetched["source_url"] == "http://source"


def test_create_without_topic():
    reset_db()
    resp = client.post(
        "/api/block/",
        json={"title": "NoTopic", "content": "Body"},
    )
    assert resp.status_code == 200
    data = resp.json()
    assert data["topic"] is None


def test_list_blocks():
    reset_db()
    client.post(
        "/api/block/",
        json={
            "title": "First",
            "content": "One",
            "trust_score": 0.8,
            "topic": "news",
        },
    )
    client.post(
        "/api/block/",
        json={
            "title": "Second",
            "content": "More",
            "trust_score": 0.5,
            "topic": "tech",
        },
    )

    resp = client.get("/api/block/")
    assert resp.status_code == 200
    data = resp.json()
    assert len(data) == 2

    filtered = client.get("/api/block/?topic=tech")
    assert filtered.status_code == 200
    items = filtered.json()
    assert len(items) == 1
    assert items[0]["topic"] == "tech"


def test_block_with_citation():
    reset_db()
    base = client.post(
        "/api/block/",
        json={"title": "Base", "content": "txt"},
    ).json()
    resp = client.post(
        "/api/block/",
        json={
            "title": "Child",
            "content": "child",
            "citation_ids": [base["id"]],
        },
    )
    assert resp.status_code == 200
    data = resp.json()
    assert len(data["citations"]) == 1
    assert data["citations"][0]["to_block_id"] == base["id"]


def test_sort_blocks():
    reset_db()
    client.post(
        "/api/block/",
        json={"title": "Old", "content": "a", "trust_score": 0.2},
    )
    client.post(
        "/api/block/",
        json={"title": "New", "content": "b", "trust_score": 0.9},
    )

    resp = client.get("/api/block/?sort=trust")
    assert resp.status_code == 200
    data = resp.json()
    assert data[0]["trust_score"] >= data[1]["trust_score"]


def test_search_blocks():
    reset_db()
    client.post("/api/block/", json={"title": "Alpha", "content": "foo"})
    client.post("/api/block/", json={"title": "Beta", "content": "bar"})

    resp = client.get("/api/block/search?q=Alp")
    assert resp.status_code == 200
    data = resp.json()
    assert len(data) == 1
    assert data[0]["title"] == "Alpha"