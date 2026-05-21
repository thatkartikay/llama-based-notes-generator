from __future__ import annotations


def build_study_prompt(
    title: str,
    source_text: str,
    learner_level: str,
    detail_level: str,
    flashcard_count: int,
) -> str:
    return f"""
You are an expert teacher, exam coach, and curriculum designer.

Create a complete study pack from the source material.

Audience level: {learner_level}
Detail level: {detail_level}
Requested flashcards: {flashcard_count}
Title: {title}

Return only valid JSON with this exact structure:
{{
  "title": "string",
  "summary": "short overview",
  "study_notes": [
    {{
      "heading": "section heading",
      "explanation": "detailed teaching explanation",
      "key_points": ["point"],
      "examples": ["example"],
      "common_confusions": ["confusion and correction"]
    }}
  ],
  "memory_map": {{
    "central_topic": "string",
    "branches": [
      {{
        "label": "branch name",
        "children": ["child idea"]
      }}
    ]
  }},
  "flashcards": [
    {{
      "question": "active recall question",
      "answer": "clear answer",
      "difficulty": "Easy|Medium|Hard"
    }}
  ],
  "exam_tips": ["tip"],
  "glossary": [
    {{
      "term": "term",
      "definition": "definition"
    }}
  ]
}}

Rules:
- Make the notes highly teachable, structured, and accurate.
- Prefer concrete explanations over vague summaries.
- Include examples where the source implies a process, formula, concept, or application.
- Flashcards should test understanding, definitions, comparison, cause/effect, and application.
- Do not invent facts that conflict with the source. If something is missing, say so cautiously.
- Return exactly {flashcard_count} flashcards unless the source is too short.

Source material:
\"\"\"
{source_text[:30000]}
\"\"\"
""".strip()

