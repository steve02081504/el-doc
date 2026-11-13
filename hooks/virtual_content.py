"""Keep large reference pages out of the browser's initial DOM and layout."""

from html import escape, unescape
import hashlib
from html.parser import HTMLParser
import json
from pathlib import Path
import re


class TocRanges(HTMLParser):
	def __init__(self, html):
		super().__init__()
		self.lines = [0] + [match.end() for match in re.finditer("\n", html)]
		self.ranges = []
		self.start = None
		self.depth = 0
		self.feed(html)

	def handle_starttag(self, tag, attrs):
		if tag != "nav": return
		if "md-nav--secondary" in dict(attrs).get("class", "").split() and self.start is None:
			line, column = self.getpos()
			self.start = self.lines[line - 1] + column
		if self.start is not None: self.depth += 1

	def handle_endtag(self, tag):
		if tag != "nav" or self.start is None: return
		self.depth -= 1
		if self.depth == 0:
			line, column = self.getpos()
			self.ranges.append((self.start, self.lines[line - 1] + column + len("</nav>")))
			self.start = None


class Ids(HTMLParser):
	def __init__(self, html):
		super().__init__()
		self.ids = []
		self.feed(html)

	def handle_starttag(self, tag, attrs):
		identity = dict(attrs).get("id")
		if identity: self.ids.append(identity)


class ListBlocks(HTMLParser):
	"""Locate complete outer blocks, so nested lists are never cut in half."""
	def __init__(self, html):
		super().__init__()
		self.lines = [0] + [match.end() for match in re.finditer("\n", html)]
		self.stack = []
		self.blocks = []
		self.feed(html)

	def handle_starttag(self, tag, attrs):
		if tag in ("table", "ul", "ol"):
			line, column = self.getpos()
			self.stack.append((tag, self.lines[line - 1] + column))

	def handle_endtag(self, tag):
		if self.stack and tag == self.stack[-1][0]:
			_, start = self.stack.pop()
			if not self.stack:
				line, column = self.getpos()
				self.blocks.append((tag, start, self.lines[line - 1] + column + len(tag) + 3))


