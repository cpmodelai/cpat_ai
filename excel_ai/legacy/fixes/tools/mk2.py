import json
s=open('render.js').read()
s=s.replace("const A=JSON.parse(fs.readFileSync('partA.json')), B=JSON.parse(fs.readFileSync('partB.json'));",
 "const CFG=JSON.parse(fs.readFileSync(process.argv[3])); const A=JSON.parse(fs.readFileSync(CFG.data));")
a=s.index("const intro=["); b=s.index("];",a)+2
intro = r"""const intro=[
 new Paragraph({heading:HeadingLevel.TITLE,children:[new TextRun({text:CFG.title,font:FONT})]}),
 P('Workbook: CPAT 1.0pre_456_NoPropData.xlsb, sheet Mitigation unless stated. Prepared from the formulas stored in the file (defined names recovered from the .xlsb) and its cached Egypt values. Bug IDs are those of the repo register (excel_ai/working_version/LegacyBugFixes_v3_8.md). Companion documents: '+CFG.others+'.'),
 H1('How to apply every fix'),
 bullet([R('Work in a copy of the workbook and fix one bug at a time (excel_ai/legacy/fixes/procedure/BugFixProcedure.md; macro template FixL1_ServicesElectricity.bas).')]),
 bullet([R('Year columns: K = 2021, L = 2022, M = 2023 … AE = 2041. Type the new formula in the cell named, then drag right as stated under "Fill".')]),
 bullet([R(CFG.policy)]),
 bullet([R('Recalculate fully, check that legacy check cells (e.g. B6602, B7640) still read "OK", and compare with the expected effect.')]),
 ...CFG.extra.map(t=>bullet([R(t)])),
];"""
s=s[:a]+intro+s[b:]
s=s.replace("const all=[...A,...B];","const all=A;")
a=s.index("children:[...intro,"); b=s.index("]}]});",a)
s=s[:a]+"children:[...intro,H1('Summary'),P(CFG.summary),summary(all),H1(CFG.section),P(CFG.order),...A.flatMap(bugBlock)"+s[b:]
# H1 is defined after intro in render.js; move H1 definition before intro
h1="const H1=(t)=>new Paragraph({heading:HeadingLevel.HEADING_1,spacing:{before:360,after:120},children:[new TextRun({text:t,font:FONT})]});"
s=s.replace(h1,"",1); s=s.replace("const intro=[",h1+"\nconst intro=[",1)
open('render2.js','w').write(s)
pol="Policy block: copy the fixed baseline row and Paste Special → Formulas onto the policy row given (+6,331 rows for every row in this document; rows above 2173 are shared and have no policy copy)."
cfgs={
'power':dict(data='partA.json',title='Legacy CPAT bug fixes: engineer power model',others='the engineer road-transport plan and the other-mitigation plan',policy=pol,
 extra=["Expected effects from the repo's Python copy of the legacy power model (power_model_ref_v3_8.py, which matches the cached legacy rows to 1e-13; price feedback to other sectors excluded). Nothing was recalculated in Excel."],
 summary='12 bugs in sections D6 and H-L: 10 that change results and 2 minor defects (L11, L12). All 10 result-changing fixes together: 2040 generation +12.6% (baseline) and +9.2% (carbon-tax run).',
 section='Fixes',order='Suggested order: L1, L3, L2 (demand), then L5, L6, then the Low items.'),
'transport':dict(data='partT.json',title='Legacy CPAT bug fixes: engineer road-transport model',others='the engineer power model plan and the other-mitigation plan',policy=pol,
 extra=["The legacy Egypt run uses the elasticity road model (TrModel = Elasticity), so none of these fixes changes the default Egypt results; they change the engineer run (switch TrModel to Engineer to test).",
        "Expected effects: Egypt engineer baseline 2035 with legacy inputs, each fix alone, from the repo's Python copy of the legacy engineer road model (transport_model_ref_v3_8.py, which reproduces the cached legacy engineer run). Nothing was recalculated in Excel.",
        "Survey IDs (B1-B23) refer to excel_ai/mitigation/Transport_Legacy_Survey_v3_8.md section 5."],
 summary='17 bugs of the engineer road model (rows 2017-5378). L27 (ownership calibration) and L38 (used-vehicle depreciation) change the engineer results most.',
 section='Fixes',order='Suggested order: L27, L28, L29 (vehicle stock), L38, L37, L41, L35 (purchase choice), L30, L31, L33, L34 (fuel use and distance), then the rest.'),
'other':dict(data='partB.json',title='Legacy CPAT bug fixes: other mitigation bugs',others='the engineer power model plan and the engineer road-transport plan',
 policy="Policy block: copy the fixed baseline row and Paste Special → Formulas onto the policy row given. Up to row ~6070 the policy block is the baseline + 6,331 rows; from the other-energy-use block (row 6066) on it is + 6,317. A paste works in both cases except L43 (its formulas point back to driver rows at + 6,331), where the policy edit is spelled out.",
 extra=["Expected effects from cached Egypt values and the register. Nothing was recalculated in Excel."],
 summary='18 bugs from the register outside the two engineer models (L15 and L18 do not reproduce in this file; L22 needs new rows) and 2 new defects found while checking (N1, N2).',
 section='Fixes',order='Suggested order: L20, L24 (macro drivers), L13, L42, L43 (fuel use), L19, L21 (GHG), then the Low items.')}
for k,v in cfgs.items(): json.dump(v,open(f'cfg_{k}.json','w'))
