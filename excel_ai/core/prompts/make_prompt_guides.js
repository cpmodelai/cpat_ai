// Writes the Word guides for the module prompts (excel_ai/core/prompts/README.md):
//   node make_prompt_guides.js [outdir]       illustrated guides (screenshots from img/) in this folder
//   LITE=1 node make_prompt_guides.js <dir>   the same without screenshots (small, for e-mail)
// The prompt text of each guide is read from its .md file, so the guide and the prompt never differ.
const fs = require('fs');
const path = require('path');
const {
  Document, Packer, Paragraph, TextRun, HeadingLevel, ImageRun, AlignmentType, LevelFormat,
  Table, TableRow, TableCell, WidthType, BorderStyle, ShadingType, PageBreak,
} = require('docx');

const HERE = __dirname;
const OUT = process.argv[2] || HERE;
const LITE = !!process.env.LITE;
const DATE = '2026-10-29';
const GREEN = '00AE49';
const W = 9360;                       // text width, US Letter with 1" margins (DXA)

// ---------------------------------------------------------------- building blocks
const t = (text, o = {}) => new TextRun({ text, font: 'Arial', size: 21, ...o });
const P = (runs, o = {}) => new Paragraph({ spacing: { after: 120 }, ...o,
  children: (Array.isArray(runs) ? runs : [runs]).map(r => (typeof r === 'string' ? t(r) : r)) });
// inline `code` and **bold** in a plain string
const rich = s => s.split(/(`[^`]+`|\*\*[^*]+\*\*)/).filter(Boolean).map(x =>
  x.startsWith('`') ? t(x.slice(1, -1), { font: 'Consolas', size: 19 })
    : x.startsWith('**') ? t(x.slice(2, -2), { bold: true }) : t(x));
const para = s => P(rich(s));
const H1 = s => new Paragraph({ heading: HeadingLevel.HEADING_1, spacing: { before: 280, after: 120 },
  children: [t(s, { bold: true, size: 30, color: GREEN })] });
const H2 = s => new Paragraph({ heading: HeadingLevel.HEADING_2, spacing: { before: 200, after: 100 },
  children: [t(s, { bold: true, size: 24 })] });
const bullet = s => new Paragraph({ numbering: { reference: 'bul', level: 0 }, spacing: { after: 60 },
  children: rich(s) });
let numRef = 0;
const numbered = items => { numRef += 1; return items.map(s => new Paragraph({
  numbering: { reference: 'num', level: 0, instance: numRef }, spacing: { after: 60 }, children: rich(s) })); };
// a shaded box of monospace lines: the exact text to paste
const box = (text, size = 18) => {
  const lines = text.replace(/\r/g, '').split('\n');
  return new Table({ width: { size: W, type: WidthType.DXA }, columnWidths: [W], rows: [new TableRow({ children: [
    new TableCell({ width: { size: W, type: WidthType.DXA },
      shading: { type: ShadingType.CLEAR, fill: 'F2F2F2', color: 'auto' },
      margins: { top: 100, bottom: 100, left: 140, right: 140 },
      borders: Object.fromEntries(['top', 'bottom', 'left', 'right'].map(k =>
        [k, { style: BorderStyle.SINGLE, size: 6, color: 'BFBFBF' }])),
      children: lines.map(l => new Paragraph({ spacing: { after: 0 },
        children: [t(l.length ? l : ' ', { font: 'Consolas', size })] })) })] })] });
};
const table = (head, rows, widths) => new Table({ width: { size: W, type: WidthType.DXA }, columnWidths: widths,
  rows: [head, ...rows].map((r, i) => new TableRow({ tableHeader: i === 0, children: r.map((c, j) =>
    new TableCell({ width: { size: widths[j], type: WidthType.DXA },
      shading: i === 0 ? { type: ShadingType.CLEAR, fill: 'EBF1DE', color: 'auto' } : undefined,
      margins: { top: 60, bottom: 60, left: 100, right: 100 },
      children: [new Paragraph({ children: i === 0 ? [t(c, { bold: true, size: 19 })] : rich(c).map(x => x) })] })) })) });
