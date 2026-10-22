"""Build the dark Python cheat sheet PDF.

Usage:  python cheatsheet/build_cheatsheet.py
Reads cheatsheet.src.html + ../progress.md, writes the A4 PDF (Python-Cheatsheet.pdf)
and the phone PDF (Python-Cheatsheet-Phone.pdf)
"""
import datetime
import html
import pathlib
import re
import subprocess
import tempfile

HERE = pathlib.Path(__file__).resolve().parent
REPO = HERE.parent
SRC = HERE / "cheatsheet.src.html"
OUT_HTML = HERE / "cheatsheet.html"
OUT_PDF = HERE / "Python-Cheatsheet.pdf"
OUT_PHONE_HTML = HERE / "cheatsheet-phone.html"
OUT_PHONE_PDF = HERE / "Python-Cheatsheet-Phone.pdf"

# Phone edition: narrow page, one column, bigger text (same content)
PHONE_CSS = """<style>
  @page { size: 95mm 190mm; margin: 0; }
  body { font-size: 11pt; padding: 6mm 5mm; }
  .grid, .wr { grid-template-columns: 1fr; }
  .toc ol { columns: 1; }
  .cover { min-height: 176mm; padding: 9mm 7mm; }
  .cover h1 { font-size: 30pt; }
  .stat { min-width: 0; flex: 1 1 38%; padding: 3mm 4mm; }
  .sec-head h2 { font-size: 16pt; }
  pre { font-size: 8.8pt; padding: 2mm 2.5mm; }
  table { font-size: 8.6pt; }
  th, td { padding: 1.3mm 1.6mm; }
  code { font-size: 8.6pt; word-break: break-word; }
</style>
</head>"""
CHROME = pathlib.Path(r"C:\Program Files\Google\Chrome\Application\chrome.exe")

HACKERRANK_URLS = {
    "Python If-Else": "py-if-else",
    "Arithmetic Operators": "python-arithmetic-operators",
    "Python: Division": "python-division",
    "Loops": "python-loops",
    "Print Function": "python-print",
    "Find the Runner-Up Score!": "find-second-maximum-number-in-a-list",
    "Write a function (leap year)": "write-a-function",
    "Finding the percentage": "finding-the-percentage",
    "Nested Lists": "nested-list",
    "Lists": "python-lists",
    "Tuples": "python-tuples",
    "Word Order": "word-order",
}

KEYWORDS = r"def|return|for|in|if|elif|else|while|break|continue|pass|None|True|False|and|or|not|import|from|class|is|del|lambda|try|except|with|as"
BUILTINS = r"print|len|range|int|str|float|list|dict|set|tuple|sum|max|min|sorted|input|map|type|reversed|enumerate|zip|abs|round"
TOKEN = re.compile(
    r"(?P<c>#[^\n]*)"
    r"|(?P<s>[fF]?(?:\"(?:\\.|[^\"\\\n])*\"|'(?:\\.|[^'\\\n])*'))"
    r"|(?P<k>\b(?:" + KEYWORDS + r")\b)"
    r"|(?P<b>\b(?:" + BUILTINS + r")\b(?=\())"
    r"|(?P<n>\b\d+(?:\.\d+)?\b)"
)


def highlight(code: str) -> str:
    """Colour Python code. `code` arrives HTML-escaped and leaves HTML-escaped."""
    raw = html.unescape(code)
    out, pos = [], 0
    for m in TOKEN.finditer(raw):
        out.append(html.escape(raw[pos:m.start()], quote=False))
        out.append(f'<span class="{m.lastgroup}">{html.escape(m.group(), quote=False)}</span>')
        pos = m.end()
    out.append(html.escape(raw[pos:], quote=False))
    return "".join(out)


def table_rows(section: str):
    """Return the data rows of the markdown table under `## <section>` in progress.md."""
    text = (REPO / "progress.md").read_text(encoding="utf-8")
    m = re.search(r"^## [^\n]*" + re.escape(section) + r"[^\n]*\n(.*?)(?=^## |\Z)", text, re.S | re.M)
    if not m:
        return []
    rows = []
    for line in m.group(1).splitlines():
        cells = [c.strip() for c in line.strip().strip("|").split("|")]
        if len(cells) >= 3 and re.match(r"\d{4}-\d{2}-\d{2}", cells[0]):
            rows.append(cells[:3])
    return rows


def md_inline(text: str) -> str:
    text = html.escape(text, quote=False)
    text = re.sub(r"`([^`]+)`", r"<code>\1</code>", text)
    return re.sub(r"\*\*([^*]+)\*\*", r"<b>\1</b>", text)


def leetcode_link(title: str) -> str:
    m = re.match(r"(\d+)\.\s*(.+)", title)
    if not m:
        return md_inline(title)
    slug = re.sub(r"[^a-z0-9]+", "-", m.group(2).lower()).strip("-")
    return f'<a href="https://leetcode.com/problems/{slug}/">{html.escape(title)}</a>'


def hackerrank_link(title: str) -> str:
    slug = HACKERRANK_URLS.get(title)
    if not slug:
        return md_inline(title)
    return f'<a href="https://www.hackerrank.com/challenges/{slug}/problem">{html.escape(title)}</a>'


def build() -> None:
    page = SRC.read_text(encoding="utf-8")
    page = re.sub(r"<pre>(.*?)</pre>", lambda m: "<pre>" + highlight(m.group(1)) + "</pre>", page, flags=re.S)

    lc, hr = table_rows("LeetCode"), table_rows("HackerRank")
    lc_rows = "\n".join(f"    <tr><td>{d}</td><td>{leetcode_link(p)}</td><td>{md_inline(r)}</td></tr>" for d, p, r in lc)
    hr_rows = "\n".join(f"    <tr><td>{d}</td><td>{hackerrank_link(p)}</td><td>{md_inline(r)}</td></tr>" for d, p, r in hr)
    lessons = len(list(REPO.glob("day[0-9][0-9].py")))
    today = datetime.date.today().strftime("%d %b %Y")

    for key, value in {"{{LESSONS}}": str(lessons), "{{LEETCODE}}": str(len(lc)), "{{HACKERRANK}}": str(len(hr)),
                       "{{UPDATED}}": today, "{{LEETCODE_ROWS}}": lc_rows, "{{HACKERRANK_ROWS}}": hr_rows}.items():
        page = page.replace(key, value)
    OUT_HTML.write_text(page, encoding="utf-8")
    OUT_PHONE_HTML.write_text(page.replace("</head>", PHONE_CSS, 1), encoding="utf-8")

    for html_file, pdf_file in [(OUT_HTML, OUT_PDF), (OUT_PHONE_HTML, OUT_PHONE_PDF)]:
        with tempfile.TemporaryDirectory() as profile:
            subprocess.run([str(CHROME), "--headless=new", "--disable-gpu", "--no-pdf-header-footer",
                            "--generate-pdf-document-outline", f"--user-data-dir={profile}",
                            f"--print-to-pdf={pdf_file}", html_file.as_uri()],
                           check=True, capture_output=True, timeout=120)
    print(f"Built {OUT_PDF.name} + {OUT_PHONE_PDF.name}: {lessons} lessons, {len(lc)} LeetCode, {len(hr)} HackerRank")


if __name__ == "__main__":
    build()
