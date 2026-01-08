from app.services import llm as llm_service


def test_generate_text_uses_ollama(monkeypatch):
    def fake_load_settings():
        return {
            "llm_provider": "ollama",
            "ollama": {
                "enabled": True,
                "host": "http://127.0.0.1:11434",
                "model": "llama3",
                "temperature": 0.5,
            },
            "openai_api_key": "",
            "openai_model": "gpt-4o-mini",
        }

    def fake_query(prompt, host, model, temperature):
        assert prompt == "Test prompt"
        assert host.startswith("http://")
        assert model == "llama3"
        assert temperature == 0.5
        return "ollama result"

    monkeypatch.setattr(llm_service, "load_settings", fake_load_settings)
    monkeypatch.setattr(llm_service, "query_ollama", fake_query)

    result = llm_service.generate_text("Test prompt", "fallback")
    assert result == "ollama result"


def test_generate_text_falls_back_when_ollama_missing(monkeypatch):
    def fake_load_settings():
        return {"llm_provider": "ollama", "ollama": {"enabled": False}, "openai_api_key": "", "openai_model": "gpt-4o-mini"}

    monkeypatch.setattr(llm_service, "load_settings", fake_load_settings)

    result = llm_service.generate_text("Test prompt", "fallback")
    assert result == "fallback"
