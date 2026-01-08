# Agent Reference

| Agent | Responsibility | Key Inputs | Outputs | Logging |
| --- | --- | --- | --- | --- |
| Media Analyst (future) | Scene detection, quality metadata | Asset path, privacy settings | Quality scores, best clips | MCC messages recorded by orchestrator |
| Location Agent | Guess location benefit and questions | Project context, asset metadata | `location_hint`, `key_questions` | MCP log entries, decisions table |
| Reel Agent | Storyboard / hook / on-screen text | Context + MCU history | `hook`, `storyboard`, `on_screen_text` | MCP + decisions |
| Sound Agent | Trendy sound + tempo hint | Vibe + trend pack | `sound_style`, `tempo_bpm`, `trend_hint` | Keeps `sound_id` in ContentItem + decisions |
| Caption Agent | Multilingual captions + CTA | Context, mixing rules | Draft captions (EN/DE/HI), hashtags, CTA | Decisions + consolidated output |
| Brand Guardian | Compliance (future) | Privacy settings + asset metadata | Notes, warnings | Store in `content_items.compliance_notes` |
| QA Agent | Duplication/policy (future) | Content graph | Readiness verdict | Logged via MCP when added |

The orchestrator writes to `agent_messages` for every agent run, making the decision log inspectable via `/mcp/messages`.
