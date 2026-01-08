from typing import Any, Optional
from pydantic import BaseModel, Field


class ProjectCreate(BaseModel):
    name: str
    languages: list[str] = Field(default_factory=list)
    tone_profile: dict[str, Any] = Field(default_factory=dict)
    privacy_settings: dict[str, Any] = Field(default_factory=dict)


class ProjectOut(BaseModel):
    id: str
    name: str
    created_at: str
    languages: list[str]
    tone_profile: dict[str, Any]
    privacy_settings: dict[str, Any]


class AssetOut(BaseModel):
    id: str
    project_id: str
    path: str
    type: str
    duration: float
    resolution: str
    metadata: dict[str, Any]
    quality_scores: dict[str, Any]
    tags: list[str]


class ContentItemCreate(BaseModel):
    project_id: str
    format: str = "reel"
    status: str = "draft"
    captions: dict[str, str] = Field(default_factory=dict)
    hashtags: list[str] = Field(default_factory=list)
    on_screen_text: dict[str, str] = Field(default_factory=dict)
    storyboard: str = ""


class ContentItemOut(BaseModel):
    id: str
    project_id: str
    concept_id: str
    format: str
    status: str
    captions: dict[str, str]
    hashtags: list[str]
    on_screen_text: dict[str, str]
    sound_id: str
    storyboard: str
    compliance_notes: str
    created_at: str


class GenerateDraftIn(BaseModel):
    project_id: str
    asset_id: str


class ExportCreate(BaseModel):
    content_item_id: str
    format: str = "instagram"
    resolution: str = "1080x1920"


class ExportOut(BaseModel):
    id: str
    content_item_id: str
    export_path: str
    format: str
    specs: dict[str, Any]
    created_at: str


class IngestResponse(BaseModel):
    assets: list[AssetOut]
    skipped: list[str]


class Health(BaseModel):
    status: str
    version: str


class DecisionOut(BaseModel):
    id: str
    content_item_id: str
    agent: str
    decision: dict[str, Any]
    rationale: str
    confidence: float
    created_at: str


class LLMSettingsIn(BaseModel):
    provider: str = "openai"
    api_key: str = ""
    model: str = "gpt-4o-mini"
    ollama_enabled: bool = False
    ollama_host: str = "http://127.0.0.1:11434"
    ollama_model: str = "llama3"
    ollama_temperature: float = 0.7


class LLMSettingsOut(BaseModel):
    llm_provider: str
    openai_model: str
    ollama_enabled: bool
    ollama_host: str
    ollama_model: str
    ollama_temperature: float


class InstagramSettingsIn(BaseModel):
    access_token: str
    ig_user_id: str
    app_id: Optional[str] = None
    app_secret: Optional[str] = None
    dry_run: bool = True


class InstagramSettingsOut(BaseModel):
    configured: bool
    ig_user_id: str
    dry_run: bool


class InstagramPublishIn(BaseModel):
    content_item_id: str
    media_url: str
    media_type: str = "image"
    scheduled_publish_time: Optional[int] = None
    dry_run: bool = True


class InstagramPublishOut(BaseModel):
    status: str
    post_id: Optional[str] = None
    container_id: Optional[str] = None
    message: str
    used_media_url: Optional[str] = None


class TrendPackOut(BaseModel):
    items: list[dict[str, Any]]
    count: int


class ContentSoundUpdate(BaseModel):
    content_item_id: str
    sound_id: str


class MCPMessageIn(BaseModel):
    thread_id: str
    sender: str
    recipient: str = "broadcast"
    message: dict[str, Any]
    confidence: float = 0.0
    citations: list[str] = Field(default_factory=list)


class MCPMessageOut(BaseModel):
    id: str
    thread_id: str
    sender: str
    recipient: str
    message: dict[str, Any]
    confidence: float
    citations: list[str]
    created_at: str