const img = (file, caption) => {
  if (LITE) return [];
  const f = path.join(HERE, 'img', file);
  const buf = fs.readFileSync(f);
  const wpx = buf.readUInt32BE(16), hpx = buf.readUInt32BE(20);     // PNG header
  const w = 600, h = Math.round(hpx * w / wpx);
  return [new Paragraph({ alignment: AlignmentType.CENTER, spacing: { before: 80, after: 40 },
    children: [new ImageRun({ type: 'png', data: buf, transformation: { width: w, height: h },
      altText: { title: caption, description: caption, name: file } })] }),
  new Paragraph({ alignment: AlignmentType.CENTER, spacing: { after: 160 },
    children: [t(caption, { italics: true, size: 18, color: '595959' })] })];
};
const spacer = () => new Paragraph({ spacing: { after: 80 }, children: [] });

// ---------------------------------------------------------------- shared sections
function copilotSteps(m) {
  return [
    H1('4. Step by step in GitHub Copilot (local mode)'),
    para('"Local mode" means Copilot works on the CPAT-AI folder on your laptop (workspace **Current checkout**), not in a cloud copy. Everything it builds lands in `C:\\Users\\WB<PID>\\Repos\\CPAT-AI`, where you can open it in Excel, and you save it to GitHub yourself at the end (section 5).'),
    H2('Step 1. Open the repo folder (first time only)'),
    para('In the Copilot app sidebar, click **+** next to Projects, then **Open folder**, and pick `C:\\Users\\WB<PID>\\Repos\\CPAT-AI`. It stays in the sidebar.'),
    ...img('01_open_folder.png', 'Projects: + then Open folder'),
    H2('Step 2. Start a session in local mode'),
    para('Point at CPAT-AI in the sidebar and click the **+** next to it. Under the prompt box, open the workspace selector and choose **Current checkout** ("Work in the existing checkout"). Do not choose New worktree or Cloud.'),
    ...img('02_current_checkout.png', 'Workspace selector: Current checkout = local mode'),
    H2('Step 3. Pick the model'),
    para('Click the model chip under the prompt box, switch **Auto** off, then pick **Claude Opus** (the strongest model: this is a long, careful task). Effort: High if offered.'),
    ...img('03_model_chip.png', 'Model chip: Auto off, then Model'),
    H2('Step 4. Pick the mode'),
    para('Click the mode chip and pick **Interactive**: Copilot asks before it runs commands or edits files, and you approve each step. Do not use Autopilot for this task.'),
    ...img('04_mode_chip.png', 'Mode chip: pick Interactive'),
    H2('Step 5. Give it the prompt'),
    para(`You only type a short **starter prompt**. The long instructions are a file in the repo (\`excel_ai/core/prompts/${m.file}\`) that Copilot reads itself; the starter and the follow-up prompts are in \`excel_ai/core/prompts/${m.starter}\` and in section 1.`),
    para(`Option A (the prompt file is in your checkout): type **@**, pick \`AGENTS.md\`, type **@** again, pick \`excel_ai/core/prompts/${m.file}\`, then add the words below and press Enter.`),
    box(`@AGENTS.md @excel_ai/core/prompts/${m.file} Follow these files. Do phase 0 only, then stop and report.`, 19),
    spacer(),
    para('Option B (the file is not in your checkout yet, or you prefer to paste): copy the whole text of **Appendix A** into the prompt box, after `@AGENTS.md `, and press Enter.'),
    ...img(`05_prompt_box_${m.key}.png`, 'The prompt box with both files attached (illustration)'),
    H2('Step 6. Let it work, approve each step, read the report'),
    para('Copilot reads the documents, runs commands and asks for approval. Approve reading files and running Python; refuse anything that would delete files, change `excel_ai/bugs_and_legacy/` or push to GitHub. When it stops, it reports what it did, the bugs and issues it registered, and the decisions it needs from you. Answer the decisions in plain words before going on.'),
    ...img('06_session_at_work.png', 'A session at work: the steps on the left, the plan on the right'),
    H2('Step 7. The next phases, one message each'),
    para('Send these one at a time. Read each report and check it (the third column) before sending the next.'),
    table(['Send', 'What it does', 'Check before going on'], m.phases, [2300, 3700, 3360]),
    spacer(),
    para('More example follow-ups (answering its decisions, asking for an explanation, a failing check, stopping and resuming in a new session): **section 1**.'),
    H2('Step 8. Look at the changes'),
    para('Type `Show me the changes before you save them.` or open **Changes** under the prompt box: every edited file as a diff. Open the new workbook in Excel 365 (enable macros) and look at it. Do not edit a built workbook by hand: ask Copilot to change the builder and rebuild.'),
    ...img('07_changes_view.png', 'The Changes view: every edit as a diff before you keep it'),
  ];
}

