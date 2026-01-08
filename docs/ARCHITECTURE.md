# Architecture Overview

## Application Layers
- **Frontend (React + Vite)**: Setup/Preferences, Library, Content Builder, Trend Pack, Instagram Publishing, Ollama Chat panels.
- **Backend (FastAPI)**: Project/asset/content CRUD, trend-pack ingestion, MCP message bus, exports, Ollama chat, Instagram Graph API integration.
- **LLM Services**: `llm.py` orchestrates OpenAI + Ollama, falling back to stub prompts if nothing responds.
- **Agents & Orchestrator**: `agents/*.py` produce captions, sound, location, storyline; `orchestrator` records decisions and publishes MCP messages.
- **Data & Persistence**: SQLite tables (`projects`, `assets`, `content_items`, `decisions`, `exports`, `agent_messages`); exported packages write JSON/markdown + preview images under `backend/data/projects/…/exports/`.

## Flow
1. UI uploads media → `POST /assets/ingest` → stored under `backend/data/projects/<id>/assets`.
2. User selects asset and triggers `POST /content/generate`. Orchestrator: create draft, run agents sequentially, log decisions, push MCP messages, publish to SQLite.
3. Export (`POST /exports`) serializes metadata/captions/hashtags/decisions + preview image and saves to disk.
4. Instagram publishing (`POST /instagram/publish`) queries Graph API for image or Reel (scheduled optional). Ollama chat allows prompt/responses and logs successes/failures in `server.log`.

## Integrations
- **Trend Pack CSV**: Uploaded per project, parsed via `trend_pack` router. UI picks a sound + assigns it to drafts.
- **MCP Bus**: `agent_messages` table; ORchestrator writes agent outputs, API exposes `/mcp/messages` for logs.
- **Ollama Provider**: `ollama_client` hits local `ollama serve`; logs `+`/`-` entries, toggled through `/settings/llm`.
- **Testing**: Extensive pytest suite covers ingestion, exports, MCP, Ollama flows.
