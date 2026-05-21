# Contributing

Thanks for improving Llama Study Notes Generator.

## Local Setup

Install Ollama and pull the default model:

```powershell
ollama pull llama3.2:1b
```

Run the app:

```powershell
.\run_app.ps1
```

## Development Checks

Compile all Python files:

```powershell
.\.venv\Scripts\python.exe -m py_compile app.py study_notes\config.py study_notes\ingest.py study_notes\llm.py study_notes\pdf.py study_notes\pipeline.py study_notes\prompts.py
```

## Good First Improvements

- Add automated tests
- Add a richer ReportLab PDF renderer as an optional mode
- Add Whisper transcription for videos without captions
- Add chunking for very long lectures
- Add Anki export for flashcards
- Add model presets for quality and speed

