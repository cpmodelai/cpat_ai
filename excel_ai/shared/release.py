"""File naming and release layout of excel_ai/ (NORMS 5, user rule 2026-10-28).

- The current version of each main file sits at the top of excel_ai/ as <Name>_v<version>.<ext>.
- When a new version is written, the older versions of the same file move to excel_ai/releases/.
- excel_ai/permalink/ holds only what other files and tools link to (data transfer): every module as <Name>_latest.<ext>.
  excel_ai/permalink_countryeditable/ is the same set, for local country runs (user 2026-10-29); publish writes both.
"""
import glob
import os
import re
import shutil

XL = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
RELEASES = os.path.join(XL, 'releases')
PERMALINK = os.path.join(XL, 'permalink')
PERMALINK_CE = os.path.join(XL, 'permalink_countryeditable')   # copy of permalink/ for local country runs


def versioned(name, version, ext):
    """excel_ai/<name>_v<version>.<ext>: where the current version is written."""
    return os.path.join(XL, f'{name}_v{version}.{ext}')


def permalink(name, ext):
    return os.path.join(PERMALINK, f'{name}_latest.{ext}')


def publish(path, link=False):
    """Move the older versions of the file at path from excel_ai/ to releases/; with link, copy it to permalink/ and
    permalink_countryeditable/."""
    m = re.match(r'(.+)_v(\d+(?:\.\d+)*)\.(\w+)$', os.path.basename(path))
    name, _ver, ext = m.groups()
    os.makedirs(RELEASES, exist_ok=True)
    for old in glob.glob(os.path.join(XL, f'{name}_v*.{ext}')):
        if os.path.abspath(old) != os.path.abspath(path):
            shutil.move(old, os.path.join(RELEASES, os.path.basename(old)))
    if link:
        for folder in (PERMALINK, PERMALINK_CE):
            os.makedirs(folder, exist_ok=True)
            shutil.copy(path, os.path.join(folder, f'{name}_latest.{ext}'))


def all_versions(name, ext):
    """Every version of a file, current (top of excel_ai/) and released, sorted by version."""
    files = glob.glob(os.path.join(XL, f'{name}_v*.{ext}')) + glob.glob(os.path.join(RELEASES, f'{name}_v*.{ext}'))
    ver = lambda f: tuple(int(x) for x in re.search(r'_v(\d+(?:\.\d+)*)\.\w+$', f).group(1).split('.'))
    return sorted(files, key=ver)
