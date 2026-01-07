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
