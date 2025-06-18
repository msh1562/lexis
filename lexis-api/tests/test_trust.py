import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parent))
from test_block import client, reset_db


def test_trust_votes_summary():
    reset_db()
    u1 = client.post("/auth/signup", json={"email": "t1@test.com", "password": "pw"}).json()
    u2 = client.post("/auth/signup", json={"email": "t2@test.com", "password": "pw"}).json()
    block = client.post("/api/block/", json={"title": "B", "content": "c"}).json()

    r1 = client.post(
        "/api/trust/",
        json={"block_id": block["id"], "user_id": u1["id"], "vote": "trust"},
    )
    assert r1.status_code == 200

    r2 = client.post(
        "/api/trust/",
        json={"block_id": block["id"], "user_id": u2["id"], "vote": "distrust"},
    )
    assert r2.status_code == 200

    summary = client.get(f"/api/trust/{block['id']}")
    assert summary.status_code == 200
    data = summary.json()
    assert data["trust"] == 1
    assert data["distrust"] == 1