def virtualize_page(path, batch_size=40):
	path = Path(path)
	html = path.read_text(encoding="utf-8")
	article = re.search(r'<article\b[^>]*>(.*?)</article>', html, re.S)
	if not article: return 0
	headings = list(re.finditer(r'<h2\b[^>]*>.*?</h2>', article[1], re.S))
	if len(headings) > batch_size * 3:
		prefix = article[1][:headings[0].start()]
		sections = [article[1][heading.start():headings[i + 1].start() if i + 1 < len(headings) else len(article[1])]
			for i, heading in enumerate(headings)]
		labels = [heading[0] for heading in headings]
	else:
		# Split large flat tables/lists into valid, independently rendered blocks.
		# Nested lists stay intact, since their hierarchy is meaningful.
		sections, labels = [], []
		cursor = 0
		prefix = ""
		for tag, begin, end in ListBlocks(article[1]).blocks:
			block = article[1][begin:end]
			if len(re.findall(r'<(?:table|ul|ol)\b', block)) != 1: continue
			row_tag = "tr" if tag == "table" else "li"
			body = re.search(r'<tbody\b[^>]*>(.*?)</tbody>', block, re.S) if tag == "table" else None
			content = body[1] if body else block
			rows = list(re.finditer(fr'<{row_tag}\b[^>]*>.*?</{row_tag}>', content, re.S))
			if len(rows) <= batch_size * 3: continue
			if tag == "table" and body is None: continue
			before = article[1][cursor:begin]
			if not sections: prefix = before
			elif before.strip():
				sections.append(before)
				labels.append(before)
			if body:
				opening, closing = block[:body.start(1)], block[body.end(1):]
			else:
				opening, closing = block[:rows[0].start()], block[rows[-1].end():]
			for row_index, row in enumerate(rows):
				row_opening = opening if row_index == 0 else re.sub(r'\s+id="[^"]*"', '', opening)
				if tag == 'ol':
					start_match = re.search(r'\bstart="(-?\d+)"', opening)
					initial = int(start_match[1]) if start_match else 1
					row_opening = re.sub(r'\s+start="[^"]*"', '', row_opening)
					row_opening = row_opening.replace('<ol', f'<ol start="{initial + row_index}"', 1)
				sections.append(row_opening + row[0] + closing)
				labels.append(row[0])
			cursor = end
		if not sections: return 0
		if article[1][cursor:].strip():
			sections.append(article[1][cursor:])
			labels.append(article[1][cursor:])
	# The complete version remains available for printing, browser Find and no JS.
	(path.parent / "full.html").write_text(html, encoding="utf-8", newline="\n")
	index = []
	blocks = []
	for start in range(0, len(sections), batch_size):
		batch = sections[start:start + batch_size]
		# Content hashes prevent stale chunks after a Pages deployment.
		anchors = []
		for offset, section in enumerate(batch):
			ids = Ids(section).ids
			if not ids:
				ids = [f'el-virtual-item-{start + offset}']
				if section.startswith('<table'):
					batch[offset] = re.sub(r'(<tbody\b[^>]*>\s*<tr)\b', fr'\1 id="{ids[0]}"', section, count=1)
				elif section.startswith(('<ul', '<ol')):
					batch[offset] = re.sub(r'<li\b', f'<li id="{ids[0]}"', section, count=1)
				else:
					batch[offset] = f'<div id="{ids[0]}">{section}</div>'
			for identity in ids:
				anchors.append(f'<span id="{escape(identity, quote=True)}" style="top:{offset * 100 / len(batch):.3f}%"></span>')
			# HTMLParser decodes entities for the search labels.
			title = unescape(re.sub(r'<[^>]+>', ' ', labels[start + offset])).strip().removesuffix("¶").strip()
			title = " ".join(title.split())
			index.append({"title": title, "id": ids[0]})
		# Adjacent rows share one table/header, and adjacent list items one list.
		joined = ''.join(batch)
		joined = re.sub(r'</tbody>\s*</table>\s*<table\b[^>]*>\s*(?:<thead\b[^>]*>.*?</thead>\s*)?<tbody\b[^>]*>', '', joined, flags=re.S)
		joined = re.sub(r'</(ul|ol)>\s*<\1\b[^>]*>', '', joined)
		payload = json.dumps(batch if joined == ''.join(batch) else [joined], ensure_ascii=False)
		filename = "content-" + hashlib.sha256(payload.encode()).hexdigest()[:16] + ".json"
		(path.parent / filename).write_text(payload, encoding="utf-8", newline="\n")
		blocks.append(f'<section class="el-virtual-chunk" data-content="{filename}" style="min-height:{len(batch) * 220}px">' + ''.join(anchors) + '</section>')
	(path.parent / "content-index.json").write_text(json.dumps(index, ensure_ascii=False), encoding="utf-8", newline="\n")
	controls = '<div class="el-virtual-tools"><label>查找本页条目 <input type="search" data-type-search autocomplete="off"></label><div data-type-results></div><p>按阅读位置加载内容。<a href="full.html">完整页面（查找／打印，加载较慢）</a></p><noscript>请启用 JavaScript，或打开完整页面。</noscript></div>'
	body = prefix + controls + '<div data-virtual-content>' + ''.join(blocks) + '</div>'
	html = html[:article.start(1)] + body + html[article.end(1):]
	for start, end in reversed(TocRanges(html).ranges):
		html = html[:start] + html[end:]
	path.write_text(html, encoding="utf-8", newline="\n")
	return len(sections)


def virtualize_site(site):
	return sum(virtualize_page(path) for path in list(Path(site).rglob("*.html")) if path.name != "full.html")
