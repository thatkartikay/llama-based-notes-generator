# Architecture

The project is intentionally small and dependency-light.

## Flow

```text
User input
  -> app.py web form
  -> study_notes.ingest
  -> study_notes.prompts
  -> study_notes.llm Ollama API call
  -> study_notes.pipeline
  -> study_notes.pdf
  -> downloadable PDF
```

## Main Modules

### `app.py`

Runs a local web server with Python's standard library. It renders the form, accepts submissions, calls the generation pipeline, and serves generated PDFs from `outputs/`.

### `study_notes/ingest.py`

Normalizes input from:

- Raw text
- Syllabus topics
- YouTube URLs, when the optional transcript package is installed

### `study_notes/prompts.py`

Builds the structured prompt sent to Ollama. The prompt asks the model to return JSON with notes, memory map branches, flashcards, exam tips, and glossary terms.

### `study_notes/llm.py`

Calls the local Ollama HTTP API at `http://localhost:11434/api/generate`.

### `study_notes/pipeline.py`

Coordinates the end-to-end workflow.

### `study_notes/pdf.py`

Converts the generated study pack into a PDF using a minimal built-in PDF writer.

## Why No Required Dependencies?

This project originally used Streamlit, Pydantic, Requests, and ReportLab. It was simplified to standard-library Python so first-time users can run it even when dependency installation is unreliable.

