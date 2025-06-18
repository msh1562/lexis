import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parent))
from test_block import client, reset_db


def test_create_and_list_history():
    reset_db()
    user = client.post("/auth/signup", json={"email": "h@test.com", "password": "pw"}).json()
    block = client.post("/api/block/", json={"title": "T", "content": "C"}).json()
    resp = client.post(
        "/api/history/",
        json={"user_id": user["id"], "block_id": block["id"], "action": "view"},
    )
    assert resp.status_code == 200
    hist = resp.json()
    assert hist["action"] == "view"

    get_resp = client.get("/api/history/?user_id=" + str(user["id"]))
    assert get_resp.status_code == 200
    data = get_resp.json()
    assert len(data) == 1
    assert data[0]["id"] == hist["id"]