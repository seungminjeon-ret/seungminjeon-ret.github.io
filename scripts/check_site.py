"""Reject unexpected public files and broken internal links before deployment."""
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import urlsplit, unquote
import re

ROOT = Path(__file__).resolve().parents[1]
SITE = ROOT / 'site'
ALLOWED = {
    'index.html', 'assets/style.css', 'assets/favicon.svg', 'assets/social.png',
}


class Page(HTMLParser):
    def __init__(self):
        super().__init__()
        self.ids = set()
        self.urls = []
        self.downloads = []
        self.headings = 0

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if 'id' in attrs:
            assert attrs['id'] not in self.ids, 'Duplicate ID'
            self.ids.add(attrs['id'])
        assert tag not in {'script', 'iframe', 'form'}, 'Unexpected active content'
        if tag == 'h1':
            self.headings += 1
        if 'href' in attrs:
            self.urls.append(attrs['href'])
        if 'src' in attrs:
            self.urls.append(attrs['src'])
        if 'download' in attrs:
            self.downloads.append(attrs['href'])


def main():
    paths = list(SITE.rglob('*'))
    assert not any(p.is_symlink() for p in paths), 'No symlinks allowed in public artifact'
    actual = {p.relative_to(SITE).as_posix() for p in paths if p.is_file()}
    assert actual == ALLOWED, f'Unexpected/missing public files: {actual ^ ALLOWED}'
    html = (SITE / 'index.html').read_text()
    page = Page()
    page.feed(html)
    assert page.headings == 1
    assert not page.downloads, 'Personal document downloads are not published'
    for url in page.urls:
        parts = urlsplit(url)
        if parts.scheme:
            assert parts.scheme in {'https', 'mailto'}, f'Unexpected URL scheme: {url}'
            continue
        if parts.path:
            dest = (SITE / unquote(parts.path)).resolve()
            assert SITE in dest.parents and dest.is_file(), f'Missing local file: {url}'
        if parts.fragment:
            assert parts.fragment in page.ids, f'Missing anchor: {url}'
    assert 'tel:' not in html.lower()
    assert not re.search(r'(?:\+?82[- .]?)?0?10[- .]?\d{4}[- .]?\d{4}', html), 'Phone number in HTML'
    print('PASS: exactly 4 public files; internal links, anchors, and static HTML valid; no personal document downloads.')


if __name__ == '__main__':
    main()
