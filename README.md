# Llama Study Notes Generator

Turn text, YouTube lecture transcripts, or syllabus topics into a downloadable PDF study pack powered by a local Llama model through Ollama.

The generated PDF includes:

- Detailed study notes
- Memory map branches
- Flashcards
- Glossary terms
- Exam tips

The app is intentionally dependency-light. The core web app and PDF generator use only the Python standard library. Ollama supplies the local Llama model.

## Demo Workflow

1. Open the local app.
2. Paste text, a captioned YouTube URL, or syllabus topics.
3. Choose learner level, detail level, flashcard count, and Ollama model.
4. Generate and download a PDF study pack.

## Requirements

- Windows, macOS, or Linux
- Python 3.10+
- Ollama
- A pulled Ollama model, such as `llama3.2:1b`

Optional:

- `youtube-transcript-api` for YouTube caption fetching

## Quickstart

Install Ollama:

https://ollama.com

Pull the default model:

```powershell
ollama pull llama3.2:1b
```

Run the app from the project folder:

```powershell
.\run_app.ps1
```

Or:

```cmd
run_app.bat
```

Open:

```text
http://127.0.0.1:8501
```

For a more detailed setup, see [docs/QUICKSTART.md](docs/QUICKSTART.md).

## Input Modes

### Text

Paste notes, article content, textbook passages, or lecture transcripts.

### Syllabus Topics

Enter one topic per line. This works well for generating structured revision notes.

### YouTube Lecture

Paste a YouTube URL. Caption fetching requires the optional package:

```powershell
pip install youtube-transcript-api
```

If captions are unavailable, paste the transcript manually in text mode.

## Project Structure

```text
app.py                  Local web app
requirements.txt        Optional dependency notes
run_app.bat             Windows Command Prompt launcher
run_app.ps1             PowerShell launcher
study_notes/
  config.py             App settings
  ingest.py             Text, syllabus, and YouTube ingestion
  llm.py                Ollama client
  pdf.py                Built-in PDF renderer
  pipeline.py           End-to-end generation flow
  prompts.py            Study-pack prompt template
docs/
  ARCHITECTURE.md       Internal flow and module guide
  QUICKSTART.md         Setup guide
  TROUBLESHOOTING.md    Common fixes
```

## Development

Compile check:

```powershell
.\.venv\Scripts\python.exe -m py_compile app.py study_notes\config.py study_notes\ingest.py study_notes\llm.py study_notes\pdf.py study_notes\pipeline.py study_notes\prompts.py
```

## Limitations

- The built-in PDF writer is simple by design.
- Very long lectures should be summarized in chunks in a future version.
- YouTube audio transcription is not included yet.
- Small models like `llama3.2:1b` are fast, but larger models usually produce better notes.

## License

MIT License. See [LICENSE](LICENSE).

