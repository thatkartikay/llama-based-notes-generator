from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

from study_notes.config import AppSettings
from study_notes.ingest import SourceKind, ingest_source
from study_notes.llm import OllamaClient, parse_json_response
from study_notes.pdf import StudyPack, render_pdf, study_pack_from_dict
from study_notes.prompts import build_study_prompt


@dataclass
class StudyPackRequest:
    title: str
    source_kind: SourceKind
    source_value: str
    learner_level: str = "Intermediate"
    detail_level: str = "Highly detailed"
    flashcard_count: int = 30


def build_study_pack(request: StudyPackRequest, settings: AppSettings, output_path: Path) -> StudyPack:
    if request.flashcard_count < 5 or request.flashcard_count > 100:
        raise ValueError("Flashcard count must be between 5 and 100.")

    source_text = ingest_source(request.source_kind, request.source_value)
    prompt = build_study_prompt(
        title=request.title,
        source_text=source_text,
        learner_level=request.learner_level,
        detail_level=request.detail_level,
        flashcard_count=request.flashcard_count,
    )

    llm = OllamaClient(settings.ollama)
    raw_response = llm.complete(prompt)
    data = parse_json_response(raw_response)
    study_pack = study_pack_from_dict(data)
    render_pdf(study_pack, output_path)
    return study_pack

