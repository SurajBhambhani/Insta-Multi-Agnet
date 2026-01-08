def test_create_content_item(client):
    project = client.post("/projects", json={"name": "Content Project"}).json()

    payload = {
        "project_id": project["id"],
        "format": "reel",
        "captions": {"en": "Hello"},
        "hashtags": ["#travel"],
        "on_screen_text": {"en": "Intro"},
        "storyboard": "Hook -> Scene -> CTA",
    }
    response = client.post("/content", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data["format"] == "reel"


def test_delete_content_item(client):
    project = client.post("/projects", json={"name": "Delete Content"}).json()
    payload = {
        "project_id": project["id"],
        "format": "reel",
        "captions": {"en": "Hello"},
        "hashtags": ["#travel"],
        "on_screen_text": {"en": "Intro"},
        "storyboard": "Hook -> Scene -> CTA",
    }
    response = client.post("/content", json=payload)
    content_id = response.json()["id"]

    deleted = client.delete(f"/content/{content_id}")
    assert deleted.status_code == 200
    assert deleted.json()["id"] == content_id

    listing = client.get(f"/content?project_id={project['id']}")
    assert listing.status_code == 200
    assert listing.json() == []
