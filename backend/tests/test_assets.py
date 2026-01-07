import io

from PIL import Image


def _make_image_bytes() -> bytes:
    image = Image.new("RGB", (10, 10), color=(120, 90, 60))
    buffer = io.BytesIO()
    image.save(buffer, format="JPEG")
    return buffer.getvalue()


def test_ingest_assets(client):
    project = client.post("/projects", json={"name": "Ingest Project"}).json()

    img_bytes = _make_image_bytes()
    files = [
        (
            "files",
            ("sample.jpg", img_bytes, "image/jpeg"),
        )
    ]
    response = client.post(
        "/assets/ingest",
        data={"project_id": project["id"]},
        files=files,
    )
    assert response.status_code == 200
    payload = response.json()
    assert payload["assets"]
    assert payload["assets"][0]["type"] == "photo"
