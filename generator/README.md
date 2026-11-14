# Portfolio static site generator

A small Python/Jinja2 project that generates a single `index.html` from the portfolio's HTML template, CSS, JavaScript and JSON content. The generated document contains the complete markup, inline stylesheet and inline script. It can be opened locally or deployed to GitHub Pages without a Python backend.

## Structure

```text
portfolio/
├── main.py                  # Static build entry point
├── requirements.txt         # Jinja2 dependency
├── README.md
├── data/
│   ├── site.json            # Identity, experience, highlights, skills, links
│   └── projects.json        # Exactly three portfolio projects
├── templates/
│   └── index.html           # Jinja2 HTML template
├── assets/
│   ├── style.css            # Original portfolio design and animations
│   └── script.js            # Typing animation and badge fallbacks
├── tests/
│   └── test_build.py
└── index.html               # Generated; do not edit manually
```

## Local setup (Windows PowerShell)

Run from the extracted `portfolio` directory with Python 3.10 or later:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
python main.py
Start-Process index.html
```

On macOS/Linux:

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
python main.py
```

Open the generated `index.html` in a browser. No local server is necessary. For an HTTP preview, optionally run `python -m http.server 8000` and visit `http://localhost:8000`.

## Edit the content

- `data/site.json`: edit identity, cover/profile image URLs, links, experience, skills and work highlights.
- `data/projects.json`: edit the project cards and status groups. The generator validates that the total number of cards is exactly three. The initial three are Key To Cart, Data Forge and TickStream Lakehouse, copied from the original page. RepoSensei was excluded to satisfy the three-project limit.
- `templates/index.html`: edit section structure or reusable Jinja2 macros.
- `assets/style.css`: adjust design tokens, responsive layout and styling.
- `assets/script.js`: adjust the hero typing animation, year display or badge fallback.

Project groups use `featured`, `wip` or `planning` as their `state`. `columns` can be `1` or `2`. Each project has `title`, `badge`, `summary`, `url` and `linkText`; optional fields include `details`, `flow`, `tags` and `metric` (an object with `value` and `label`). An empty URL shows an inactive link label. To move a project to a different status, move its JSON object to the appropriate group's `items` array. The `badge` text is editable independently.

After editing any source file, run:

```bash
python main.py
```

Python reads the JSON, validates the project count, renders the complete page with Jinja2 and embeds the stylesheet and JavaScript into the output. The page content is visible without JavaScript; JS adds the typing animation, dynamic year and fallback chips for failed badge images. Reduced-motion preferences are respected.

## Deploy to GitHub Pages

1. Commit the project, including the generated root `index.html`, to your repository.
2. In GitHub repository settings, enable Pages and choose **Deploy from a branch**, then your publishing branch and `/ (root)`.
3. After each source change, regenerate `index.html` and commit/push the updated output.

Only the generated `index.html` needs to be published. It does not fetch the JSON, CSS or JS at runtime.

**External assets:** like the original portfolio, the generated page references Google Fonts, Supabase-hosted profile/cover images, and Shields.io badges. These require internet access for their full appearance. No separate local asset files are needed. This is a single-file deployment, not a fully offline snapshot. External links are also preserved.

## Tests

```bash
python -m unittest discover -s tests -v
```

The tests verify the three-card limit, unique HTML IDs, inline CSS and JavaScript, and static project rendering.
