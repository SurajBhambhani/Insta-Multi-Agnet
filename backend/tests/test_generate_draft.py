import io

from PIL import Image

from app.agents.base import AgentResult
from app.services import orchestrator


def _make_image_bytes() -> bytes:
    image = Image.new("RGB", (10, 10), color=(120, 90, 60))
    buffer = io.BytesIO()
    image.save(buffer, format="JPEG")
    return buffer.getvalue()


def _create_project_and_asset(client):
    project = client.post("/projects", json={"name": "Draft Project"}).json()
    img_bytes = _make_image_bytes()
    files = [("files", ("sample.jpg", img_bytes, "image/jpeg"))]
    ingest = client.post(
        "/assets/ingest",
        data={"project_id": project["id"]},
        files=files,
    )
    asset_id = ingest.json()["assets"][0]["id"]
    return project, asset_id


def test_generate_requires_asset(client):
    project = client.post("/projects", json={"name": "Missing Asset"}).json()
    response = client.post(
        "/content/generate",
        json={"project_id": project["id"], "asset_id": "missing"},
    )
    assert response.status_code == 404


def test_generate_applies_hashtag_rules(monkeypatch, client):
    project, asset_id = _create_project_and_asset(client)

    def fake_caption_agent(context):
        return AgentResult(
            name="CaptionAgent",
            output={"captions": {"en": "Test"}, "hashtags": ["#Travel", "#follow4follow"]},
            confidence=0.5,
        )

    monkeypatch.setattr(orchestrator, "run_caption_agent", fake_caption_agent)

    generated = client.post(
        "/content/generate",
        json={"project_id": project["id"], "asset_id": asset_id},
    )
    assert generated.status_code == 200
    payload = generated.json()
    hashtags = [tag.lower() for tag in payload["hashtags"]]
    assert "#follow4follow" not in hashtags
    assert len(hashtags) >= 8
    assert len(hashtags) <= 20


def test_generate_dedupes_hashtags(monkeypatch, client):
    project, asset_id = _create_project_and_asset(client)

    def fake_caption_agent(context):
        return AgentResult(
            name="CaptionAgent",
            output={"captions": {"en": "Test"}, "hashtags": ["Travel", "#travel", "#Travel"]},
            confidence=0.5,
        )

    monkeypatch.setattr(orchestrator, "run_caption_agent", fake_caption_agent)

    generated = client.post(
        "/content/generate",
        json={"project_id": project["id"], "asset_id": asset_id},
    )
    assert generated.status_code == 200
    payload = generated.json()
    hashtags = [tag.lower() for tag in payload["hashtags"]]
    assert hashtags.count("#travel") == 1
