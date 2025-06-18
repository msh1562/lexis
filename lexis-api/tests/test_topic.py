import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parent))
from test_block import client, reset_db


def test_create_and_list_topics():
    reset_db()
    # create root
    r1 = client.post("/api/topic/", json={"name": "Root"})
    assert r1.status_code == 200
    root = r1.json()
    assert root["depth"] == 0

    r2 = client.post("/api/topic/", json={"name": "Child", "parent_id": root["id"]})
    assert r2.status_code == 200
    child = r2.json()
    assert child["depth"] == 1

    resp = client.get("/api/topic/")
    assert resp.status_code == 200
    data = resp.json()
    assert [n["name"] for n in data] == ["Root", "Child"]