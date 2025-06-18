from fastapi.testclient import TestClient
import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parents[1]))
from app.main import app

client = TestClient(app)


def test_lexify_summary():
    resp = client.post("/api/lexify/summary", json={"text": "a" * 120})
    assert resp.status_code == 200
    data = resp.json()
    assert "summary" in data
    assert data["summary"].startswith("a")
    assert len(data["summary"]) <= 103


def test_from_trace_fact_creates_block():
    resp = client.post(
        "/api/lexify/fromTraceFact",
        json={
            "title": "TF",
            "content": "text",
            "source_url": "http://example.com",
            "trust_score": 0.8,
        },
    )
    assert resp.status_code == 200
    block = resp.json()
    assert block["source_url"] == "http://example.com"