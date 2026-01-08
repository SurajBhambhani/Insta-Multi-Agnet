import io


def test_trend_pack_upload_and_fetch(client):
    project = client.post("/projects", json={"name": "Trend Pack"}).json()
    csv_data = "title,artist,region\nSunset Drive,Artist A,EU\n"
    file_obj = io.BytesIO(csv_data.encode("utf-8"))
    response = client.post(
        "/trend-pack",
        data={"project_id": project["id"]},
        files={"file": ("trend.csv", file_obj, "text/csv")},
    )
    assert response.status_code == 200
    payload = response.json()
    assert payload["count"] == 1

    fetched = client.get(f"/trend-pack?project_id={project['id']}")
    assert fetched.status_code == 200
    assert fetched.json()["count"] == 1