function syncSection(m) {
  return [
    H1('5. When done: save to GitHub with SyncRepo.bat'),
    para('Copilot does not commit unless you ask (AGENTS.md). When the last phase is done and you are happy with the result, save everything to GitHub with the sync script in the repo folder.'),
    ...numbered([
      '**Close** every workbook of the repo in Excel (an open file cannot be committed cleanly).',
      'In File Explorer, go to `C:\\Users\\WB<PID>\\Repos\\CPAT-AI` and **double-click `SyncRepo.bat`**.',
      'It switches to `main`, pulls everyone else\'s changes, and lists the files you changed. **Read the list**: no workbook or export with real (proprietary) data may be in it (only dummy or public data are committed).',
      `Type a short commit message, for example \`${m.commit}\`, and press Enter.`,
      'It commits, pushes to `main` and shows **Pushed.** Press any key to close the window.',
      'Check on github.com/cpmodelai/cpat_ai that your commit is the latest one.',
    ]),
    ...img('08_explorer_syncrepo.png', 'The CPAT-AI folder: double-click SyncRepo.bat (illustration)'),
    ...img('09_syncrepo_console.png', 'SyncRepo.bat at work: pull, list of changes, your message, push (illustration)'),
    para('Other ways: from a terminal in the repo folder, `SyncRepo.bat "your message"` skips the question; `SyncAllRepos.bat` in the Repos folder syncs every repo; or tell Copilot `Commit and push with a clear message.`'),
    para('If it stops with **[ERROR] Could not switch to main**, Copilot left work on another branch: ask Copilot "Merge this branch into main locally and switch to main", then run SyncRepo.bat again. If it stops with a **merge conflict** or a failed push, use GitHub Desktop (Setup guide, Part 4) or ask Copilot to resolve the merge; for a binary file (Excel, Word) keep one whole version.'),
  ];
}

function common(m, intro) {
  return [
    new Paragraph({ spacing: { after: 60 }, children: [t(m.title, { bold: true, size: 36, color: GREEN })] }),
    new Paragraph({ spacing: { after: 200 }, children: [t(`CPAT-AI · repo github.com/cpmodelai/cpat_ai · prompt file excel_ai/core/prompts/${m.file} · ${DATE}`, { size: 18, color: '595959' })] }),
    ...(LITE ? [para(`This copy has no screenshots (to keep it small for e-mail). The illustrated copy, with the same text: \`${m.docx}\`.`)] : []),
    H1('1. Example queries'),
    ...mdBlocks(m.starter),
    ...intro,
  ];
}

function before(m) {
  return [
    H1('3. Before you start'),
    ...[
      'The Setup guide (`other/SetupGuide.docx`) Parts 1 and 3 are done: Git, the GitHub Copilot app signed in, the repo in `C:\\Users\\WB<PID>\\Repos\\CPAT-AI`.',
      'The repo is up to date: double-click `SyncRepo.bat` once before you start (section 5).',
      `The prompt file \`excel_ai/core/prompts/${m.file}\` is in your checkout after you sync (it is on main); if not, use Appendix A (the same text).`,
      'Time and credits: each phase is a long task. Send one phase, read the report, then the next. Type `/context` to see the credits used.',
      ...m.before,
    ].map(bullet),
    para('**Optional** (not needed to start): Copilot runs the builders and checks with Python and recalculates the workbooks in LibreOffice. If either is missing on your desktop, the prompt tells Copilot to say so, install nothing without your OK, and list what it could not run; you then review the workbook in Excel 365.'),
  ];
}

function appendix(m) {
  return [
    new Paragraph({ children: [new PageBreak()] }),
    H1('Appendix A. The prompt (exact text)'),
    para(`The full content of \`excel_ai/core/prompts/${m.file}\`. Paste all of it (Step 5, option B).`),
    box(fs.readFileSync(path.join(HERE, m.file), 'utf8').trim(), 18),
    new Paragraph({ children: [new PageBreak()] }),
    H1('Appendix B. Getting set up with AI in the Climate-Fiscal Team'),
    para('The text of the team\'s setup guide (`other/SetupGuide.docx`; written to `setup_guide.md` by `make_quick_guides.py`).'),
    ...mdBlocks('setup_guide.md'),
  ];
}

