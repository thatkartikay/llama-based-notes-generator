# Quickstart

This guide gets the app running locally with Ollama and a small Llama model.

## 1. Install Ollama

Download and install Ollama for Windows:

https://ollama.com/download/OllamaSetup.exe

After installation, open a new terminal and confirm Ollama is available:

```powershell
ollama --version
```

## 2. Pull a Model

The app defaults to `llama3.2:1b`, which is small and practical for first-time local use:

```powershell
ollama pull llama3.2:1b
```

For better notes, try a larger model if your computer can handle it:

```powershell
ollama pull llama3.1:8b
```

Then enter `llama3.1:8b` in the app's model field.

## 3. Run the App

From the project folder:

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

## 4. Generate a PDF

Start with a small syllabus test:

```text
Photosynthesis basics
Chlorophyll
Light-dependent reactions
Calvin cycle
```

Choose `Syllabus topics`, click `Generate PDF`, and wait for the download link.

