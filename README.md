# Insta-Multi-Agent Studio

Local-first multi-agent pipeline engineered for travel + lifestyle creators. It ingests raw media, runs contextual agents (scene analysis, travel story, captions, sound, compliance), and exports polished Instagram/WIP packages.

## Highlights
- FastAPI backend + React UI for setup, ingestion, library, review, export, and Ollama chat.
- SQLite + FAISS-ready shared memory; decisions + MCP-style messaging for auditing.
- OpenAI + optional Ollama provider with local chat widget and logging.
- Instagram + scheduling exports via Graph API; Trend Pack management for compliant sound + hashtags.
- Tests covering ingestion, agents, exports, MCP messaging, Ollama flows.

## Getting Started
1. `cd backend` → `python -m venv .venv && source .venv/bin/activate`
2. `pip install -r requirements.txt`
3. `npm install` inside `frontend`
4. `ollama serve` (or `export OPENAI_API_KEY=...` and choose OpenAI in the UI)
5. `uvicorn app.main:app --reload --port 8000`
6. `npm run dev -- --host 0.0.0.0 --port 5173`

## Testing
- `backend/.venv/bin/pytest backend/tests -q`
- `backend/.venv/bin/pytest backend/tests/test_ollama_chat.py -q` for Ollama health.

## Docs
- `docs/ARCHITECTURE.md`: module, UI, agent, and data flow details.
- `docs/AGENTS.md`: agent responsibilities + message patterns.

## Next Steps
- Replace Ollama stub if you want remote GPUs.
- Add Playwright UI E2E if necessary.
