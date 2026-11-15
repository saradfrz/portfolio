import json
from html import unescape
import sys
import tempfile
import shutil
import unittest
from html.parser import HTMLParser
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from main import build, validate_projects


class PageParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.ids = []
        self.project_cards = 0
        self.external_scripts = []
        self.styles = 0

    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        if 'id' in a:
            self.ids.append(a['id'])
        if tag == 'article' and set(a.get('class', '').split()) & {'featured', 'wip', 'planning'}:
            self.project_cards += 1
        if tag == 'script' and 'src' in a:
            self.external_scripts.append(a['src'])
        if tag == 'style':
            self.styles += 1


class BuildTests(unittest.TestCase):
    def test_build(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            for folder in ('data', 'templates', 'assets'):
                shutil.copytree(ROOT / folder, root / folder)
            output = build(root)
            html = output.read_text(encoding='utf-8')
            parser = PageParser()
            parser.feed(html)
            self.assertEqual(parser.project_cards, 4)
            self.assertEqual(len(parser.ids), len(set(parser.ids)))
            self.assertEqual(parser.external_scripts, [])
            self.assertEqual(parser.styles, 1)
            self.assertIn((root / 'assets/style.css').read_text(encoding='utf-8'), html)
            self.assertIn((root / 'assets/script.js').read_text(encoding='utf-8'), html)
            projects = json.loads((root / 'data/projects.json').read_text(encoding='utf-8'))
            for group in projects['groups']:
                for project in group['items']:
                    self.assertIn(project['title'], unescape(html))
            self.assertNotIn('id="facts"', html)
            self.assertIn('href="posts/data-pipeline-engineering/index.html"', html)
            self.assertFalse((output.parent / 'posts').exists())
            self.assertNotIn('RepoSensei', html)

    def test_custom_link_and_output_filename(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            for folder in ('data', 'templates', 'assets'):
                shutil.copytree(ROOT / folder, root / folder)
            config_path = root / 'data/site.json'
            config = json.loads(config_path.read_text())
            config['site']['output_file'] = 'portfolio.html'
            config_path.write_text(json.dumps(config))
            posts_path = root / 'data/posts.json'
            posts = json.loads(posts_path.read_text())
            posts['items'][0]['url'] = 'https://example.com/blog/my-custom-article.html'
            posts_path.write_text(json.dumps(posts))
            output = build(root)
            self.assertEqual(output.name, 'portfolio.html')
            self.assertIn('href="https://example.com/blog/my-custom-article.html"',
                          output.read_text())
            self.assertFalse((output.parent / 'posts').exists())

    def test_project_count_validation(self):
        projects = json.loads((ROOT / 'data/projects.json').read_text(encoding='utf-8'))
        projects['groups'][0]['items'].clear()
        with self.assertRaisesRegex(ValueError, 'exactly four'):
            validate_projects(projects)


if __name__ == '__main__':
    unittest.main()
