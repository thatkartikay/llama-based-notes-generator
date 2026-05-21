from __future__ import annotations

import html
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.parse import parse_qs

from study_notes.config import AppSettings, OllamaSettings
from study_notes.ingest import SourceKind
from study_notes.pipeline import StudyPackRequest, build_study_pack


HOST = "127.0.0.1"
PORT = 8501
OUTPUT_DIR = Path("outputs")


class StudyNotesHandler(BaseHTTPRequestHandler):
    def do_GET(self) -> None:
        if self.path.startswith("/outputs/"):
            self.serve_pdf()
            return
        self.send_html(render_form())

    def do_POST(self) -> None:
        if self.path != "/generate":
            self.send_error(404)
            return

        try:
            length = int(self.headers.get("Content-Length", "0"))
            data = parse_qs(self.rfile.read(length).decode("utf-8"))
            title = first(data, "title", "Study Notes")
            source_kind = SourceKind(first(data, "source_kind", "text"))
            source_value = first(data, "source_value", "")
            model = first(data, "model", "llama3.2:1b")
            ollama_url = first(data, "ollama_url", "http://localhost:11434")
            learner_level = first(data, "learner_level", "Intermediate")
            detail_level = first(data, "detail_level", "Highly detailed")
            flashcard_count = int(first(data, "flashcard_count", "30"))

            request = StudyPackRequest(
                title=title,
                source_kind=source_kind,
                source_value=source_value,
                learner_level=learner_level,
                detail_level=detail_level,
                flashcard_count=flashcard_count,
            )
            settings = AppSettings(ollama=OllamaSettings(model=model, base_url=ollama_url))
            OUTPUT_DIR.mkdir(exist_ok=True)
            filename = safe_filename(title) + "_study_pack.pdf"
            output_path = OUTPUT_DIR / filename
            build_study_pack(request, settings, output_path)

            self.send_html(render_success(filename))
        except Exception as exc:
            self.send_html(render_form(error=str(exc)))

    def serve_pdf(self) -> None:
        name = Path(self.path.removeprefix("/outputs/")).name
        path = OUTPUT_DIR / name
        if not path.exists():
            self.send_error(404)
            return

        data = path.read_bytes()
        self.send_response(200)
        self.send_header("Content-Type", "application/pdf")
        self.send_header("Content-Disposition", f'attachment; filename="{name}"')
        self.send_header("Content-Length", str(len(data)))
        self.end_headers()
        self.wfile.write(data)

    def send_html(self, body: str) -> None:
        data = body.encode("utf-8")
        self.send_response(200)
        self.send_header("Content-Type", "text/html; charset=utf-8")
        self.send_header("Content-Length", str(len(data)))
        self.end_headers()
        self.wfile.write(data)

    def log_message(self, format: str, *args: object) -> None:
        return


def first(data: dict[str, list[str]], key: str, default: str) -> str:
    return data.get(key, [default])[0].strip() or default


def safe_filename(value: str) -> str:
    chars = [char.lower() if char.isalnum() else "_" for char in value.strip()]
    return "".join(chars).strip("_") or "study_notes"


def render_form(error: str | None = None) -> str:
    error_html = f'<div class="error">{html.escape(error)}</div>' if error else ""
    return f"""<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>Llama Study Notes Generator</title>
  <style>
    :root {{ color-scheme: light; font-family: Arial, sans-serif; }}
    body {{ margin: 0; background: #f6f8fa; color: #172126; }}
    main {{ max-width: 980px; margin: 0 auto; padding: 32px 20px 56px; }}
    h1 {{ margin: 0 0 8px; font-size: 32px; }}
    p {{ color: #52616b; }}
    form {{ display: grid; gap: 18px; background: #fff; border: 1px solid #d9e1e5; border-radius: 8px; padding: 22px; }}
    label {{ display: grid; gap: 7px; font-weight: 700; }}
    input, select, textarea {{ font: inherit; border: 1px solid #c8d2d7; border-radius: 6px; padding: 10px; }}
    textarea {{ min-height: 260px; resize: vertical; }}
    .grid {{ display: grid; grid-template-columns: repeat(2, minmax(0, 1fr)); gap: 16px; }}
    button {{ justify-self: start; border: 0; border-radius: 6px; background: #1f6f8b; color: white; font-weight: 700; padding: 12px 18px; cursor: pointer; }}
    .error {{ background: #fff0f0; border: 1px solid #e7a2a2; color: #8a1f1f; padding: 12px; border-radius: 6px; }}
    @media (max-width: 720px) {{ .grid {{ grid-template-columns: 1fr; }} }}
  </style>
</head>
<body>
  <main>
    <h1>Llama Study Notes Generator</h1>
    <p>Create detailed notes, memory maps, glossary entries, exam tips, and flashcards as a downloadable PDF.</p>
    {error_html}
    <form method="post" action="/generate">
      <div class="grid">
        <label>PDF title <input name="title" value="Study Notes"></label>
        <label>Source type
          <select name="source_kind">
            <option value="text">Text</option>
            <option value="youtube">YouTube lecture</option>
            <option value="syllabus">Syllabus topics</option>
          </select>
        </label>
      </div>
      <label>Text, YouTube URL, or syllabus topics
        <textarea name="source_value" placeholder="Paste your text, a YouTube URL with captions, or syllabus topics here"></textarea>
      </label>
      <div class="grid">
        <label>Ollama model <input name="model" value="llama3.2:1b"></label>
        <label>Ollama URL <input name="ollama_url" value="http://localhost:11434"></label>
      </div>
      <div class="grid">
        <label>Learner level
          <select name="learner_level">
            <option>Beginner</option>
            <option selected>Intermediate</option>
            <option>Advanced</option>
          </select>
        </label>
        <label>Detail level
          <select name="detail_level">
            <option>Concise</option>
            <option>Detailed</option>
            <option selected>Highly detailed</option>
          </select>
        </label>
      </div>
      <label>Flashcards <input type="number" name="flashcard_count" value="30" min="5" max="100"></label>
      <button type="submit">Generate PDF</button>
    </form>
  </main>
</body>
</html>"""


def render_success(filename: str) -> str:
    escaped = html.escape(filename)
    return f"""<!doctype html>
<html lang="en">
<head><meta charset="utf-8"><title>Study Pack Ready</title></head>
<body style="font-family: Arial, sans-serif; max-width: 760px; margin: 48px auto;">
  <h1>Study pack ready</h1>
  <p>Your PDF was generated successfully.</p>
  <p><a href="/outputs/{escaped}">Download {escaped}</a></p>
  <p><a href="/">Create another</a></p>
</body>
</html>"""


def main() -> None:
    server = ThreadingHTTPServer((HOST, PORT), StudyNotesHandler)
    url = f"http://{HOST}:{PORT}"
    print(f"Running at {url}")
    server.serve_forever()


if __name__ == "__main__":
    main()
