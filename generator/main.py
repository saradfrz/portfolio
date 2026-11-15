"""Build the portfolio into one HTML file; no web server or Node required."""
from datetime import date
import json
from pathlib import Path
from urllib.parse import quote, urlencode, urlsplit

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
    """Keep exactly four visible projects and validate card configuration."""
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



def load_posts(root: Path) -> dict:
    """Load portfolio link metadata only; articles are managed separately."""
    config = load_json(root / "data/posts.json")
    limit = config.get("limit", 3)
    if type(limit) is not int or limit < 1:
        raise ValueError("posts.json limit must be a positive integer.")
    published = []
    for post in config["items"]:
        if post.get("draft", False):
            continue
        for field in ("title", "summary", "date", "url"):
            if not isinstance(post.get(field), str) or not post[field].strip():
                raise ValueError(f"Post requires a nonempty {field}.")
        published_date = date.fromisoformat(post["date"])
        url = post["url"]
        if any(c.isspace() for c in url) or "\\" in url:
            raise ValueError("Post URL must not contain whitespace or backslashes.")
        parts = urlsplit(url)
        if parts.scheme and parts.scheme.lower() not in {"http", "https"}:
            raise ValueError("Post URL must be HTTP(S) or a relative path.")
        if parts.scheme and not parts.netloc:
            raise ValueError("Absolute post URL requires a hostname.")
        published.append(dict(post, date_label=published_date.strftime("%b %d, %Y")))
    config["items"] = sorted(published, key=lambda p: p["date"], reverse=True)[:limit]
    return config


def build(root: Path = ROOT) -> Path:
    cfg = load_json(root / "data/site.json")
    projects = load_json(root / "data/projects.json")
    validate_projects(projects)
    posts = load_posts(root)
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
        cfg=cfg, projects=projects, posts=posts, css=css, javascript=javascript,
        year=date.today().year,
    )
    output_name = cfg["site"].get("output_file", "index.html")
    if (not isinstance(output_name, str) or "/" in output_name or "\\" in output_name
            or not output_name.lower().endswith(".html")):
        raise ValueError("site.output_file must be an HTML filename, e.g. portfolio.html.")
    output = root / "output" / output_name
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(html, encoding="utf-8")
    return output


if __name__ == "__main__":
    output = build()
    print(f"Generated {output} ({output.stat().st_size:,} bytes)")
