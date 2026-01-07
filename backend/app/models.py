import uuid
from datetime import datetime
from sqlalchemy import String, Text, Float, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .db import Base


def _uuid() -> str:
    return str(uuid.uuid4())


def _now() -> str:
    return datetime.utcnow().isoformat()


class Project(Base):
    __tablename__ = "projects"

    id: Mapped[str] = mapped_column(String, primary_key=True, default=_uuid)
    name: Mapped[str] = mapped_column(String, nullable=False)
    created_at: Mapped[str] = mapped_column(String, default=_now)
    languages: Mapped[str] = mapped_column(Text, default="[]")
    tone_profile: Mapped[str] = mapped_column(Text, default="{}")
    privacy_settings: Mapped[str] = mapped_column(Text, default="{}")

    assets: Mapped[list["Asset"]] = relationship(back_populates="project")


class Asset(Base):
    __tablename__ = "assets"

    id: Mapped[str] = mapped_column(String, primary_key=True, default=_uuid)
    project_id: Mapped[str] = mapped_column(String, ForeignKey("projects.id"))
    path: Mapped[str] = mapped_column(String, nullable=False)
    type: Mapped[str] = mapped_column(String, nullable=False)
    duration: Mapped[float] = mapped_column(Float, default=0.0)
    resolution: Mapped[str] = mapped_column(String, default="")
    metadata_json: Mapped[str] = mapped_column("metadata", Text, default="{}")
    quality_scores: Mapped[str] = mapped_column(Text, default="{}")
    tags: Mapped[str] = mapped_column(Text, default="[]")

    project: Mapped[Project] = relationship(back_populates="assets")


class ContentItem(Base):
    __tablename__ = "content_items"

    id: Mapped[str] = mapped_column(String, primary_key=True, default=_uuid)
    project_id: Mapped[str] = mapped_column(String, ForeignKey("projects.id"))
    concept_id: Mapped[str] = mapped_column(String, default="")
    format: Mapped[str] = mapped_column(String, default="reel")
    status: Mapped[str] = mapped_column(String, default="draft")
    captions: Mapped[str] = mapped_column(Text, default="{}")
    hashtags: Mapped[str] = mapped_column(Text, default="[]")
    on_screen_text: Mapped[str] = mapped_column(Text, default="{}")
    sound_id: Mapped[str] = mapped_column(String, default="")
    storyboard: Mapped[str] = mapped_column(Text, default="")
    compliance_notes: Mapped[str] = mapped_column(Text, default="")
    created_at: Mapped[str] = mapped_column(String, default=_now)


class Decision(Base):
    __tablename__ = "decisions"

    id: Mapped[str] = mapped_column(String, primary_key=True, default=_uuid)
    content_item_id: Mapped[str] = mapped_column(String, default="")
    agent: Mapped[str] = mapped_column(String, default="")
    decision: Mapped[str] = mapped_column(Text, default="")
    rationale: Mapped[str] = mapped_column(Text, default="")
    confidence: Mapped[float] = mapped_column(Float, default=0.0)
    created_at: Mapped[str] = mapped_column(String, default=_now)


class Export(Base):
    __tablename__ = "exports"

    id: Mapped[str] = mapped_column(String, primary_key=True, default=_uuid)
    content_item_id: Mapped[str] = mapped_column(String, default="")
    export_path: Mapped[str] = mapped_column(String, default="")
    format: Mapped[str] = mapped_column(String, default="instagram")
    specs: Mapped[str] = mapped_column(Text, default="{}")
    created_at: Mapped[str] = mapped_column(String, default=_now)
