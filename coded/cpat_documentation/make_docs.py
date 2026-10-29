"""Build the Word copies of the Coded CPAT documents from their qmd sources.

The qmd files are the source (coded/NORMS.md section 8); the .docx files next to them are generated and never
edited by hand. With Quarto installed, `quarto render <file>.qmd --to docx` gives the same result; this script is
the fallback that needs only pandoc, and it is what the repository uses.

Mermaid diagrams: each ```{mermaid} block carries a first line `%%| fig-name: <name>`. Quarto draws the block itself
(HTML, website). For Word, the block is replaced by `figures/<name>.png`, rendered with mermaid and Playwright when
`--mermaid-js <path to mermaid.min.js>` is given (Node.js with Playwright needed), else the committed PNG is used.

Usage (from coded/cpat_documentation):
    python make_docs.py                                   # every qmd listed in DOCUMENTS
    python make_docs.py --mermaid-js /path/mermaid.min.js # also re-render the diagrams
"""

from __future__ import annotations

import argparse
import os
import re
import shutil
import subprocess
import tempfile
from pathlib import Path

HERE = Path(__file__).resolve().parent

# qmd source -> Word copy (same folder)
DOCUMENTS = [
    "project/Spec.qmd",
    "equations/Equations.qmd",
    "equations/Equations_codes.qmd",
]

MERMAID_BLOCK = re.compile(r"```\{mermaid\}\n%%\| fig-name: (?P<name>[\w-]+)\n(?P<body>.*?)```", re.S)
YAML_HEADER = re.compile(r"\A---\n.*?\n---\n", re.S)

RENDER_JS = r"""
const { chromium } = require('playwright');
const fs = require('fs');
(async () => {
  const [mjs, src, out] = process.argv.slice(2);
  const code = fs.readFileSync(src, 'utf8').replace(/</g, '&lt;');
  const browser = await chromium.launch();
  const page = await browser.newPage({ deviceScaleFactor: 2 });
  await page.setContent(`<html><body style="margin:0;background:white"><pre class="mermaid">${code}</pre></body></html>`);
  await page.addScriptTag({ path: mjs });
  await page.evaluate(async () => {
    mermaid.initialize({ startOnLoad: false, theme: 'neutral', flowchart: { htmlLabels: true } });
    await mermaid.run();
  });
  await (await page.$('pre.mermaid svg')).screenshot({ path: out });
  await browser.close();
})();
"""


def render_mermaid(name: str, body: str, figures: Path, mermaid_js: Path | None) -> Path:
    """Render one mermaid block to figures/<name>.png (only when mermaid_js is given); return the PNG path."""
    png = figures / f"{name}.png"
    if mermaid_js is None:
        if not png.exists():
            raise FileNotFoundError(f"{png} is missing: run with --mermaid-js to render it")
        return png
    figures.mkdir(exist_ok=True)
    with tempfile.TemporaryDirectory() as tmp:
        src, js = Path(tmp, "diagram.mmd"), Path(tmp, "render.js")
        src.write_text(body, encoding="utf-8")
        js.write_text(RENDER_JS, encoding="utf-8")
        npm_root = subprocess.run(["npm", "root", "-g"], capture_output=True, text=True, check=True).stdout.strip()
        subprocess.run(["node", str(js), str(mermaid_js), str(src), str(png)], check=True,
                       env={**os.environ, "NODE_PATH": npm_root})
    return png


def to_markdown(qmd: Path, mermaid_js: Path | None) -> tuple[str, str]:
    """Return (title, pandoc markdown) for a qmd: mermaid blocks become images, Quarto-only lines are dropped."""
    text = qmd.read_text(encoding="utf-8")
    header = YAML_HEADER.match(text)
    title = ""
    if header:
        found = re.search(r'^title:\s*"?(.*?)"?\s*$', header.group(0), re.M)
        title = found.group(1) if found else ""
    figures = qmd.parent / "figures"

    def image(match: re.Match) -> str:
        png = render_mermaid(match["name"], match["body"], figures, mermaid_js)
        return f"![]({png.relative_to(qmd.parent).as_posix()})"

    text = MERMAID_BLOCK.sub(image, text)
    text = re.sub(r"^\{\{<.*?>\}\}\s*$", "", text, flags=re.M)  # Quarto shortcodes
    return title, text


def build(qmd: Path, mermaid_js: Path | None) -> Path:
    title, text = to_markdown(qmd, mermaid_js)
    docx = qmd.with_suffix(".docx")
    with tempfile.NamedTemporaryFile("w", suffix=".md", delete=False, dir=qmd.parent, encoding="utf-8") as tmp:
        tmp.write(text)
    try:
        cmd = ["pandoc", tmp.name, "-f", "markdown", "-o", str(docx), "--toc", "--toc-depth=2",
               f"--resource-path={qmd.parent}"]
        if title:
            cmd += ["--metadata", f"title={title}"]
        subprocess.run(cmd, check=True, cwd=qmd.parent)
    finally:
        Path(tmp.name).unlink()
    return docx


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("files", nargs="*", help="qmd files (default: DOCUMENTS)")
    parser.add_argument("--mermaid-js", type=Path, help="mermaid.min.js, to re-render the diagrams")
    args = parser.parse_args()
    if shutil.which("pandoc") is None:
        raise SystemExit("pandoc is needed (or use: quarto render <file>.qmd --to docx)")
    for name in args.files or DOCUMENTS:
        print("wrote", build((HERE / name).resolve(), args.mermaid_js).relative_to(HERE))


if __name__ == "__main__":
    main()
