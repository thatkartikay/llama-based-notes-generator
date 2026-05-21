# Troubleshooting

## The browser shows script text instead of the app

You opened `run_app.ps1` or `run_app.bat` directly in the browser. Those files must be run in a terminal.

Use PowerShell:

```powershell
cd "path\to\llama-study-notes-generator"
.\run_app.ps1
```

Then open:

```text
http://127.0.0.1:8501
```

## `ollama` is not recognized

Ollama is not installed or the terminal was opened before installation completed.

Install Ollama, then open a new terminal:

https://ollama.com/download/OllamaSetup.exe

Check:

```powershell
ollama --version
```

## Could not connect to Ollama

Make sure Ollama is running and that the app's Ollama URL is:

```text
http://localhost:11434
```

Check Ollama from PowerShell:

```powershell
Invoke-WebRequest http://localhost:11434/api/tags
```

## Model not found

Pull the default model:

```powershell
ollama pull llama3.2:1b
```

## Generation is slow

Local generation speed depends on CPU, RAM, GPU, and model size. For faster results:

- Use `llama3.2:1b`
- Use fewer flashcards
- Start with shorter text
- Use syllabus topics instead of very long pasted lectures

## YouTube input does not work

YouTube captions need the optional `youtube-transcript-api` package:

```powershell
pip install youtube-transcript-api
```

If a video has no captions, paste the transcript manually.

## The PDF is too simple

The project intentionally uses a dependency-free PDF writer so it can run on a clean Python setup. For richer layouts, replace `study_notes/pdf.py` with a ReportLab renderer.
