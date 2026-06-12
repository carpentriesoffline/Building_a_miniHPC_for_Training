#!/usr/bin/env python3
"""Generate _data/toc.yml from H1/H2 headings in markdown content files."""

import re
import yaml
from pathlib import Path

ROOT = Path(__file__).parent.parent


def slugify(text):
    """Match kramdown's anchor generation."""
    text = text.lower().strip()
    text = re.sub(r'[^\w\s-]', '', text)
    text = re.sub(r'[\s]+', '-', text)
    return text.strip('-')


def extract_headings(md_path):
    """Extract H1/H2 headings from markdown, skipping code blocks."""
    headings = []
    in_code_block = False

    with open(md_path) as f:
        for line in f:
            # Toggle code block state on fenced code delimiters (up to 3 spaces indent allowed)
            if re.match(r'^ {0,3}(`{3,}|~{3,})', line):
                in_code_block = not in_code_block
                continue
            if in_code_block:
                continue

            m = re.match(r'^(#{1,2})\s+(.+)', line)
            if m:
                level = len(m.group(1))
                title = m.group(2).strip()
                headings.append({'level': level, 'title': title, 'anchor': slugify(title)})

    return headings


def main():
    nav_path = ROOT / '_data' / 'navigation.yml'
    with open(nav_path) as f:
        nav = yaml.safe_load(f)

    toc = []
    for item in nav:
        link = item['link']
        # Derive markdown filename from the html link
        stem = Path(link).stem
        md_path = ROOT / f'{stem}.md'
        if not md_path.exists():
            md_path = ROOT / f'{stem}.markdown'
        if not md_path.exists():
            continue

        headings = extract_headings(md_path)
        toc.append({
            'title': item['name'],
            'link': link,
            'headings': headings,
        })

    out_path = ROOT / '_data' / 'toc.yml'
    with open(out_path, 'w') as f:
        yaml.dump(toc, f, allow_unicode=True, default_flow_style=False, sort_keys=False)

    print(f"Written {out_path} ({len(toc)} pages)")


if __name__ == '__main__':
    main()
