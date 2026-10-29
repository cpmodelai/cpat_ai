"""Rebuild the generated documents of a release (after build.py), in order:

- make_replication_lists.py: ../BUGS.md, ../ISSUES.md;
- make_bugfix_book.py: ../Legacy_CPAT_Bugs_v<version>.docx (and ../legacy/Legacy_CPAT_Register.json);
- make_tracker.py: ../Tracking_Legacy_Bugs_v<version>.xlsx (the master list; the team's tabs kept);
- make_codesmap.py: ../CPAT-AI_CodesMap_v<version>.xlsx (codes and inputs);
- make_docs.py: CPAT-AI-Mitigation_Documentation.docx (with the issues, data issues and the procedure as appendices)
  and CPAT-AI-Mitigation_Methods.docx.
The deck: python presentation/make_screenshots.py && node presentation/build_deck.js.

    python excel_ai/mitigation/make_documentation.py
"""
import os
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))


def main():
    for script in ('make_replication_lists.py', 'make_bugfix_book.py', 'make_tracker.py', 'make_codesmap.py',
                   'make_docs.py'):
        subprocess.run([sys.executable, script], cwd=HERE, check=True)


if __name__ == '__main__':
    main()
