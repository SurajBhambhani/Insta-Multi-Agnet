def test_create_and_list_projects(client):
    payload = {
        "name": "Test Project",
        "languages": ["English"],
        "tone_profile": {"cinematic": 80},
        "privacy_settings": {"blur_faces": True},
    }
    create = client.post("/projects", json=payload)
    assert create.status_code == 200
    project = create.json()
    assert project["name"] == "Test Project"

    listing = client.get("/projects")
    assert listing.status_code == 200
    items = listing.json()
    assert any(p["id"] == project["id"] for p in items)
