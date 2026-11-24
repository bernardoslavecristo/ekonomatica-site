"""Check local resources, anchors and JavaScript embedded in all public HTML."""
from html.parser import HTMLParser
from pathlib import Path
import subprocess
import tempfile
from urllib.parse import unquote, urlsplit


class Page(HTMLParser):
    def __init__(self, text):
        super().__init__()
        self.links, self.ids, self.scripts = [], set(), []
        self.capture, self.parts = False, []
        self.feed(text)

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if 'id' in attrs:
            self.ids.add(attrs['id'])
        self.links.extend(attrs[k] for k in ('href', 'src', 'poster') if k in attrs)
        if tag == 'script' and 'src' not in attrs and attrs.get('type') != 'application/ld+json':
            self.capture, self.parts = True, []

    def handle_data(self, data):
        if self.capture:
            self.parts.append(data)

    def handle_endtag(self, tag):
        if tag == 'script' and self.capture:
            self.scripts.append(''.join(self.parts))
            self.capture = False


pages = {p.name: Page(p.read_text()) for p in Path('.').glob('*.html')}
errors = []
for name, page in pages.items():
    for link in page.links:
        url = urlsplit(link)
        if url.scheme or url.netloc:
            continue
        target = unquote(url.path).lstrip('/') or (name if url.fragment else 'index.html')
        if target == './':
            target = 'index.html'
        if not Path(target).exists():
            errors.append(f'{name}: arquivo ausente {link}')
        elif url.fragment and target in pages and url.fragment not in pages[target].ids:
            errors.append(f'{name}: âncora ausente {link}')
    for script in page.scripts:
        with tempfile.NamedTemporaryFile(mode='w', suffix='.js') as file:
            file.write(script)
            file.flush()
            result = subprocess.run(['node', '--check', file.name], capture_output=True, text=True)
            if result.returncode:
                errors.append(f'{name}: {result.stderr}')
for path in Path('.').glob('*.js'):
    result = subprocess.run(['node', '--check', str(path)], capture_output=True, text=True)
    if result.returncode:
        errors.append(f'{path}: {result.stderr}')
print('\n'.join(errors) if errors else f'OK: {len(pages)} páginas, recursos, âncoras e JavaScript.')
raise SystemExit(bool(errors))
