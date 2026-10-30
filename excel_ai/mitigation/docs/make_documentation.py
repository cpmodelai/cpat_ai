"""Rebuild the generated documents of a release (after build.py), in order:

- make_replication_lists.py: ../BUGS.md, ../ISSUES.md;
- make_bugfix_book.py: ../Legacy_CPAT_Bugs_v<version>.docx (and ../legacy/Legacy_CPAT_Register.json);
- make_tracker.py: ../Tracking_Legacy_Bugs_v<version>.xlsx (the master list; the team's tabs kept);
- make_codesmap.py: ../CPAT-AI_CodesMap_v<version>.xlsx (codes and inputs);
- make_docs.py: CPAT-AI-Mitigation_Documentation.docx (with the issues, data issues and the procedure as appendices)
  and CPAT-AI-Mitigation_Methods.docx.
The deck: python presentation/make_screenshots.py && node presentation/build_deck.js.

    python excel_ai/mitigation/docs/make_documentation.py
"""
import os as _os, sys as _sys  # the excel_ai code folders and data/scripts on the path (core/tools/xlpaths.py)
_xl = _os.path.dirname(_os.path.abspath(__file__))
while _os.path.basename(_xl) != 'excel_ai':
    _xl = _os.path.dirname(_xl)
_sys.path.insert(0, _os.path.join(_xl, 'core', 'tools'))
import xlpaths  # noqa: E402,F401
import os
import subprocess
import sys

HERE = xlpaths.MIT                     # excel_ai/mitigation/ (the script sits in a subfolder)


def main():
    for script in ('make_replication_lists.py', 'make_bugfix_book.py', 'make_tracker.py', 'make_codesmap.py',
                   'make_docs.py'):
        subprocess.run([sys.executable, script], cwd=HERE, check=True)


if __name__ == '__main__':
    main()
