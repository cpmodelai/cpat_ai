"""v4.9: one headless LibreOffice session driven through UNO (fast full build, user rule 2026-10-17).

The workbook is loaded once; each run writes its inputs, recalculates in memory (calculateAll, about 17 s for the
mitigation MVP) and reads only the cells it needs. This replaces one save, load, LAMBDA expansion, LibreOffice
conversion and reload per run (about 155 s each). Own user profile, so it never shares one with another
LibreOffice job.

    with Session() as s:
        doc = s.load(path)
        s.calc(doc)
        g = s.grid(doc, 'MTOutputs', r0, c0, r1, c1)    # g.cell(r, c).value, 1-based like openpyxl
"""
import html
import os
import re
import shutil
import subprocess
import tempfile
import time
import zipfile


class _Cell:
    __slots__ = ('value',)

    def __init__(self, v):
        self.value = v


class Grid:
    """Values of a cell range, read at once; cell(r, c) with sheet coordinates (1-based); empty cells None."""

    def __init__(self, r0, c0, data):
        self.r0, self.c0, self.data = r0, c0, data

    def cell(self, r, c):
        v = self.data[r - self.r0][c - self.c0]
        return _Cell(None if v == '' else v)


class Session:
    def __init__(self, timeout=120):
        self.timeout = timeout

    def __enter__(self):
        import uno                                  # imported here, not at module level: a spawned child that
                                                    # imports uno while it re-imports the parent's main module
                                                    # fails (pyuno runtime not initialized)
        self.profile = tempfile.mkdtemp(prefix='lo_cpat_')
        self.pipe = f'cpat_{os.getpid()}'
        self.proc = subprocess.Popen(['soffice', '--headless', '--invisible', '--norestore', '--nologo',
                                      f'-env:UserInstallation=file://{self.profile}',
                                      f'--accept=pipe,name={self.pipe};urp;'],
                                     stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        local = uno.getComponentContext()
        res = local.ServiceManager.createInstanceWithContext('com.sun.star.bridge.UnoUrlResolver', local)
        t0 = time.time()
        while True:
            try:
                ctx = res.resolve(f'uno:pipe,name={self.pipe};urp;StarOffice.ComponentContext')
                break
            except Exception:
                if time.time() - t0 > self.timeout:
                    raise
                time.sleep(0.3)
        self.desktop = ctx.ServiceManager.createInstanceWithContext('com.sun.star.frame.Desktop', ctx)
        self.docs = []
        return self

    def load(self, path):
        """Load a private copy of path (parallel sessions would clash on the lock file of one file)."""
        import uno
        from com.sun.star.beans import PropertyValue
        own = os.path.join(self.profile, os.path.basename(path))
        shutil.copyfile(path, own)
        doc = self.desktop.loadComponentFromURL(uno.systemPathToFileUrl(own), '_blank', 0,
                                                (PropertyValue(Name='Hidden', Value=True),))
        if doc is None:
            raise RuntimeError(f'LibreOffice could not load {path}')
        self.docs.append(doc)
        return doc

    @staticmethod
    def calc(doc):
        doc.calculateAll()
        doc.calculateAll()       # v7.1: one calculateAll leaves differences of up to 2e-3 (stored results, fiscal
                                 # impulse): every recalculation is two (excel_ai/NORMS.md 3i.2)

    @staticmethod
    def grid(doc, sheet, r0, c0, r1, c1):
        sh = doc.Sheets.getByName(sheet)
        return Grid(r0, c0, sh.getCellRangeByPosition(c0 - 1, r0 - 1, c1 - 1, r1 - 1).getDataArray())

    @staticmethod
    def set_value(doc, sheet, r, c, v):
        doc.Sheets.getByName(sheet).getCellByPosition(c - 1, r - 1).setValue(v)

    @staticmethod
    def copy_cells(doc, sheet, r0, r1, c_from, c_to):
        """Copy rows r0..r1 of column c_from to column c_to (values and types, as a user's copy-paste)."""
        sh = doc.Sheets.getByName(sheet)
        src = sh.getCellRangeByPosition(c_from - 1, r0 - 1, c_from - 1, r1 - 1).getRangeAddress()
        sh.copyRange(sh.getCellByPosition(c_to - 1, r0 - 1).getCellAddress(), src)

    def __exit__(self, *exc):
        for d in self.docs:
            try:
                d.close(True)
            except Exception:
                pass
        try:
            self.desktop.terminate()
        except Exception:
            pass
        try:
            self.proc.wait(timeout=30)
        except subprocess.TimeoutExpired:
            self.proc.kill()
        shutil.rmtree(self.profile, ignore_errors=True)
        return False


def run_worker(k, path, spec, inbox, outbox):
    """Child process k of a parallel run (spawned; pyuno serialises threads, so one process per session): load path;
    session 0 reports the cells spec['first'] names (('first', [grid data, ...])); every session waits for its
    ('set', [(sheet, row, col, value), ...]) message, writes the values, then for each run of spec['plan'][k]
    (key, [(sheet, r0, r1, col_from, col_to), ...]) copies the cells, recalculates and reports ('grid', key, data)
    of the range spec['read']; finally ('done', k), or ('error', k, traceback)."""
    import traceback
    try:
        with Session() as s:
            doc = s.load(path)
            if k == 0:
                outbox.put(('first', [s.grid(doc, *rng).data for rng in spec['first']]))
            msg = inbox.get(timeout=1800)
            if msg[0] != 'set':
                return
            for sheet, r, c, v in msg[1]:
                s.set_value(doc, sheet, r, c, v)
            s.calc(doc)          # v7.0: a recalculation after loading, before the first definition
            for key, copies in spec['plan'][k]:
                for sheet, r0, r1, cf, ct in copies:
                    s.copy_cells(doc, sheet, r0, r1, cf, ct)
                s.calc(doc)
                outbox.put(('grid', key, s.grid(doc, *spec['read']).data))
        outbox.put(('done', k))
    except BaseException:
        outbox.put(('error', k, traceback.format_exc()))


class ValuesSheet(Grid):
    """Recalculated values of a sheet's used range, read like an openpyxl data_only sheet: title, max_row,
    max_column, cell(r, c).value (None outside the range or empty)."""

    def __init__(self, title, data):
        super().__init__(1, 1, data)
        self.title = title
        self.max_row, self.max_column = len(data), len(data[0]) if data else 0

    def cell(self, r, c):
        if 1 <= r <= self.max_row and 1 <= c <= self.max_column:
            return super().cell(r, c)
        return _Cell(None)

    def iter_rows(self, min_row=1, max_row=None, min_col=1, max_col=None, values_only=False):
        """As openpyxl: rows of values (values_only) or of cells; empty cells None."""
        max_row, max_col = max_row or self.max_row, max_col or self.max_column
        for r in range(min_row, max_row + 1):
            row = tuple(self.cell(r, c) for c in range(min_col, max_col + 1))
            yield tuple(c.value for c in row) if values_only else row


class ValuesBook(dict):
    """{sheet name: ValuesSheet}, read like an openpyxl data_only workbook (book['Mitigation'])."""


def _read(doc, sheets):
    """Used ranges of the sheets named (all if None) and the cells holding an error value [(sheet, ranges)]."""
    data, errs = {}, []
    for name in doc.Sheets.ElementNames:
        sh = doc.Sheets.getByName(name)
        q = sh.queryFormulaCells(4)                    # com.sun.star.sheet.FormulaResult.ERROR
        if q.getCount():
            errs.append((name, q.getRangeAddressesAsString()))
        if sheets is None or name in sheets:
            cur = sh.createCursor()
            cur.gotoEndOfUsedArea(False)
            a = cur.getRangeAddress()
            data[name] = sh.getCellRangeByPosition(0, 0, a.EndColumn, a.EndRow).getDataArray()
    return data, errs


def values_worker(path, sheets, outbox):
    import traceback
    try:
        with Session() as s:
            doc = s.load(path)
            s.calc(doc)          # v6.0: a full recalculation after loading shows circular references (Err:522), which
            outbox.put(('ok',) + _read(doc, sheets))   # loading alone does not (v6.0 I47: found by the stored results)
    except BaseException:
        outbox.put(('error', traceback.format_exc()))


def start_values(path, sheets=None, timeout=1800):
    """Recalculate path in a spawned LibreOffice session (loading recalculates) while the caller goes on; returns
    a function that waits and returns (ValuesBook of the sheets named, or all; error cells [(sheet, ranges)])."""
    import multiprocessing as mp
    ctx = mp.get_context('spawn')
    q = ctx.Queue()
    p = ctx.Process(target=values_worker, args=(path, set(sheets) if sheets else None, q), daemon=True)
    p.start()

    def wait():
        try:
            msg = q.get(timeout=timeout)
        finally:
            p.join(30)
            if p.is_alive():
                p.terminate()
        if msg[0] != 'ok':
            raise RuntimeError(f'LibreOffice session failed:\n{msg[1]}')
        return ValuesBook({k: ValuesSheet(k, v) for k, v in msg[1].items()}), msg[2]
    return wait


_F = re.compile(r'(<f(?:\s[^>]*)?>)(.*?)(</f>)', re.S)
_ROW = re.compile(r'(<row\s[^>]*[^/]>)(.*?)(</row>)', re.S)
_CELL = re.compile(r'<c r="([A-Z]+)(\d+)"([^>]*?)(?:/>|>(.*?)</c>)', re.S)
_ESC = lambda x: x.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')


def _col(letters):
    n = 0
    for ch in letters:
        n = n * 26 + ord(ch) - 64
    return n


def _letters(n):
    s = ''
    while n:
        n, r = divmod(n - 1, 26)
        s = chr(65 + r) + s
    return s


def _paste_xml(xml, c0, c1, dests, shift, overwrite=False):
    """A user's copy-paste in the sheet XML: the cells of columns c0..c1 copied to the columns starting at each of
    dests (right of every existing cell), formulas shifted by shift(formula, columns) as Excel's paste does.
    v6.6: overwrite=True pastes over existing cells (the plain twin of the LAMBDA group: group 1 over group 2)."""
    width = c1 - c0 + 1

    def cell_xml(col, r, attrs, inner):
        return f'<c r="{_letters(col)}{r}"{attrs}>{inner}</c>' if inner else f'<c r="{_letters(col)}{r}"{attrs}/>'

    def row(m):
        cells = _CELL.findall(m.group(2))
        if not overwrite:
            assert all(_col(c) < min(dests) for c, *_x in cells), 'paste target not empty'
        src = [(_col(c), r, attrs, inner) for c, r, attrs, inner in cells if c0 <= _col(c) <= c1]
        add = []
        for d in dests:
            for col, r, attrs, inner in src:
                inner = _F.sub(lambda f: f.group(1) + _ESC(shift('=' + html.unescape(f.group(2)), d - c0)[1:])
                               + f.group(3), inner or '')
                add.append((col + d - c0, r, attrs, inner))
        if not overwrite:
            return m.group(1) + m.group(2) + ''.join(cell_xml(*x) for x in add) + m.group(3)
        hit = lambda col: any(d <= col < d + width for d in dests)
        keep = [(_col(c), r, attrs, inner) for c, r, attrs, inner in cells if not hit(_col(c))]
        allc = sorted(keep + add, key=lambda x: x[0])
        return m.group(1) + ''.join(cell_xml(*x) for x in allc) + m.group(3)
    return _ROW.sub(row, xml)


def expanded_zip(src, call, expand, pastes=None, shift=None, overwrite=False):
    """The copy LibreOffice recalculates (check variant 'expand': LAMBDA calls expanded), written from the file's
    XML: every <f> element whose formula matches call (the LAMBDA call pattern) gets expand(formula). A few seconds,
    no openpyxl load (same formulas as variant 'expand': checked on all 422,845 formulas of v4.9). pastes: {sheet:
    (first column, last column, [destination first columns])} copy-pasted in the XML, formulas shifted by shift
    (the paste test: scenario group 2 pasted to the right)."""
    def fix(m):
        f = '=' + html.unescape(m.group(2))
        if not call.search(f):
            return m.group(0)
        return m.group(1) + _ESC(expand(f)[1:]) + m.group(3)
    dst = os.path.join(tempfile.mkdtemp(), 'expand' + os.path.splitext(src)[1])
    with zipfile.ZipFile(src) as zin, zipfile.ZipFile(dst, 'w', zipfile.ZIP_DEFLATED, compresslevel=1) as zout:
        part_of = {}
        if pastes:
            wbx, rels = zin.read('xl/workbook.xml').decode(), zin.read('xl/_rels/workbook.xml.rels').decode()
            target = {m.group(1): m.group(2) for m in re.finditer(r'<Relationship[^>]*Id="([^"]+)"[^>]*Target="([^"]+)"',
                                                                 rels)}
            target.update({m.group(2): m.group(1) for m in re.finditer(r'<Relationship[^>]*Target="([^"]+)"[^>]*'
                                                                       r'Id="([^"]+)"', rels)})
            for m in re.finditer(r'<sheet [^>]*name="([^"]+)"[^>]*r:id="([^"]+)"', wbx):
                if html.unescape(m.group(1)) in pastes:
                    part_of['xl/' + target[m.group(2)].split('xl/')[-1].lstrip('/')] = pastes[html.unescape(m.group(1))]
        for item in zin.infolist():
            data = zin.read(item.filename)
            if item.filename.startswith('xl/worksheets/sheet') and item.filename.endswith('.xml'):
                xml = _F.sub(fix, data.decode('utf-8'))
                if item.filename in part_of:
                    xml = _paste_xml(xml, *part_of[item.filename], shift, overwrite)
                    xml = re.sub(r'<dimension ref="[^"]*"/>', '', xml, count=1)   # recomputed by the reader
                data = xml.encode('utf-8')
            zout.writestr(item, data)
    return dst
