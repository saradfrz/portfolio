# Portfolio generator with latest posts

The About section now displays article cards in place of the facts list.
The existing portfolio content and project cards are preserved.

## Build (Windows PowerShell)

Run inside the extracted `generator` folder:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
python main.py
Start-Process output/index.html
```

On Linux/macOS, activate using `source .venv/bin/activate`.
Python 3.10+ is required.

## Add an article

1. Create `posts/my-post/`.
2. Put the article's HTML in `posts/my-post/index.html` and its images or other
   resources inside that folder (for example `assets/cover.png`).
3. Add an item to `posts/posts.json`:

```json
{
  "title": "My new article",
  "date": "2026-11-16",
  "summary": "A short description for the card.",
  "path": "my-post/index.html",
  "draft": false
}
```

4. Run `python main.py` again.

The JSON file's `title` sets the section heading; `limit` controls the
maximum visible cards (default 3). Cards are ordered newest first.
Use ISO dates (`YYYY-MM-DD`); the included article uses November 15, 2026.
Edit that date if its actual publication date differs.

`draft: true` hides a card, but files are still copied into the public output.
Keep private drafts outside `posts/`. Future dates do not schedule publishing.
Paths are relative to `posts/`. Published entries must point to existing HTML.
The generator does not convert Markdown or write article content.

Included: your existing Data Pipeline Engineering article and its cover from
the data-pipeline-blog package. Replace those files with a newer article export
whenever you revise the article.

## Deploy to GitHub Pages

The ZIP's root `index.html` and root `posts/` are ready to copy to the
publishing root of your portfolio repository, beside each other.

For subsequent builds, copy **the contents of `generator/output/`** into that
same publishing root. Commit and push both `index.html` and `posts/`.
Each post then lives at `https://<user>.github.io/<repo>/posts/<slug>/`.
Relative links support a GitHub Pages repository subdirectory.

Do not publish only index.html: article pages and their assets are separate files.
Do not manually edit output/: the next build replaces its generated posts folder.
Regenerate after changing metadata or adding articles; there is no runtime JSON fetch.
The Python environment is local only and is not included in the ZIP.

## Other source files

- `data/site.json`: profile, About, experience, highlights, skills and links.
  The old `facts` data is retained but no longer rendered.
- `data/projects.json`: four portfolio projects.
- `templates/index.html`: portfolio markup and post card structure.
- `assets/style.css`: portfolio and post card styling.
- `assets/script.js`: existing animations.
- `posts/`: article metadata, pages and their assets.
- `output/`: generated site ready for deployment.

The portfolio still uses its existing external fonts, badges and profile images.

## Checks

```powershell
python -m unittest discover -s tests -v
```
