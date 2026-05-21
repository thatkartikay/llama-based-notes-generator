from __future__ import annotations

import textwrap
from dataclasses import dataclass, field
from pathlib import Path


@dataclass
class StudyNoteSection:
    heading: str
    explanation: str
    key_points: list[str] = field(default_factory=list)
    examples: list[str] = field(default_factory=list)
    common_confusions: list[str] = field(default_factory=list)


@dataclass
class MemoryBranch:
    label: str
    children: list[str] = field(default_factory=list)


@dataclass
class MemoryMap:
    central_topic: str
    branches: list[MemoryBranch] = field(default_factory=list)


@dataclass
class Flashcard:
    question: str
    answer: str
    difficulty: str = "Medium"


@dataclass
class GlossaryItem:
    term: str
    definition: str


@dataclass
class StudyPack:
    title: str
    summary: str
    study_notes: list[StudyNoteSection]
    memory_map: MemoryMap
    flashcards: list[Flashcard]
    exam_tips: list[str]
    glossary: list[GlossaryItem]


def study_pack_from_dict(data: dict) -> StudyPack:
    memory_map = data.get("memory_map") or {}
    return StudyPack(
        title=str(data.get("title") or "Study Notes"),
        summary=str(data.get("summary") or ""),
        study_notes=[
            StudyNoteSection(
                heading=str(item.get("heading") or "Section"),
                explanation=str(item.get("explanation") or ""),
                key_points=list_of_strings(item.get("key_points")),
                examples=list_of_strings(item.get("examples")),
                common_confusions=list_of_strings(item.get("common_confusions")),
            )
            for item in ensure_list(data.get("study_notes"))
        ],
        memory_map=MemoryMap(
            central_topic=str(memory_map.get("central_topic") or data.get("title") or "Central topic"),
            branches=[
                MemoryBranch(
                    label=str(branch.get("label") or "Branch"),
                    children=list_of_strings(branch.get("children")),
                )
                for branch in ensure_list(memory_map.get("branches"))
            ],
        ),
        flashcards=[
            Flashcard(
                question=str(card.get("question") or ""),
                answer=str(card.get("answer") or ""),
                difficulty=str(card.get("difficulty") or "Medium"),
            )
            for card in ensure_list(data.get("flashcards"))
        ],
        exam_tips=list_of_strings(data.get("exam_tips")),
        glossary=[
            GlossaryItem(term=str(item.get("term") or ""), definition=str(item.get("definition") or ""))
            for item in ensure_list(data.get("glossary"))
        ],
    )


def ensure_list(value: object) -> list:
    return value if isinstance(value, list) else []


def list_of_strings(value: object) -> list[str]:
    return [str(item) for item in ensure_list(value)]


def render_pdf(pack: StudyPack, output_path: Path) -> None:
    output_path.parent.mkdir(parents=True, exist_ok=True)
    writer = SimplePdfWriter(title=pack.title)

    writer.h1(pack.title)
    writer.p(pack.summary)
    writer.h1("Study Notes")
    for section in pack.study_notes:
        writer.h2(section.heading)
        writer.p(section.explanation)
        writer.bullets("Key points", section.key_points)
        writer.bullets("Examples", section.examples)
        writer.bullets("Common confusions", section.common_confusions)

    writer.h1("Memory Map")
    writer.h2(pack.memory_map.central_topic)
    for branch in pack.memory_map.branches:
        writer.h2(branch.label)
        writer.bullet_items(branch.children)

    if pack.glossary:
        writer.h1("Glossary")
        for item in pack.glossary:
            writer.h2(item.term)
            writer.p(item.definition)

    writer.h1("Flashcards")
    for index, card in enumerate(pack.flashcards, start=1):
        writer.h2(f"{index}. {card.question}")
        writer.p(f"Answer: {card.answer}")
        writer.p(f"Difficulty: {card.difficulty}")

    if pack.exam_tips:
        writer.h1("Exam Tips")
        writer.bullet_items(pack.exam_tips)

    output_path.write_bytes(writer.build())


