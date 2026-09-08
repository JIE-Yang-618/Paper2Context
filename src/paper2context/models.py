from __future__ import annotations
from dataclasses import dataclass, field, asdict
from typing import Any

@dataclass
class Diagnostics:
    pages: int
    encrypted: bool
    text_layer: bool
    document_type: str
    layout: str
    metadata_available: bool
    ocr_required: bool
    confidence: dict[str, str] = field(default_factory=dict)

@dataclass
class Paragraph:
    text: str
    page_start: int
    page_end: int
    section: str | None = None

@dataclass
class Section:
    title: str
    level: int
    page_start: int
    page_end: int
    paragraphs: list[Paragraph] = field(default_factory=list)

@dataclass
class Reference:
    raw: str
    page: int
    year: int | None = None
    doi: str | None = None

@dataclass
class Asset:
    kind: str
    label: str
    caption: str
    page: int
    bbox: list[float] | None = None
    file: str | None = None

@dataclass
class Chunk:
    chunk_id: str
    section: str
    pages: list[int]
    text: str
    token_estimate: int

@dataclass
class PaperDocument:
    source_file: str
    source_sha256: str
    diagnostics: Diagnostics
    metadata: dict[str, Any]
    sections: list[Section]
    references: list[Reference]
    assets: list[Asset]
    chunks: list[Chunk]
    warnings: list[str] = field(default_factory=list)

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)
