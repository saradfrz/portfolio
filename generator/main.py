"""Build the portfolio into one HTML file; no web server or Node required."""
from datetime import date
import json
from pathlib import Path
from urllib.parse import quote, urlencode

from jinja2 import Environment, FileSystemLoader, StrictUndefined, select_autoescape

ROOT = Path(__file__).resolve().parent


def load_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def badge_url(name: str, tech: dict) -> str:
    """Escape the Shields.io badge label as in the original portfolio."""
    label = name.replace("-", "--").replace("_", "__").replace(" ", "_")
    params = urlencode({"style": "flat-square", "logo": tech["logo"],
                        "logoColor": tech.get("logoColor", "white")})
    return f"https://img.shields.io/badge/{quote(label, safe='')}-{tech['color']}?{params}"


def validate_projects(projects: dict) -> None:
    """Keep exactly three visible projects and validate card configuration."""
    groups = projects["groups"]
    if sum(len(group["items"]) for group in groups) != 4:
        raise ValueError("projects.json must contain exactly four projects in total.")
    for group in groups:
        if group["state"] not in {"featured", "wip", "planning"}:
            raise ValueError(f"Unknown project state: {group['state']}")
        if group["columns"] not in {1, 2}:
            raise ValueError("Project group columns must be 1 or 2.")
        for project in group["items"]:
            for field in ("title", "badge", "summary", "url", "linkText"):
                if not isinstance(project.get(field), str):
                    raise ValueError(f"Project {project.get('title', '?')}: missing or invalid {field}")


def build(root: Path = ROOT) -> Path:
    cfg = load_json(root / "data/site.json")
    projects = load_json(root / "data/projects.json")
    validate_projects(projects)
    env = Environment(
        loader=FileSystemLoader(root / "templates"),
        autoescape=select_autoescape(["html"]),
        undefined=StrictUndefined,
        trim_blocks=True,
        lstrip_blocks=True,
        keep_trailing_newline=True,
    )
    env.globals["badge_url"] = badge_url
    css = (root / "assets/style.css").read_text(encoding="utf-8")
    javascript = (root / "assets/script.js").read_text(encoding="utf-8")
    # These files are trusted source code. Reject raw closing tags that could
    # terminate the corresponding inline HTML elements prematurely.
    if "</style" in css.lower() or "</script" in javascript.lower():
        raise ValueError("CSS/JavaScript must not contain raw closing HTML tags.")
    html = env.get_template("index.html").render(
        cfg=cfg, projects=projects, css=css, javascript=javascript,
        year=date.today().year,
    )
    output = root / "output/index.html"
    output.write_text(html, encoding="utf-8")
    return output


if __name__ == "__main__":
    output = build()
    print(f"Generated {output} ({output.stat().st_size:,} bytes)")