class SimplePdfWriter:
    def __init__(self, title: str):
        self.title = title
        self.pages: list[list[str]] = [[]]
        self.y = 780

    def h1(self, text: str) -> None:
        self.add_gap(10)
        self.add_line(text, size=20, bold=True)
        self.add_gap(8)

    def h2(self, text: str) -> None:
        self.add_gap(7)
        self.add_line(text, size=13, bold=True)
        self.add_gap(3)

    def p(self, text: str) -> None:
        for paragraph in str(text).splitlines() or [""]:
            for line in textwrap.wrap(paragraph, width=92) or [""]:
                self.add_line(line, size=10)
        self.add_gap(5)

    def bullets(self, title: str, items: list[str]) -> None:
        if not items:
            return
        self.h2(title)
        self.bullet_items(items)

    def bullet_items(self, items: list[str]) -> None:
        for item in items:
            wrapped = textwrap.wrap(str(item), width=86) or [""]
            self.add_line(f"- {wrapped[0]}", size=10)
            for continuation in wrapped[1:]:
                self.add_line(f"  {continuation}", size=10)
        self.add_gap(4)

    def add_gap(self, amount: int) -> None:
        self.y -= amount
        if self.y < 60:
            self.new_page()

    def add_line(self, text: str, size: int = 10, bold: bool = False) -> None:
        if self.y < 60:
            self.new_page()
        font = "F2" if bold else "F1"
        escaped = escape_pdf_text(text)
        self.pages[-1].append(f"BT /{font} {size} Tf 50 {self.y} Td ({escaped}) Tj ET")
        self.y -= int(size * 1.45)

    def new_page(self) -> None:
        self.pages.append([])
        self.y = 780

    def build(self) -> bytes:
        objects: list[bytes] = []
        page_ids = []

        def add_object(content: bytes) -> int:
            objects.append(content)
            return len(objects)

        catalog_id = add_object(b"")
        pages_id = add_object(b"")
        font_regular_id = add_object(b"<< /Type /Font /Subtype /Type1 /BaseFont /Helvetica >>")
        font_bold_id = add_object(b"<< /Type /Font /Subtype /Type1 /BaseFont /Helvetica-Bold >>")

        for page in self.pages:
            stream = "\n".join(page).encode("latin-1", errors="replace")
            content_id = add_object(b"<< /Length " + str(len(stream)).encode() + b" >>\nstream\n" + stream + b"\nendstream")
            page_id = add_object(
                (
                    f"<< /Type /Page /Parent {pages_id} 0 R /MediaBox [0 0 595 842] "
                    f"/Resources << /Font << /F1 {font_regular_id} 0 R /F2 {font_bold_id} 0 R >> >> "
                    f"/Contents {content_id} 0 R >>"
                ).encode()
            )
            page_ids.append(page_id)

        kids = " ".join(f"{page_id} 0 R" for page_id in page_ids)
        objects[catalog_id - 1] = f"<< /Type /Catalog /Pages {pages_id} 0 R >>".encode()
        objects[pages_id - 1] = f"<< /Type /Pages /Kids [{kids}] /Count {len(page_ids)} >>".encode()

        output = bytearray(b"%PDF-1.4\n")
        offsets = [0]
        for index, content in enumerate(objects, start=1):
            offsets.append(len(output))
            output.extend(f"{index} 0 obj\n".encode())
            output.extend(content)
            output.extend(b"\nendobj\n")

        xref_offset = len(output)
        output.extend(f"xref\n0 {len(objects) + 1}\n".encode())
        output.extend(b"0000000000 65535 f \n")
        for offset in offsets[1:]:
            output.extend(f"{offset:010d} 00000 n \n".encode())
        output.extend(
            (
                "trailer\n"
                f"<< /Size {len(objects) + 1} /Root {catalog_id} 0 R >>\n"
                "startxref\n"
                f"{xref_offset}\n"
                "%%EOF\n"
            ).encode()
        )
        return bytes(output)


def escape_pdf_text(value: str) -> str:
    return str(value).replace("\\", "\\\\").replace("(", "\\(").replace(")", "\\)")

