import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parent))
from test_block import client, reset_db


def create_blocks():
    b1 = client.post(
        "/api/block/",
        json={"title": "A", "content": "A", "topic": "t", "trust_score": 0.9},
    ).json()
    b2 = client.post(
        "/api/block/",
        json={"title": "B", "content": "B", "topic": "t", "trust_score": 0.8},
    ).json()
    return b1, b2


def test_create_and_get_book():
    reset_db()
    b1, b2 = create_blocks()
    resp = client.post(
        "/api/book/",
        json={
            "title": "My Book",
            "description": "Desc",
            "block_ids": [b1["id"], b2["id"]],
        },
    )
    assert resp.status_code == 200
    data = resp.json()
    assert data["slug"].startswith("my-book")
    assert len(data["blocks"]) == 2
    get_resp = client.get(f"/api/book/{data['slug']}")
    assert get_resp.status_code == 200
    fetched = get_resp.json()
    assert fetched["title"] == "My Book"
    assert [b["id"] for b in fetched["blocks"]] == [b1["id"], b2["id"]]


def test_list_books():
    reset_db()
    b1, b2 = create_blocks()
    client.post(
        "/api/book/",
        json={"title": "First", "description": "", "block_ids": [b1["id"]]},
    )
    client.post(
        "/api/book/",
        json={"title": "Second", "description": "", "block_ids": [b2["id"]]},
    )

    resp = client.get("/api/book/")
    assert resp.status_code == 200
    data = resp.json()
    assert len(data) == 2


def test_update_and_delete_book():
    reset_db()
    b1, b2 = create_blocks()
    resp = client.post(
        "/api/book/",
        json={"title": "Book", "description": "d", "block_ids": [b1["id"]]},
    )
    slug = resp.json()["slug"]

    up = client.put(
        f"/api/book/{slug}",
        json={"title": "New", "description": "n", "block_ids": [b2["id"], b1["id"]]},
    )
    assert up.status_code == 200
    data = up.json()
    assert data["title"] == "New"
    assert [b["id"] for b in data["blocks"]] == [b2["id"], b1["id"]]

    del_resp = client.delete(f"/api/book/{slug}")
    assert del_resp.status_code == 200
    get_resp = client.get(f"/api/book/{slug}")
    assert get_resp.status_code == 404