function repoBrief() {
  return [
    H1('6. The repo in brief (github.com/cpmodelai/cpat_ai)'),
    para('Four documents to know:'),
    ...[
      '`README.md`: start here; what is where and who reads what.',
      '`AGENTS.md`: the instructions every AI follows; attach it to every prompt.',
      '`NORMS.md`: the rules. Section 0: never replicate a legacy bug; always replicate a legacy issue, and register both. Section 9: how the modules work. Section 1: the column layout.',
      '`CAVEATS.md`: the log of every finished task (newest at the bottom); read it before building on earlier work.',
    ].map(bullet),
    para('Also useful: `excel_ai/core/BUGS.md` and `excel_ai/core/ISSUES.md` (the legacy bugs and issues found so far), `QuickStart.docx` (a short orientation for people), `excel_ai/core/prompts/` (these prompts).'),
  ];
}

// a markdown file (the starter prompts, the setup guide) as headings, paragraphs, lists and one box per code block
function mdBlocks(file) {
  const out = [];
  let code = null;
  for (const line of fs.readFileSync(path.join(HERE, file), 'utf8').split('\n')) {
    const s = line.trim();
    if (line.startsWith('```')) {
      if (code === null) code = [];
      else { out.push(box(code.join('\n'), 18), spacer()); code = null; }
    } else if (code !== null) code.push(line);
    else if (s.startsWith('## ')) out.push(H2(s.slice(3)));
    else if (s.startsWith('# ') || s.startsWith('<!--') || !s) continue;
    else if (s.startsWith('- ')) out.push(bullet(s.slice(2)));
    else if (/^\|[\s|:-]+\|$/.test(s)) continue;
    else if (s.startsWith('|')) out.push(para(s.replace(/^\||\|$/g, '').split('|').map(c => c.trim()).join(' · ')));
    else out.push(para(s.replace(/\[([^\]]+)\]\([^)]+\)/g, '$1').replace(/(^|\s)\*([^*]+)\*(?=\s|$|[.,;:])/g, '$1$2')));
  }
  return out;
}

// ---------------------------------------------------------------- the three guides
const PHASES = (rows) => rows.map(([n, what, check]) => [`Go ahead with phase ${n}.`, what, check]);

const TCB = {
  key: 'TCB', file: 'TCB_module_prompt.md', starter: 'TCB_starter_prompts.md',  docx: 'CPAT-AI_Prompt_TransportCobenefits.docx',
  title: 'Transport co-benefits module: the prompt and how to run it',
  commit: 'Transport co-benefits module v0.1.0',
  phases: PHASES([
    ['1', 'Python reference `tcb_ref.py`: legacy equations, both modes, fixes on and off', 'Legacy mode with fixes off reproduces the cached Egypt values (plan section 4); the effect of each fix is listed'],
    ['2', 'Data: Transport1, Tran_Elast, the Transport literals as TransportParams, in `data/transport_cobenefits/`', 'Tables unchanged from legacy; tests pass; public data only'],
    ['3', 'The workbook and its builder, with Cover, From and To tabs, the macros', 'Opens in Excel without a repair prompt; Mitigation column layout; both modes switch'],
    ['4', '`check_tcb.py` and its report', 'PASS; welfare 0 in scenario 1; ToMitigation matches Mitigation\'s FromTransportCB'],
    ['5', 'Release to `excel_ai/`, `active_workbooks/`; README, method note, CAVEATS, TODO, register', '`_latest` in `active_workbooks/`; CAVEATS entry at the bottom'],
  ]),
  before: ['Read the transport co-benefits plan `excel_ai/core/plans/Transport_cobenefits.md` section 7 (decisions D1-D9): Copilot will ask you about them.'],
};
const AP = {
  key: 'AP', file: 'AP_module_prompt.md', starter: 'AP_starter_prompts.md',  docx: 'CPAT-AI_Prompt_AirPollution.docx',
  title: 'Air pollution module: the prompt and how to run it',
  commit: 'Air pollution module v0.1.0',
  phases: PHASES([
    ['1', 'Python reference `ap_ref.py`: the legacy chain from emissions to valuation and unit costs', 'Fixes off reproduces the cached legacy values; the effect of each fix is listed'],
    ['2', 'Data step: data tabs in legacy layout, country and method selection', 'All-country clone test passes; no proprietary data'],
    ['3', 'The calculation sheet, ToMitigation and ToTransportCB, the builder and macro', 'Opens in Excel without a repair prompt; Mitigation column layout; kt converted to t once'],
    ['4', '`check_ap.py` and its report, with the option sweep', 'PASS; differences from Mitigation\'s typed FromAirPollution values explained'],
    ['5', 'Release, README, method, CAVEATS, TODO, register', '`_latest` in `active_workbooks/`; the old Standalone copy removed'],
  ]),
  before: ['Read `excel_ai/core/plans/Air_pollution.md` section 7 (decisions, above all B1): Copilot will ask you about them.'],
};
const DIST = {
  key: 'Distribution', file: 'Distribution_module_prompt.md', starter: 'Distribution_starter_prompts.md',  docx: 'CPAT-AI_HowTo_Distribution.docx',
  title: 'Distribution module: how to use it, and the prompt to update it',
  commit: 'Distribution module v0.1.4: permalink_countryeditable link, legacy 465 check',
  phases: PHASES([
    ['1', 'The macro looks for the mitigation workbook in `active_workbooks/` first; Cover shows the file used', 'The macro test and the VBA name scan pass'],
    ['2', 'Legacy check on 465, decile by decile, through `distribution_ref.py`', 'Every difference explained by a registered bug or issue'],
    ['3', 'Release v0.1.4: rebuild, `check_distribution.py`, publish, README, CAVEATS, TODO', 'PASS; `_latest` in `active_workbooks/`'],
  ]),
  before: ['Victor and Faustyna: you do not need Copilot to use the module (section 2b). The prompt is for changes to it.'],
};

