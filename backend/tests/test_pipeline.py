import io

from PIL import Image


def _make_image_bytes() -> bytes:
    image = Image.new("RGB", (10, 10), color=(120, 90, 60))
    buffer = io.BytesIO()
    image.save(buffer, format="JPEG")
    return buffer.getvalue()


def test_pipeline_creates_content_and_decisions(client):
    project = client.post("/projects", json={"name": "Pipeline Project"}).json()

    img_bytes = _make_image_bytes()
    files = [("files", ("sample.jpg", img_bytes, "image/jpeg"))]
    ingest = client.post(
        "/assets/ingest",
        data={"project_id": project["id"]},
        files=files,
    )
    assert ingest.status_code == 200
    asset_id = ingest.json()["assets"][0]["id"]

    generated = client.post(
        "/content/generate",
        json={"project_id": project["id"], "asset_id": asset_id},
    )
    assert generated.status_code == 200
    content_id = generated.json()["id"]

    decisions = client.get(f"/decisions?content_item_id={content_id}").json()
    assert len(decisions) >= 4
