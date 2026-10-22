"""Rebuild the generated Word documents of documentation/ (plan and index: README.md here).

The generators write straight into this folder:
- make_docs_v<n>.py: CPAT-AI-Mitigation-MVP_Documentation_v<version>.docx (quick start, equations, method notes);
- make_bugfix_book_v<n>.py: CPAT-AI-Mitigation-MVP_BugsAndIssues_v<version>.docx (the one register).
The other documents here are kept by hand. Run after the release's register scripts:

    python excel_ai/mitigation/make_documentation.py
"""
import os
import subprocess
import sys

MVP = os.path.dirname(os.path.abspath(__file__))   # excel_ai/mitigation/
V_ = '7_0'                                       # mitigation MVP release (build_v<n>.py)


def main():
    for script in (f'make_docs_v{V_}.py', f'make_bugfix_book_v{V_}.py'):
        subprocess.run([sys.executable, script], cwd=MVP, check=True)


if __name__ == '__main__':
    main()