const tcbIntro = [
  H1('2. What this does'),
  para('Builds the **transport co-benefits module** (accidents, congestion and road damage) as a free-standing workbook, `CPAT-AI-Transport-Cobenefits-Prototype_v0.1.0.xlsm`, that reproduces the legacy `Transport` sheet of CPAT 1.0pre_465. It follows the module rules of `NORMS.md` section 9: inputs only through the tabs `FromMitigation` (Mitigation section 5b, the road engineer model) and `FromAirPollution` (VSL and earnings), outputs only through `ToMitigation`; the same column layout as the Mitigation sheet; links to the other modules through the files in `excel_ai/active_workbooks/` (then `active_workbooks/`).'),
  para('**Legacy rule** (`NORMS.md` section 0): legacy bugs are never replicated; they are fixed and added to the register (L codes). Legacy issues are always replicated, and added to the register (I codes). Bug candidates that need your decision (B-c value of time, B-d road-damage fuel economy, B-e earnings deflator) are replicated as issues and listed for you.'),
  H2('The two modes (setting TcbMode)'),
  table(['Mode', 'Vehicle-km, fuel economy, class splits', 'Road fuel shares', 'Consistent?'], [
    ['`Legacy` (default)', 'Engineer road model (Mitigation 5b), whatever TrModel is', 'Switched model (TrModel; Egypt default Elasticity)', '**No**, when TrModel = Elasticity (issue I100, replicated)'],
    ['`Engineer`', 'Engineer road model', 'Engineer model\'s own fuel use', 'Yes, with the engineer model; Cover warns if Mitigation does not run TrModel = Engineer'],
  ], [1700, 2800, 2560, 2300]),
  spacer(),
  para('**The legacy method is inconsistent (checked).** Legacy takes vehicle-km, fuel economy and the passenger/freight splits from the engineer road model even when TrModel = Elasticity (the default), while the road share of each fuel follows TrModel. For Egypt in 2031 the engineer vehicle-km fall by 8.6%, while the road fuel use the elasticity model computes falls by 12.9% (gasoline) and 14.3% (diesel): the welfare from accidents, congestion and road damage does not follow the fuel use modelled. This was found in the review of 2026-10-29 (register issue I100, `excel_ai/core/plans/Transport_cobenefits.md` section 1.3); phase 0 of the prompt re-checks it on legacy 465.'),
];
const apIntro = [
  H1('2. What this does'),
  para('Finishes the **air pollution module** that was started (the recovered v0.3 scaffold in `excel_ai/air_pollution/`: Cover, inputs from Mitigation and nine legacy data tables, no calculations yet). The result is a free-standing workbook, `CPAT-AI-Air-Pollution-Prototype_v0.1.0.xlsm`, that reproduces the legacy `Air pollution` sheet (concentrations, exposure, health burden, valuation, unit externalities per fuel) of CPAT 1.0pre_465.'),
  para('It follows `NORMS.md` section 9: inputs only through `FromMitigation` (Mitigation section 15: emissions by pollutant and sector, in kt, converted to tonnes once), outputs only through `ToMitigation` (the rows of Mitigation\'s tab `FromAirPollution`) and `ToTransportCB` (VSL and daily earnings for the transport co-benefits module); the same column layout as the Mitigation sheet; links through `excel_ai/active_workbooks/` (then `active_workbooks/`).'),
  para('**Legacy rule** (`NORMS.md` section 0): bugs fixed and registered (L), issues replicated and registered (I). The scaffold was written on legacy 459; phase 0 reconciles it with 465, the latest legacy file. Bugs that need your decision (B1 adult-disease incidence, B14 "Transfer from OECD", I-d manual VSL units) are replicated as issues and listed for you.'),
];
const distIntro = [
  H1('2. What this is'),
  para('The **distribution module** already exists: `excel_ai/CPAT-AI-Distribution-Prototype_v0.1.3.xlsm`, household effects of a mitigation scenario by income decile in one analysis year, replicating the legacy `Distribution` sheet (bugs fixed and registered; issues replicated and registered). It is cut from the built mitigation prototype, so its formulas have one source (`excel_ai/mitigation/build.py`), and it reads Mitigation only through its tab `FromMitigation` (section 19a of the mitigation workbook, defined name `ExportDistn`).'),
  H2('2b. Using the module (no AI needed)'),
  ...numbered([
    'Open `CPAT-AI-Mitigation-Prototype_latest.xlsm` (in `excel_ai/active_workbooks/`), define the scenario, click Recalculate now, and save it (or leave it open).',
    'Open `CPAT-AI-Distribution-Prototype_latest.xlsm` from the same folder and enable macros.',
    'On Cover, click **Update from Mitigation**: it copies section 19a of the mitigation workbook into `FromMitigation` and recalculates. Cover shows the file used and its time.',
    'Read the results on `Distribution` (one column group per scenario, deciles across).',
    'Distribution settings of a scenario (analysis year, revenue recycling, targeting): `ScenarioDefinition`, then Recalculate now.',
  ]),
  ...img('10_distribution_cover.png', 'The Cover of the distribution module v0.1.3 (rendered from the file; the buttons are not shown)'),
  H2('2c. What the prompt does'),
  para('It does not rebuild the module. It (1) makes the macro look for the mitigation workbook in `active_workbooks/` first, as the module rules of `NORMS.md` section 9 require (today it looks in `active_workbooks/`); (2) checks the module against legacy 465 decile by decile and registers anything new; (3) fixes the Cover version table and releases v0.1.4. Phase 0 is a review only.'),
];

