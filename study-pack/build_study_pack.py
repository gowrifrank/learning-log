"""Build the dark Study Pack PDF (all lessons + review docs in one file).

Usage:  python study-pack/build_study_pack.py      (or python build_pdfs.py for everything)
Reads the markdown files listed in DOCS, writes the A4 PDF (Python-Study-Pack.pdf)
and the phone PDF (Python-Study-Pack-Phone.pdf), with a clickable contents page and bookmarks.
"""
import datetime
import pathlib
import re
import subprocess
import sys
import tempfile

import markdown

HERE = pathlib.Path(__file__).resolve().parent
REPO = HERE.parent
sys.path.insert(0, str(REPO / "cheatsheet"))
from build_cheatsheet import CHROME, PHONE_CSS, highlight  # same Chrome, phone layout and code colours

GITHUB = "https://github.com/gowrifrank/learning-log/blob/main/"
OUT_HTML = HERE / "study-pack.html"
OUT_PDF = HERE / "Python-Study-Pack.pdf"
OUT_PHONE_HTML = HERE / "study-pack-phone.html"
OUT_PHONE_PDF = HERE / "Python-Study-Pack-Phone.pdf"

# Guides that also get their own PDF (A4 + phone), next to the pack: (file, colour, PDF name).
# Empty on purpose: everything lives in the one Study Pack (user's choice, 28 Oct).
STANDALONE = []

# (file, colour, one-line description). Order = order in the PDF. Add new lessons here.
DOCS = [
    ("lessons/revision-1.md", "green", "Start here: the 9 revision topics, checklists, what to rewrite"),
    ("lessons/python-reference.md", "blue", "Types, ranges, built-ins: what each takes and gives back"),
    ("lessons/add-remove-loop-book.md", "pink", "Drills: position vs value, add / remove / loop"),
    ("lessons/data-structures-guide.md", "cyan", "What am I holding? Nested data, parsing, printing"),
    ("lessons/problem-solving-method.md", "violet", "The STEP method: solve without panicking"),
    ("lessons/review-weekend-1.md", "lime", "Predict-the-output drills: strings, map, dicts"),
    ("lessons/day06-functions.md", "amber", "Day 06 lesson: functions"),
    ("lessons/day07-dictionaries.md", "orange", "Day 07 lesson: dictionaries"),
]

CSS_EXTRA = """<style>
  .doc { break-before: page; }
  .doc h1 { font-size: 20pt; color: var(--c); border-bottom: 2px solid var(--c); padding-bottom: 2mm; margin-bottom: 4mm; }
  .doc h2 { font-size: 14pt; color: var(--c); margin: 6mm 0 2mm; }
  .doc h3 { font-size: 11.5pt; margin: 4mm 0 2mm; }
  .doc h4 { font-size: 10pt; margin: 3mm 0 1mm; }
  .doc h1, .doc h2, .doc h3, .doc h4 { break-after: avoid; }
  .doc blockquote { margin: 2mm 0 3mm; padding: 2mm 4mm; background: var(--panel); border-left: 4px solid var(--c); border-radius: 6px; color: var(--muted); }
  .doc blockquote p { margin: 0.5mm 0; }
  .doc hr { border: 0; border-top: 1px solid var(--line); margin: 5mm 0; }
  .doc pre code { background: none; color: inherit; padding: 0; font-size: inherit; }
  .doc li > p { margin: 0; }
  .answers { border-top: 2px dashed var(--c); margin-top: 6mm; padding-top: 2mm; }
  .back { float: right; font-size: 8pt; color: var(--muted); border: 1px solid var(--line); border-radius: 20px; padding: 1mm 3mm; }
</style>
</head>"""


# Phone edition: tables with 4+ columns don't fit 95 mm (Chrome would shrink the WHOLE PDF),
# so each row becomes a card and every cell shows its column name above it
PHONE_STACK_CSS = """<style>
  table.stack thead { display: none; }
  table.stack, table.stack tbody, table.stack tr, table.stack td { display: block; width: 100%; }
  table.stack { break-inside: auto; }
  table.stack tr { background: var(--panel); border: 1px solid var(--line); border-radius: 8px; margin-bottom: 2.5mm; break-inside: avoid; }
  table.stack td, table.stack tr:nth-child(even) td { background: none; border: 0; padding: 0.8mm 2.5mm; }
  table.stack td::before { content: attr(data-label); display: block; font-size: 7pt; font-weight: 700; color: var(--c); text-transform: uppercase; letter-spacing: 0.5px; }
</style>
</head>"""


def stack_wide_tables(page: str) -> str:
    """Give 4+ column tables class="stack" and a data-label (its column name) on every cell."""
    def one(m: re.Match) -> str:
        table = m.group(0)
        labels = [re.sub(r"<[^>]+>", "", h).replace('"', "'").strip() for h in re.findall(r"<th[^>]*>(.*?)</th>", table, flags=re.S)]
        if len(labels) < 4:
            return table

        def row(r: re.Match) -> str:
            cells = iter(labels)
            return re.sub(r"<td([^>]*)>", lambda c: f'<td{c.group(1)} data-label="{next(cells, "")}">', r.group(0))

        table = re.sub(r"<tr>.*?</tr>", row, table, flags=re.S)
        return table.replace("<table>", '<table class="stack">', 1)

    return re.sub(r"<table>.*?</table>", one, page, flags=re.S)


def slug(path: str) -> str:
    return pathlib.Path(path).stem


