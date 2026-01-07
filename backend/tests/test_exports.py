import io
from pathlib import Path

from PIL import Image


def _make_image_bytes() -> bytes:
    image = Image.new("RGB", (10, 10), color=(120, 90, 60))
    buffer = io.BytesIO()
    image.save(buffer, format="JPEG")
    return buffer.getvalue()


def test_export_creates_files(client):
    project = client.post("/projects", json={"name": "Export Project"}).json()
    img_bytes = _make_image_bytes()
    ingest = client.post(
        "/assets/ingest",
        data={"project_id": project["id"]},
        files=[("files", ("sample.jpg", img_bytes, "image/jpeg"))],
    )
    asset_id = ingest.json()["assets"][0]["id"]

    generated = client.post(
        "/content/generate",
        json={"project_id": project["id"], "asset_id": asset_id},
    )
    content_id = generated.json()["id"]

    exported = client.post(
        "/exports",
        json={"content_item_id": content_id, "format": "instagram", "resolution": "1080x1920"},
    )
    assert exported.status_code == 200
    payload = exported.json()
    export_path = Path(payload["export_path"])
    assert export_path.exists()
    assert (export_path / "metadata.json").exists()
    assert (export_path / "caption.md").exists()
    assert (export_path / "preview.jpg").exists()