const GUIDES = [[TCB, tcbIntro], [AP, apIntro], [DIST, distIntro]];

async function main() {
  for (const [m, intro] of GUIDES) {
    numRef = 0;
    const children = [...common(m, intro), ...before(m), ...copilotSteps(m), ...syncSection(m), ...repoBrief(), ...appendix(m)];
    const doc = new Document({
      creator: 'CPAT-AI', title: m.title,
      styles: { default: { document: { run: { font: 'Arial', size: 21 } } },
        paragraphStyles: [
          { id: 'Heading1', name: 'Heading 1', basedOn: 'Normal', next: 'Normal', quickFormat: true,
            run: { size: 30, bold: true, font: 'Arial', color: GREEN }, paragraph: { spacing: { before: 280, after: 120 }, outlineLevel: 0 } },
          { id: 'Heading2', name: 'Heading 2', basedOn: 'Normal', next: 'Normal', quickFormat: true,
            run: { size: 24, bold: true, font: 'Arial' }, paragraph: { spacing: { before: 200, after: 100 }, outlineLevel: 1 } }] },
      numbering: { config: [
        { reference: 'bul', levels: [{ level: 0, format: LevelFormat.BULLET, text: '•', alignment: AlignmentType.LEFT,
          style: { paragraph: { indent: { left: 540, hanging: 270 } } } }] },
        { reference: 'num', levels: [{ level: 0, format: LevelFormat.DECIMAL, text: '%1.', alignment: AlignmentType.LEFT,
          style: { paragraph: { indent: { left: 540, hanging: 300 } } } }] }] },
      sections: [{ properties: { page: { size: { width: 12240, height: 15840 },
        margin: { top: 1440, right: 1440, bottom: 1440, left: 1440 } } }, children }],
    });
    const out = path.join(OUT, m.docx);
    fs.writeFileSync(out, await Packer.toBuffer(doc));
    console.log(out, fs.statSync(out).size);
  }
}
main();
