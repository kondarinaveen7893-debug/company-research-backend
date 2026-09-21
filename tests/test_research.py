import json


def _parse_sse(raw: str) -> list[dict]:
    events = []
    current_event = {}
    for line in raw.strip().splitlines():
        if line.startswith("event:"):
            current_event["event"] = line[len("event:"):].strip()
        elif line.startswith("data:"):
            current_event["data"] = json.loads(line[len("data:"):].strip())
        elif line == "" and current_event:
            events.append(current_event)
            current_event = {}
    if current_event:
        events.append(current_event)
    return events


def test_research_rejects_empty_company_name(client):
    response = client.post("/api/research", json={"company_name": ""})
    assert response.status_code == 422


def test_research_rejects_single_char_company_name(client):
    response = client.post("/api/research", json={"company_name": "x"})
    assert response.status_code == 422


def test_research_rejects_missing_company_name(client):
    response = client.post("/api/research", json={})
    assert response.status_code == 422


def test_research_streams_known_company(client):
    response = client.post("/api/research", json={"company_name": "Microsoft"})
    assert response.status_code == 200
    assert "text/event-stream" in response.headers["content-type"]

    events = _parse_sse(response.text)
    event_names = [e["event"] for e in events]

    assert "section" in event_names
    assert "complete" in event_names

    section_events = [e for e in events if e["event"] == "section"]
    section_names = [e["data"]["section"] for e in section_events]
    assert section_names == ["overview", "key_people", "news", "financials", "risks"]


def test_research_streams_unknown_company(client):
    response = client.post("/api/research", json={"company_name": "UnknownCorp XYZ"})
    assert response.status_code == 200

    events = _parse_sse(response.text)
    event_names = [e["event"] for e in events]
    assert "complete" in event_names


def test_research_persists_report_after_streaming(client):
    response = client.post("/api/research", json={"company_name": "Apple"})
    assert response.status_code == 200

    events = _parse_sse(response.text)
    complete_event = next(e for e in events if e["event"] == "complete")
    report_id = complete_event["data"]["report_id"]
    assert isinstance(report_id, int)

    detail_response = client.get(f"/api/reports/{report_id}")
    assert detail_response.status_code == 200
    assert detail_response.json()["company_name"] == "Apple"
