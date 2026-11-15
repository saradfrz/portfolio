# Portfolio generator

Generates your portfolio with Latest posts cards beside About.
Articles are generated and published in your separate repository.
This project only renders links: it does not generate, copy or require article files.

## Setup and build

Inside generator/ (Windows PowerShell):

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
python main.py
Start-Process output/index.html
```

On Linux/macOS use `source .venv/bin/activate`. Requires Python 3.10+.

## Add a portfolio post entry

Edit `data/posts.json`:

```json
{
  "title": "Latest posts",
  "limit": 3,
  "items": [
    {
      "title": "My article",
      "date": "2026-11-15",
      "summary": "A short description.",
      "url": "https://saradfrz.github.io/YOUR-POSTS-REPO/my-article.html",
      "draft": false
    }
  ]
}
```

Replace the example URL with the actual published page URL.
Any HTML filename is supported. The link is used exactly as configured.
Use the GitHub Pages URL to open the rendered article, rather than a GitHub source-file URL.
Relative paths such as `posts/my-article.html` also work if you publish those files
separately at that location.

The included Data Pipeline Engineering entry retains the previous relative URL.
**Set its url to the actual address from your posts repository before publishing.**
No article files are bundled, and the generator does not check remote availability.

Cards sort by date, newest first. `limit` controls the visible count.
`draft: true` hides an entry. Dates use YYYY-MM-DD and do not schedule publication.
Rebuild after editing JSON.

## Customize the portfolio HTML filename

In `data/site.json`, under `site`, edit:

```json
"output_file": "portfolio.html"
```

The default is `index.html`. Output is written to `output/<output_file>`.
This changes the portfolio filename only. Article filenames are managed in
your other repository; update each card's URL to match.
Old generated HTML files are not deleted when changing output_file.

## Publish

Copy the generated HTML from `generator/output/` to your portfolio repository's
publishing directory, commit and push. The ZIP includes a ready-built root index.html.
Only the portfolio HTML is needed here; articles stay in your other repository.
Use index.html for the default landing page, or visit /portfolio.html when using that filename.

## Source files

- data/site.json: profile and portfolio content, plus output filename.
- data/projects.json: four existing project cards.
- data/posts.json: post card metadata and links.
- templates/index.html: markup.
- assets/style.css: styling.
- assets/script.js: existing animations.

Legacy facts data is retained in site.json but no longer rendered.
External fonts, badges and profile images remain as in the original portfolio.

## Checks

```powershell
python -m unittest discover -s tests -v
```
