"""File naming and release layout of excel_ai/ (NORMS 5; user rules 2026-10-28, 2026-10-30).

- Every version of a module workbook, the current one included, sits in the module's releases/ folder as
  <Name>_v<version>.<ext> (mitigation/releases/, distribution/releases/, air_pollution/releases/).
- v1.2.0 (user 2026-10-31): the latest unactivated copy of each module, <Name>_latest.xlsx, sits in the module's own
  folder (excel_ai/mitigation/, ...; the GitHub link of the Master points to it). excel_ai/active_workbooks/ holds what
  people open and run: the Master workbook (CPAT-AI-Master_UserGuide.xlsm, the only one with macros) and the
  activated copies <Name>_latest.xlsb that the Master writes (generated files: never merged, regenerated).
- The documents people read keep their current version where people look: the bug book and the tracker in
  excel_ai/bugs_and_legacy/, the codes map and the overview deck at the top of excel_ai/; writing a new version moves
  the older ones to their releases/ folder.
"""
import glob
import os
import re
import shutil

XL = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..'))   # excel_ai/
ACTIVE = os.path.join(XL, 'active_workbooks')
REGISTER_RELEASES = os.path.join(XL, 'bugs_and_legacy', 'register', 'releases')

# name -> (folder of the current version, folder of the older versions)
HOME = {
    'CPAT-AI-Mitigation-Prototype': ('mitigation/releases', 'mitigation/releases'),
    'CPAT-AI-Distribution-Prototype': ('distribution/releases', 'distribution/releases'),
    'CPAT-AI-Air-Pollution-Standalone': ('air_pollution/releases', 'air_pollution/releases'),
    'CPAT-AI-Master_UserGuide': ('master/releases', 'master/releases'),   # v1.2.0: the Master (copy: active_workbooks)
    'CPAT-AI_Overview': ('', 'mitigation/releases'),
    'Legacy_CPAT_Bugs': ('bugs_and_legacy', 'bugs_and_legacy/register/releases'),
    'Tracking_Legacy_Bugs': ('bugs_and_legacy', 'bugs_and_legacy/register/releases'),
    'CPAT-AI_CodesMap': ('', 'bugs_and_legacy/register/releases'),
    'CPAT-AI_BugsAndIssues': ('', 'bugs_and_legacy/register/releases'),
}


def _dirs(name):
    cur, old = HOME.get(name, ('', 'bugs_and_legacy/register/releases'))
    return os.path.join(XL, cur), os.path.join(XL, old)


def versioned(name, version, ext):
    """Where the current version of a file is written."""
    return os.path.join(_dirs(name)[0], f'{name}_v{version}.{ext}')


MODULE_DIR = {'CPAT-AI-Mitigation-Prototype': 'mitigation', 'CPAT-AI-Distribution-Prototype': 'distribution',
              'CPAT-AI-Air-Pollution-Standalone': 'air_pollution'}


def permalink(name, ext):
    """The latest unactivated copy: in the module's folder (v1.2.0; before, in active_workbooks/)."""
    return os.path.join(XL, MODULE_DIR[name], f'{name}_latest.{ext}') if name in MODULE_DIR else \
        os.path.join(ACTIVE, f'{name}_latest.{ext}')


def activated(name):
    """v1.2.0: the activated copy the Master writes (Excel binary workbook), in active_workbooks/."""
    return os.path.join(ACTIVE, f'{name}_latest.xlsb')


def publish(path, link=False):
    """Move the older versions of the file at path to its releases folder (when that is not where it sits); with link,
    copy it to <name>_latest.<ext> (permalink: the module's folder)."""
    m = re.match(r'(.+)_v(\d+(?:\.\d+)*)\.(\w+)$', os.path.basename(path))
    name, _ver, ext = m.groups()
    cur, old_dir = _dirs(name)
    os.makedirs(old_dir, exist_ok=True)
    if os.path.abspath(cur) != os.path.abspath(old_dir):
        for old in glob.glob(os.path.join(cur, f'{name}_v*.{ext}')):
            if os.path.abspath(old) != os.path.abspath(path):
                shutil.move(old, os.path.join(old_dir, os.path.basename(old)))
    if link:
        os.makedirs(os.path.dirname(permalink(name, ext)), exist_ok=True)
        shutil.copy(path, permalink(name, ext))


def all_versions(name, ext):
    """Every version of a file, current and released, sorted by version."""
    cur, old_dir = _dirs(name)
    files = set(glob.glob(os.path.join(cur, f'{name}_v*.{ext}')) + glob.glob(os.path.join(old_dir, f'{name}_v*.{ext}')))
    ver = lambda f: tuple(int(x) for x in re.search(r'_v(\d+(?:\.\d+)*)\.\w+$', f).group(1).split('.'))
    return sorted(files, key=ver)
