import json

import pytest


def test_ollama_chat_requires_enabled(monkeypatch, client):
    def fake_settings():
        return {"ollama": {"enabled": False}}

    monkeypatch.setattr("app.routers.ollama_chat.load_settings", fake_settings)
    payload = {"prompt": "Hello"}
    response = client.post("/ollama/chat", json=payload)
    assert response.status_code == 503
    assert "disabled" in response.json()["detail"].lower()


def test_ollama_chat_success(monkeypatch, client):
    def fake_load_settings():
        return {
            "ollama": {"enabled": True, "host": "http://example.com", "model": "llama3", "temperature": 0.4}
        }

    def fake_query(prompt, host, model, temperature):
        assert prompt == "Hey"
        return "response"

    monkeypatch.setattr("app.routers.ollama_chat.load_settings", fake_load_settings)
    monkeypatch.setattr("app.services.ollama_client.query_ollama", fake_query)

    response = client.post("/ollama/chat", json={"prompt": "Hey"})
    assert response.status_code == 200
    assert response.json()["response"] == "response"
