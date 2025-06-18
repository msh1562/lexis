import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parent))
from test_block import client, reset_db


def test_create_citation():
    reset_db()
    b1 = client.post("/api/block/", json={"title": "A", "content": "a"}).json()
    b2 = client.post("/api/block/", json={"title": "B", "content": "b"}).json()
    resp = client.post(
        "/api/citation/",
        json={
            "from_block_id": b1["id"],
            "to_block_id": b2["id"],
            "type": "quote",
            "reason": "support",
        },
    )
    assert resp.status_code == 200
    data = resp.json()
    assert data["from_block_id"] == b1["id"]
    assert data["to_block_id"] == b2["id"]
    assert data["type"] == "quote"
    assert data["reason"] == "support"
    assert "created_at" in data


def test_list_citations():
    reset_db()
    b1 = client.post("/api/block/", json={"title": "A", "content": "a"}).json()
    b2 = client.post("/api/block/", json={"title": "B", "content": "b"}).json()
    client.post(
        "/api/citation/",
        json={"from_block_id": b1["id"], "to_block_id": b2["id"], "type": "quote"},
    )
    resp = client.get("/api/citation/?from_block_id=" + str(b1["id"]))
    assert resp.status_code == 200
    data = resp.json()
    assert len(data) == 1


def test_citation_graph():
    reset_db()
    a = client.post("/api/block/", json={"title": "A", "content": "a"}).json()
    b = client.post("/api/block/", json={"title": "B", "content": "b"}).json()
    client.post(
        "/api/citation/",
        json={"from_block_id": a["id"], "to_block_id": b["id"], "type": "quote"},
    )

    resp = client.get(f"/api/citation/graph/{a['id']}")
    assert resp.status_code == 200
    data = resp.json()
    ids = {blk["id"] for blk in data["blocks"]}
    assert a["id"] in ids and b["id"] in ids
    assert len(data["citations"]) == 1
    assert data["citations"][0]["reason"] is None