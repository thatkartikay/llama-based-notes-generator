from __future__ import annotations

import re
from enum import Enum
from urllib.parse import parse_qs, urlparse


class SourceKind(str, Enum):
    TEXT = "text"
    YOUTUBE = "youtube"
    SYLLABUS = "syllabus"


def ingest_source(kind: SourceKind, value: str) -> str:
    cleaned = value.strip()
    if not cleaned:
        raise ValueError("Please provide source material.")

    if kind == SourceKind.TEXT:
        return cleaned
    if kind == SourceKind.SYLLABUS:
        return format_syllabus(cleaned)
    if kind == SourceKind.YOUTUBE:
        return fetch_youtube_transcript(cleaned)

    raise ValueError(f"Unsupported source kind: {kind}")


def format_syllabus(raw_topics: str) -> str:
    topics = [line.strip(" -\t") for line in raw_topics.splitlines() if line.strip()]
    if not topics:
        raise ValueError("Please enter at least one syllabus topic.")

    formatted = "\n".join(f"{index}. {topic}" for index, topic in enumerate(topics, start=1))
    return f"Syllabus topics:\n{formatted}"


def fetch_youtube_transcript(url_or_id: str) -> str:
    video_id = extract_youtube_id(url_or_id)
    if not video_id:
        raise ValueError("Could not find a valid YouTube video ID.")

    try:
        from youtube_transcript_api import YouTubeTranscriptApi
    except ImportError as exc:
        raise ValueError(
            "YouTube caption fetching needs the optional youtube-transcript-api package. "
            "Install it or paste the lecture transcript manually."
        ) from exc

    try:
        transcript = YouTubeTranscriptApi.get_transcript(video_id)
    except Exception as exc:
        raise ValueError(
            "Could not fetch captions for this YouTube video. "
            "Try a video with captions enabled or paste the lecture text manually."
        ) from exc

    lines = [entry.get("text", "").replace("\n", " ").strip() for entry in transcript]
    text = " ".join(line for line in lines if line)
    if not text:
        raise ValueError("The fetched transcript was empty.")
    return text


def extract_youtube_id(url_or_id: str) -> str | None:
    candidate = url_or_id.strip()
    if re.fullmatch(r"[A-Za-z0-9_-]{11}", candidate):
        return candidate

    parsed = urlparse(candidate)
    host = parsed.netloc.lower()
    if "youtu.be" in host:
        video_id = parsed.path.strip("/").split("/")[0]
        return video_id if re.fullmatch(r"[A-Za-z0-9_-]{11}", video_id) else None

    if "youtube.com" in host:
        query_id = parse_qs(parsed.query).get("v", [None])[0]
        if query_id and re.fullmatch(r"[A-Za-z0-9_-]{11}", query_id):
            return query_id

        match = re.search(r"/(?:embed|shorts)/([A-Za-z0-9_-]{11})", parsed.path)
        if match:
            return match.group(1)

    return None
