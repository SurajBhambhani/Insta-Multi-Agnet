import io

from PIL import Image


def _make_image_bytes() -> bytes:
    image = Image.new("RGB", (10, 10), color=(120, 90, 60))
    buffer = io.BytesIO()
    image.save(buffer, format="JPEG")
    return buffer.getvalue()


def _create_content_item(client):
    project = client.post("/projects", json={"name": "IG Project"}).json()
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
    return generated.json()["id"]


def test_instagram_settings_roundtrip(client):
    payload = {
        "ig_user_id": "123456",
        "access_token": "token",
        "dry_run": True,
    }
    saved = client.post("/instagram/settings", json=payload)
    assert saved.status_code == 200
    data = saved.json()
    assert data["configured"] is True
    assert data["ig_user_id"] == "123456"
    assert data["dry_run"] is True

    fetched = client.get("/instagram/settings")
    assert fetched.status_code == 200
    fetched_data = fetched.json()
    assert fetched_data["configured"] is True


def test_instagram_publish_dry_run(client):
    content_id = _create_content_item(client)
    client.post(
        "/instagram/settings",
        json={
            "ig_user_id": "123456",
            "access_token": "token",
            "dry_run": True,
        },
    )

    response = client.post(
        "/instagram/publish",
        json={
            "content_item_id": content_id,
            "media_url": "https://example.com/test.jpg",
            "dry_run": True,
        },
    )
    assert response.status_code == 200
    payload = response.json()
    assert payload["status"] == "dry_run"
