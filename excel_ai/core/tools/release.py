"""File naming and release layout of excel_ai/ (NORMS 5; user rules 2026-10-28, 2026-10-30).

- Every version of a module workbook, the current one included, sits in the module's releases/ folder as
  <Name>_v<version>.<ext> (mitigation/releases/, distribution/releases/, air_pollution/releases/).
- excel_ai/active_workbooks/ holds the permalinked copy of each module, <Name>_latest.<ext>: what people open and
  what the modules and links read (it replaced permalink/ and permalink_countryeditable/, 2026-10-30).
- The documents people read (the bug book, the tracker, the codes map, the overview deck) keep their current version at
  the top of excel_ai/; writing a new version moves the older ones to their releases/ folder.
"""
import glob
import os
import re
import shutil

XL = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..'))   # excel_ai/
ACTIVE = os.path.join(XL, 'active_workbooks')
REGISTER_RELEASES = os.path.join(XL, 'legacy', 'register', 'releases')

# name -> (folder of the current version, folder of the older versions)
HOME = {
    'CPAT-AI-Mitigation-Prototype': ('mitigation/releases', 'mitigation/releases'),
    'CPAT-AI-Distribution-Prototype': ('distribution/releases', 'distribution/releases'),
    'CPAT-AI-Air-Pollution-Standalone': ('air_pollution/releases', 'air_pollution/releases'),
    'CPAT-AI_Overview': ('', 'mitigation/releases'),
    'Legacy_CPAT_Bugs': ('', 'legacy/register/releases'),
    'Tracking_Legacy_Bugs': ('', 'legacy/register/releases'),
    'CPAT-AI_CodesMap': ('', 'legacy/register/releases'),
    'CPAT-AI_BugsAndIssues': ('', 'legacy/register/releases'),
}


def _dirs(name):
    cur, old = HOME.get(name, ('', 'legacy/register/releases'))
    return os.path.join(XL, cur), os.path.join(XL, old)


def versioned(name, version, ext):
    """Where the current version of a file is written."""
    return os.path.join(_dirs(name)[0], f'{name}_v{version}.{ext}')


def permalink(name, ext):
    return os.path.join(ACTIVE, f'{name}_latest.{ext}')


def publish(path, link=False):
    """Move the older versions of the file at path to its releases folder (when that is not where it sits); with link,
    copy it to active_workbooks/<name>_latest.<ext>."""
    m = re.match(r'(.+)_v(\d+(?:\.\d+)*)\.(\w+)$', os.path.basename(path))
    name, _ver, ext = m.groups()
    cur, old_dir = _dirs(name)
    os.makedirs(old_dir, exist_ok=True)
    if os.path.abspath(cur) != os.path.abspath(old_dir):
        for old in glob.glob(os.path.join(cur, f'{name}_v*.{ext}')):
            if os.path.abspath(old) != os.path.abspath(path):
                shutil.move(old, os.path.join(old_dir, os.path.basename(old)))
    if link:
        os.makedirs(ACTIVE, exist_ok=True)
        shutil.copy(path, permalink(name, ext))


def all_versions(name, ext):
    """Every version of a file, current and released, sorted by version."""
    cur, old_dir = _dirs(name)
    files = set(glob.glob(os.path.join(cur, f'{name}_v*.{ext}')) + glob.glob(os.path.join(old_dir, f'{name}_v*.{ext}')))
    ver = lambda f: tuple(int(x) for x in re.search(r'_v(\d+(?:\.\d+)*)\.\w+$', f).group(1).split('.'))
    return sorted(files, key=ver)