def render(path: str, in_pack: set | None = None) -> str:
    """Markdown file -> HTML fragment with ids and links made unique to this doc.
    `in_pack` = slugs of docs inside the same PDF (links to them jump inside it; others open on GitHub)."""
    text = (REPO / path).read_text(encoding="utf-8")
    # <details> answers would print collapsed (hidden), so turn them into a visible block at the end
    text = re.sub(r"<details>\s*<summary>(.*?)</summary>", r'\n<div class="answers" markdown="1">\n\n**\1**\n', text, flags=re.S)
    text = text.replace("</details>", "\n</div>\n")
    text = re.sub(r"^(\s*)- \[ \] ", r"\1- ☐ ", text, flags=re.M)
    text = re.sub(r"^(\s*)- \[x\] ", r"\1- ☑ ", text, flags=re.M | re.I)
    body = markdown.markdown(text, extensions=["tables", "fenced_code", "toc", "sane_lists", "md_in_html"])

    me = slug(path)
    body = re.sub(r'id="([^"]+)"', rf'id="{me}-\1"', body)
    body = re.sub(r'href="#([^"]+)"', rf'href="#{me}-\1"', body)

    if in_pack is None:
        in_pack = {slug(p) for p, _, _ in DOCS}
    folder = pathlib.PurePosixPath(path).parent

    def fix_link(m: re.Match) -> str:
        href = m.group(1)
        if href.startswith(("http", "#", "mailto:")):
            return m.group(0)
        target = pathlib.PurePosixPath(href.split("#")[0])
        if target.stem in in_pack and target.suffix == ".md":
            return f'href="#doc-{target.stem}"'                       # jump inside the PDF
        resolved = (folder / target).as_posix()
        parts = []
        for part in resolved.split("/"):                            # collapse "lessons/../notes.md"
            if part == "..":
                parts.pop()
            elif part != ".":
                parts.append(part)
        return f'href="{GITHUB}{"/".join(parts)}"'                   # open the file on GitHub

    body = re.sub(r'href="([^"]+)"', fix_link, body)
    body = re.sub(r'<pre><code[^>]*>(.*?)</code></pre>', lambda m: "<pre>" + highlight(m.group(1)) + "</pre>", body, flags=re.S)
    return body


def build() -> None:
    style = (REPO / "cheatsheet" / "cheatsheet.src.html").read_text(encoding="utf-8")
    head = style[:style.index("</head>")].replace("<title>Python Cheat Sheet: Gowri</title>", "<title>Python Study Pack: Gowri</title>")
    today = datetime.date.today().strftime("%d %b %Y")

    toc, docs = [], []
    for path, colour, desc in DOCS:
        html = render(path)
        title = re.sub(r"<[^>]+>", "", re.search(r"<h1[^>]*>(.*?)</h1>", html, flags=re.S).group(1))
        toc.append(f'<li><a href="#doc-{slug(path)}" style="--c:var(--{colour})">{title}<small>{desc}</small></a></li>')
        docs.append(f'<div class="doc" id="doc-{slug(path)}" style="--c:var(--{colour})">'
                    f'<a class="back" href="#toc">↑ contents</a>{html}</div>')

    page = f"""{head}</head>
<body>
<div class="cover" id="top">
  <div class="tag">PYTHON · FROM ZERO · LEARNING LOG</div>
  <h1>Python Study Pack</h1>
  <p>All my lessons, revision guides and drills in one place. <b>Start with Revision #1</b>, and cover the answers before checking them.</p>
  <div class="stats">
    <div class="stat"><b style="color:var(--cyan)">{len(DOCS)}</b><span>guides inside</span></div>
    <div class="stat"><b style="color:var(--pink)">{today}</b><span>last updated</span></div>
  </div>
</div>
<div class="toc" id="toc"><h2>📚 Contents</h2><ol>
{chr(10).join(toc)}
</ol></div>
{chr(10).join(docs)}
<div class="footer">Generated from the markdown files in <code>lessons/</code> · updated {today} · <a href="#top">↑ back to cover</a></div>
</body>
</html>"""
    write_pdfs(page, OUT_HTML, OUT_PDF, OUT_PHONE_HTML, OUT_PHONE_PDF)
    print(f"Built {OUT_PDF.name} + {OUT_PHONE_PDF.name}: {len(DOCS)} guides")
    build_standalone(head, today)


def build_standalone(head: str, today: str) -> None:
    """One guide = one PDF (A4 + phone)."""
    for path, colour, name in STANDALONE:
        html = render(path, in_pack=set())
        page = f"""{head}</head>
<body id="top">
<div class="doc" style="--c:var(--{colour}); break-before: auto">{html}</div>
<div class="footer">Generated from <code>{path}</code> · updated {today} · <a href="#top">↑ back to top</a></div>
</body>
</html>"""
        write_pdfs(page, HERE / f"{name}.html", HERE / f"{name}.pdf", HERE / f"{name}-Phone.html", HERE / f"{name}-Phone.pdf")
        print(f"Built {name}.pdf + {name}-Phone.pdf")


def write_pdfs(page: str, html_file: pathlib.Path, pdf_file: pathlib.Path,
               phone_html: pathlib.Path, phone_pdf: pathlib.Path) -> None:
    page = page.replace("</head>", CSS_EXTRA, 1)
    html_file.write_text(page, encoding="utf-8")
    phone = stack_wide_tables(page).replace("</head>", PHONE_CSS, 1).replace("</head>", PHONE_STACK_CSS, 1)
    phone_html.write_text(phone, encoding="utf-8")

    for src, out in [(html_file, pdf_file), (phone_html, phone_pdf)]:
        with tempfile.TemporaryDirectory() as profile:
            subprocess.run([str(CHROME), "--headless=new", "--disable-gpu", "--no-pdf-header-footer",
                            "--generate-pdf-document-outline", f"--user-data-dir={profile}",
                            f"--print-to-pdf={out}", src.as_uri()],
                           check=True, capture_output=True, timeout=120)


if __name__ == "__main__":
    build()
