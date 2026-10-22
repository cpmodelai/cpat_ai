// Build documentation/CPAT-AI_Overview_v<version>.pptx, the one core deck of CPAT-AI (v7.1: the prototype
// overview and user guide merged with the management briefing; earlier decks in other/presentations/Old/).
// Legacy CPAT bugs up front (img/v71_legacy.json from make_legacy_fixes.py; register counts in v71_facts.json).
// Same style as v4.0: navy / teal / amber, Cambria headings, Calibri body. Screenshots and numbers:
// presentation/img/v71_*.png, v71_data.json, v71_facts.json and v71_transport.json from make_screenshots.py
// (rendered from the current workbook and its check reports).
//
//   PPTX_SKILL=<pptx skill dir> node presentation/build_deck.js
const fs = require("fs");
const path = require("path");
const pptxgen = require("pptxgenjs");
const { imageSize } = require("image-size");
const { applyTheme } = require(process.env.PPTX_SKILL + "/scripts/apply_theme.js");

const HERE = __dirname;
const IMG = (f) => path.join(HERE, "img", f);
const VER = require(path.join(HERE, "..", "version.json")).version, PFX = "v" + VER.replace(".", "");
const OUT = path.join(HERE, "..", "..", "releases", `CPAT-AI_Overview_v${VER}.pptx`);   // + _latest copy
const LATEST = path.join(HERE, "..", "..", "CPAT-AI_Overview_latest.pptx");
const DATA = JSON.parse(fs.readFileSync(IMG(`${PFX}_data.json`), "utf8"));
const FACTS = JSON.parse(fs.readFileSync(IMG(`${PFX}_facts.json`), "utf8"));
const LEG = JSON.parse(fs.readFileSync(IMG(`${PFX}_legacy.json`), "utf8"));
const TR = JSON.parse(fs.readFileSync(IMG(`${PFX}_transport.json`), "utf8"));
const BUGS = FACTS.bugs.mit + FACTS.bugs.dist, ISSUES = FACTS.issues.mit + FACTS.issues.dist;
const REG = `CPAT-AI_BugsAndIssues_v7.2.docx`;   // the register has its own version

const THEME = {
  name: "CPAT AI Mitigation",
  headFontFace: "Cambria",
  bodyFontFace: "Calibri",
  colors: {
    dk1: "1F1F2E", lt1: "FFFFFF", dk2: "1E2761", lt2: "F4F6FB",
    accent1: "1E2761", accent2: "0F7B6C", accent3: "E08A1E", accent4: "D4A24C",
    accent5: "5C667A", accent6: "D5DAE3", hlink: "0F7B6C", folHlink: "5C667A",
  },
};
const NAVY = "1E2761", TEAL = "0F7B6C", AMBER = "E08A1E", GOLD = "D4A24C", INK = "1F1F2E", GREY = "5C667A";
const CARD = "F4F6FB", LINE = "D5DAE3", TEAL_T = "EAF4F2", AMBER_T = "FDF3E6", ICE = "CADCFC";

const pres = new pptxgen();
pres.layout = "LAYOUT_WIDE";
pres.title = `CPAT-AI-Mitigation-Prototype v${VER}: overview, status, legacy bugs and user guide`;
pres.theme = { headFontFace: THEME.headFontFace, bodyFontFace: THEME.bodyFontFace };

pres.defineSlideMaster({
  title: "TITLE_DARK",
  background: { color: NAVY },
  objects: [
    { placeholder: { options: { name: "title", type: "title", x: 0.6, y: 1.55, w: 6.2, h: 1.6, fontFace: "Cambria",
      fontSize: 40, bold: true, color: "FFFFFF", valign: "top", align: "left", margin: 0 }, text: "" } },
  ],
});
pres.defineSlideMaster({
  title: "CONTENT",
  background: { color: "FFFFFF" },
  objects: [
    { placeholder: { options: { name: "label", type: "body", x: 0.6, y: 0.32, w: 12.1, h: 0.3, fontFace: "Calibri",
      fontSize: 11, bold: true, color: TEAL, charSpacing: 2, margin: 0 }, text: "" } },
    { placeholder: { options: { name: "title", type: "title", x: 0.6, y: 0.62, w: 12.1, h: 0.7, fontFace: "Cambria",
      fontSize: 30, bold: true, color: NAVY, valign: "top", align: "left", margin: 0 }, text: "" } },
    { text: { text: `CPAT-AI-Mitigation-Prototype v${VER}  ·  core deck  ·  screenshots and charts from the workbook`,
      options: { x: 0.6, y: 7.05, w: 9.5, h: 0.25, fontSize: 9, color: GREY, margin: 0 } } },
  ],
  slideNumber: { x: 12.3, y: 7.05, w: 0.5, h: 0.25, fontSize: 9, color: GREY, align: "right" },
});

let n = 0;
const nm = (s) => `${s}-${++n}`;
function header(slide, label, title) {
  slide.addText(label, { placeholder: "label" });
  slide.addText(title, { placeholder: "title" });
}
// picture fitted into a box (aspect ratio kept), centred horizontally in the box; returns the size used
function picture(slide, file, x, y, maxW, maxH, align = "center") {
  const d = imageSize(fs.readFileSync(IMG(file)));
  let w = maxW, h = maxW * d.height / d.width;
  if (h > maxH) { h = maxH; w = maxH * d.width / d.height; }
  const px = align === "center" ? x + (maxW - w) / 2 : x;
  slide.addShape(pres.shapes.RECTANGLE, { x: px - 0.06, y: y - 0.06, w: w + 0.12, h: h + 0.12, fill: { color: "FFFFFF" },
    line: { color: LINE, width: 1 }, shadow: { type: "outer", color: "1E2761", opacity: 0.18, blur: 6, offset: 2, angle: 90 },
    objectName: nm("frame") });
  slide.addImage({ path: IMG(file), x: px, y, w, h, objectName: nm("screenshot") });
  return { x: px, y, w, h };
}
function caption(slide, text, x, y, w) {
  slide.addText(text, { x, y, w, h: 0.3, fontSize: 12, italic: true, color: GREY, margin: 0, isTextBox: true,
    objectName: nm("caption") });
}
function badge(slide, txt, x, y, color, size = 0.42) {
  slide.addShape(pres.shapes.OVAL, { x, y, w: size, h: size, fill: { color }, line: { color }, objectName: nm("badge") });
  slide.addText(txt, { x, y, w: size, h: size, align: "center", valign: "middle", fontSize: 14, bold: true,
    color: "FFFFFF", margin: 0, isTextBox: true, objectName: nm("badgeText") });
}
function item(slide, num, head, body, x, y, w, color = TEAL, h = 1.0) {
  badge(slide, String(num), x, y, color);
  slide.addText([
    { text: head, options: { bold: true, fontSize: 15, color: INK, breakLine: true } },
    { text: body, options: { fontSize: 14, color: GREY } },
  ], { x: x + 0.6, y: y - 0.05, w: w - 0.6, h, valign: "top", margin: 0, isTextBox: true, objectName: nm("item") });
}
function card(slide, x, y, w, h, fill, lineC, runs) {
  slide.addShape(pres.shapes.RECTANGLE, { x, y, w, h, fill: { color: fill }, line: { color: lineC }, objectName: nm("card") });
  slide.addText(runs, { x: x + 0.18, y: y + 0.12, w: w - 0.36, h: h - 0.24, valign: "top", margin: 0, isTextBox: true,
    objectName: nm("cardText") });
}
function stat(slide, big, small, x, y, w, color = NAVY) {
  slide.addText([
    { text: big, options: { fontSize: 40, bold: true, color, fontFace: "Cambria", breakLine: true } },
    { text: small, options: { fontSize: 13, color: GREY } },
  ], { x, y, w, h: 1.5, valign: "top", margin: 0, isTextBox: true, objectName: nm("stat") });
}
function flow(slide, labels, y, color = NAVY) {
  const k = labels.length, gap = 0.4, w = (12.1 - gap * (k - 1)) / k;
  labels.forEach((t, i) => {
    const x = 0.6 + i * (w + gap);
    slide.addShape(pres.shapes.ROUNDED_RECTANGLE, { x, y, w, h: 0.62, rectRadius: 0.1, fill: { color }, line: { color },
      objectName: nm("flow") });
    slide.addText(t, { x, y, w, h: 0.62, align: "center", valign: "middle", fontSize: 14, bold: true, color: "FFFFFF",
      margin: 0, isTextBox: true, objectName: nm("flowText") });
    if (i < k - 1) slide.addShape(pres.shapes.RIGHT_ARROW, { x: x + w + 0.07, y: y + 0.17, w: gap - 0.14, h: 0.28,
      fill: { color: GOLD }, line: { color: GOLD }, objectName: nm("flowArrow") });
  });
}
const H = (t) => ({ text: t, options: { bold: true, fontSize: 11, color: TEAL, charSpacing: 2, breakLine: true } });
const HA = (t) => ({ text: t, options: { bold: true, fontSize: 11, color: AMBER, charSpacing: 2, breakLine: true } });
const BL = (t, last = false, size = 15) => ({ text: t, options: { bullet: true, fontSize: size, color: INK, breakLine: !last } });
const GAP = { text: " ", options: { fontSize: 8, breakLine: true } };
const CHART_TXT = { catAxisLabelColor: GREY, valAxisLabelColor: GREY, catAxisLabelFontSize: 11, valAxisLabelFontSize: 11,
  catAxisLabelFontFace: "+mn-lt", valAxisLabelFontFace: "+mn-lt", titleFontFace: "+mn-lt", legendFontFace: "+mn-lt" };
function lineChart(slide, series, x, y, w, h, title, colors, valFmt = "#,##0") {
  slide.addChart(pres.charts.LINE, series, {
    x, y, w, h, showTitle: true, title, titleFontSize: 14, titleColor: INK, chartColors: colors, lineSize: 2.5,
    lineDataSymbol: "none", showLegend: series.length > 1, legendPos: "b", legendFontSize: 11, legendColor: GREY,
    valGridLine: { color: "E3E7EF", size: 0.75 }, catGridLine: { style: "none" }, valAxisLabelFormatCode: valFmt,
    catAxisLabelFrequency: 3, catAxisLabelRotate: 315, ...CHART_TXT, objectName: nm("chart"),
  });
}
function barChart(slide, series, x, y, w, h, title, colors, valFmt = "#,##0") {
  slide.addChart(pres.charts.BAR, series, {
    x, y, w, h, barDir: "col", barGrouping: "clustered", chartColors: colors, showLegend: series.length > 1,
    legendPos: "b", legendFontSize: 11, legendColor: GREY, valAxisLabelFormatCode: valFmt, showTitle: true, title,
    titleFontSize: 14, titleColor: INK, valGridLine: { color: "E3E7EF", size: 0.75 }, catGridLine: { style: "none" },
    ...CHART_TXT, objectName: nm("chart"),
  });
}
// numbers from the workbook (v62_data.json): value of a stored scenario in a year
const years = DATA.years.map(String);
const at = (key, sid, year) => DATA[key][String(sid)][DATA.years.indexOf(year)];
const f0 = (v) => Math.round(v).toLocaleString("en-US");
const f1 = (v) => v.toLocaleString("en-US", { minimumFractionDigits: 1, maximumFractionDigits: 1 });
const pct = (v, d = 0) => `${(v * 100).toFixed(d)}%`;
const ids = ["1", "3", "4", "5"].filter((k) => DATA.co2[k]);
const short = { "1": "Baseline", "3": "Carbon price $20", "4": "Package A", "5": "Package B" };
const SCEN_COLORS = ["5C667A", "0F7B6C", "E08A1E", "1E2761"];

// 1. Title ------------------------------------------------------------------------------------------------------
pres.addSection({ title: "Overview" });
{
  const s = pres.addSlide({ masterName: "TITLE_DARK", sectionTitle: "Overview" });
  s.addText("OVERVIEW + USER GUIDE", { x: 0.6, y: 1.05, w: 6, h: 0.35, fontSize: 12, bold: true, color: GOLD,
    charSpacing: 3, margin: 0, isTextBox: true, objectName: nm("kicker") });
  s.addText("CPAT-AI-Mitigation-Prototype", { placeholder: "title" });
  s.addText("The CPAT mitigation and distribution modules as a readable Excel workbook, generated and checked by AI.",
    { x: 0.6, y: 3.25, w: 5.9, h: 1.2, fontSize: 18, color: ICE, valign: "top", margin: 0, isTextBox: true,
      objectName: nm("subtitle") });
  ["Plain formulas", "Checked by Python", `${BUGS} legacy bugs found`].forEach((t, i) => {
    const w = [1.9, 2.3, 2.6][i], x = [0.6, 2.6, 5.0][i];
    s.addShape(pres.shapes.ROUNDED_RECTANGLE, { x, y: 4.75, w, h: 0.45, rectRadius: 0.12, fill: { color: "2E3A7A" },
      line: { color: "3A4A8A" }, objectName: nm("chip") });
    s.addText(t, { x, y: 4.75, w, h: 0.45, align: "center", valign: "middle", fontSize: 13, color: "FFFFFF",
      margin: 0, isTextBox: true, objectName: nm("chipText") });
  });
  s.addText(`Version ${VER}, October 2026  ·  Egypt data  ·  prototype for discussion`, { x: 0.6, y: 6.8, w: 6.5,
    h: 0.3, fontSize: 10, color: ICE, margin: 0, isTextBox: true, objectName: nm("footnote") });
  const p = picture(s, `${PFX}_01_overview.png`, 7.9, 1.2, 4.8, 4.2);
  s.addText("The Mitigation tab as it opens: every section rolled up", { x: 7.9, y: p.y + p.h + 0.15, w: 4.8, h: 0.3,
    fontSize: 11, color: ICE, italic: true, margin: 0, isTextBox: true, objectName: nm("caption") });
  s.addNotes("One workbook for the CPAT mitigation chain (policies, prices, power, fuel use, revenues, emissions, "
    + "GDP) and the distribution module. Generated and checked by AI; every value is recomputed independently.");
}

// 1b. Where we are (from the management briefing, v6.3; updated to v7.2) -------------------------------------------
{
  const s = pres.addSlide({ masterName: "CONTENT", sectionTitle: "Overview" });
  header(s, "WHERE WE ARE", "Mitigation: substantial progress. Distribution: done.");
  card(s, 0.6, 1.5, 3.85, 2.95, TEAL_T, "C7E3DE", [
    H("MITIGATION"),
    BL("Prices, demand by 16 sectors and 8 fuels, power, road transport"),
    BL("Revenues, CO2, other GHGs, GDP effects, carbon rates"),
    BL("Checked against legacy CPAT and an independent Python recomputation", true),
  ]);
  card(s, 4.72, 1.5, 3.85, 2.95, CARD, LINE, [
    H("DISTRIBUTION"),
    BL("Household impacts as legacy, by decile"),
    BL("ASPIRE and poverty-line transfers, production-sector prices, charts"),
    BL(`All ${FACTS.bugs.dist} legacy distribution bugs fixed`, true),
  ]);
  card(s, 8.85, 1.5, 3.85, 2.95, AMBER_T, "F2D9B6", [
    HA("SINCE v6.3"),
    BL("Ships with its values: opens without recalculating"),
    BL("Dashboard: Live or Stored results, key table, charts"),
    BL(`${FACTS.links.length} data tabs linked to the data workbook`),
    BL("Codes on the CPAT code protocol (v7.2)"),
    BL("Every result checked again in a full check", true),
  ]);
  stat(s, String(BUGS), `legacy bugs found (${FACTS.bugs.mit} mitigation, ${FACTS.bugs.dist} distribution), none `
    + "replicated", 0.6, 4.75, 3.85, AMBER);
  stat(s, String(ISSUES), `legacy issues (${FACTS.issues.mit} mitigation, ${FACTS.issues.dist} distribution), `
    + "replicated and tracked", 4.72, 4.75, 3.85);
  stat(s, FACTS.codes, "output codes, checked against an independent Python recomputation", 8.85, 4.75, 3.85, TEAL);
  caption(s, `Source: CPAT-AI repo, release ${VER} and the bug and issue register (${REG}).`, 0.6, 6.6, 12.1);
  s.addNotes("Around it: quick start, equations, method notes, every formula listed; the bug register with cell-by-cell "
    + "fix plans for legacy CPAT; the Python model (Coded CPAT) shares the same codes. v7.2: every prototype code follows the "
    + "CPAT code protocol (legacy variable names, no model letters, tot for totals, each code once); the v7.1 stems stay "
    + "as aliases for one release.");
}

// 2. What it covers --------------------------------------------------------------------------------------------
{
  const s = pres.addSlide({ masterName: "CONTENT", sectionTitle: "Overview" });
  header(s, "WHAT IT IS", "Two tabs follow the CPAT mitigation and distribution chain");
  flow(s, ["1. Policies", "2. Prices", "3. Power", "5-8. Fuel use", "11-13. Energy, revenue, CO2",
    "14-18. GHGs, GDP, welfare"], 1.65);
  item(s, 1, "Policies and prices", "Carbon tax, ETS with a cap, feebates, excises, subsidy phase-outs, producer "
    + "subsidy reform, methane fee, regulations, existing carbon pricing.", 0.6, 2.75, 6.2);
  item(s, 2, "Power and fuel use", "The legacy power model with its engineer options; 16 sectors × 9 fuels; an "
    + "optional engineer road model.", 0.6, 3.95, 6.2);
  item(s, 3, "Results to 2041", "Fuel use, revenue by policy, CO2, GHGs with methane, NDC comparison, GDP effects, "
    + "welfare; distribution by decile.", 0.6, 5.15, 6.2);
  card(s, 7.1, 2.7, 5.6, 3.55, CARD, LINE, [
    H("IN THE WORKBOOK"),
    BL("Egypt data, 2022-2041; legacy data tabs paste in"),
    BL("Any number of scenarios, run by one macro"),
    BL("Distribution tab: one year, deciles across"),
    BL("The model in equations; every formula listed"),
    GAP,
    HA("NOT IN SCOPE"),
    BL("Air-pollution co-benefits module (dropped)"),
    BL("Transport externalities module (dropped)", true),
  ]);
  s.addNotes("The section numbers follow legacy CPAT. Equations: Equations.md; every workbook formula: "
    + "Formulas.md. Section 15 keeps the air-pollutant input table; the co-benefits and transport-externality "
    + "modules were dropped by the user on 2026-10-20.");
}

// 3. Legacy bugs ------------------------------------------------------------------------------------------------
{
  const s = pres.addSlide({ masterName: "CONTENT", sectionTitle: "Overview" });
  header(s, "LEGACY CPAT · FIXES NEEDED", `${BUGS} bugs found in legacy CPAT; ${LEG.counts.High} change today's results`);
  const rows = [[{ text: "ID", options: { bold: true, color: "FFFFFF", fill: { color: NAVY } } },
                 { text: "High-priority bug and its effect", options: { bold: true, color: "FFFFFF", fill: { color: NAVY } } }]]
    .concat(LEG.high.map((b) => [{ text: b.id, options: { bold: true, color: AMBER } }, { text: b.effect }]));
  s.addTable(rows, { x: 0.6, y: 1.5, w: 8.6, colW: [0.8, 7.8], fontSize: 12, color: INK, border: { type: "solid",
    color: LINE, pt: 0.75 }, rowH: 0.47, valign: "middle", margin: [2, 6, 2, 6], objectName: nm("bugTable") });
  stat(s, String(LEG.counts.High), "mitigation, high: wrong results in standard runs", 9.6, 1.55, 3.1, AMBER);
  stat(s, String(LEG.counts.Medium), "mitigation, medium: some runs or countries, or a reported number", 9.6, 3.1, 3.1);
  stat(s, `${LEG.counts.Low} + ${FACTS.bugs.dist}`, "mitigation low (latent or reporting) + distribution", 9.6, 4.65, 3.1, GREY);
  caption(s, `${FACTS.bugs.mit} mitigation and ${FACTS.bugs.dist} distribution bugs, all fixed in the prototype; also ${ISSUES} `
    + `legacy issues (${FACTS.issues.mit} mitigation, ${FACTS.issues.dist} distribution), replicated and tracked. `
    + `Fix plans: ${REG}.`, 0.6, 6.55, 12.1);
  s.addNotes("Generated from the register (issues_register.py, make_legacy_fixes.py). The prototype never "
    + "replicates a legacy bug; it replicates legacy issues and tracks them (NORMS section 0).");
}

// 4. Problems and fixes ------------------------------------------------------------------------------------------
{
  const s = pres.addSlide({ masterName: "CONTENT", sectionTitle: "Overview" });
  header(s, "WHAT CHANGES", "Four problems with today's Excel, four fixes");
  s.addText("TODAY IN CPAT", { x: 0.6, y: 1.5, w: 5.2, h: 0.3, fontSize: 11, bold: true, color: AMBER, charSpacing: 2,
    margin: 0, isTextBox: true, objectName: nm("colhead") });
  s.addText("IN THE prototype", { x: 6.7, y: 1.5, w: 6, h: 0.3, fontSize: 11, bold: true, color: TEAL, charSpacing: 2,
    margin: 0, isTextBox: true, objectName: nm("colhead") });
  const rows = [
    ["Hard to read: long formulas, many tabs", "Numbered sections, rolled up; every formula at most 100 characters"],
    ["Formulas differ from row to row", "One formula per block: copy, drag or paste it anywhere in the block"],
    ["New scenarios are slow to build", "Paste a scenario block, or list scenarios in ScenarioDefinition and run one macro"],
    ["Results are hard to verify", "Every value recomputed in Python; legacy bugs found, fixed and listed"],
  ];
  rows.forEach(([a, b], i) => {
    const y = 1.9 + i * 1.22;
    s.addShape(pres.shapes.RECTANGLE, { x: 0.6, y, w: 5.2, h: 1.02, fill: { color: AMBER_T }, line: { color: "F2D9B6" },
      objectName: nm("problem") });
    s.addText(a, { x: 0.8, y, w: 4.85, h: 1.02, fontSize: 16, color: INK, valign: "middle", margin: 0, isTextBox: true,
      objectName: nm("problemText") });
    s.addShape(pres.shapes.RIGHT_ARROW, { x: 5.95, y: y + 0.33, w: 0.6, h: 0.36, fill: { color: GOLD }, line: { color: GOLD },
      objectName: nm("arrow") });
    s.addShape(pres.shapes.RECTANGLE, { x: 6.7, y, w: 6.0, h: 1.02, fill: { color: TEAL_T }, line: { color: "C7E3DE" },
      objectName: nm("fix") });
    s.addText(b, { x: 6.9, y, w: 5.65, h: 1.02, fontSize: 16, color: INK, valign: "middle", margin: 0, isTextBox: true,
      objectName: nm("fixText") });
  });
  s.addNotes("Readability, copy-pasteable formulas, fast scenarios, and independent verification.");
}

// 5. The workbook ------------------------------------------------------------------------------------------------
pres.addSection({ title: "Using the workbook" });
{
  const s = pres.addSlide({ masterName: "CONTENT", sectionTitle: "Using the workbook" });
  header(s, "USER GUIDE · LAYOUT", "Years across, scenarios side by side, one formula per block");
  const p = picture(s, `${PFX}_01b_scenarios.png`, 0.6, 1.5, 12.1, 2.4);
  caption(s, "Each scenario is a block of columns: output codes, 2022 (beige), the years to 2041, a blank column.",
    0.6, p.y + p.h + 0.12, 12.1);
  const y0 = p.y + p.h + 0.6, hc = 1.5;
  card(s, 0.6, y0, 3.85, hc, CARD, LINE, [
    { text: "Paste a scenario", options: { bold: true, fontSize: 15, color: NAVY, breakLine: true } },
    { text: "Paste a block of columns to the right: it numbers itself and runs the next ScenarioDefinition column.",
      options: { fontSize: 14, color: INK } }]);
  card(s, 4.72, y0, 3.85, hc, TEAL_T, "C7E3DE", [
    { text: "One formula, at most 100 characters", options: { bold: true, fontSize: 15, color: TEAL, breakLine: true } },
    { text: `The same formula in every row of a block; all ${FACTS.formulas} formulas are short.`,
      options: { fontSize: 14, color: INK } }]);
  card(s, 8.85, y0, 3.85, hc, "EEECE1", "D9D4BC", [
    { text: "LAMBDAs in the live scenario", options: { bold: true, fontSize: 15, color: "9C0006", breakLine: true } },
    { text: "Group 1 (baseline) holds plain formulas; group 2 (the live scenario) calls the named LAMBDAs.",
      options: { fontSize: 14, color: INK } }]);
  s.addNotes("Every section is rolled up to its summary row on open; columns B:G and I:K are grouped. Row 5 holds the "
    + "scenario number (a formula); every input row looks up its value in that ScenarioDefinition column. Two groups "
    + "ship (v6.6); more by pasting group 2 to the right.");
}

// 6. Many scenarios ----------------------------------------------------------------------------------------------
{
  const s = pres.addSlide({ masterName: "CONTENT", sectionTitle: "Using the workbook" });
  header(s, "USER GUIDE · MANY SCENARIOS", "List scenarios, run one macro, compare");
  flow(s, ["Define in ScenarioDefinition", "Run stored scenarios", "StoredOutputs", "ScenarioCompare"], 1.6, TEAL);
  const p = picture(s, `${PFX}_06_definitions.png`, 0.6, 2.6, 6.0, 3.6, "left");
  caption(s, "ScenarioDefinition: one column per scenario, short name, Run? = Yes", 0.6, p.y + p.h + 0.12, 6);
  const q = picture(s, `${PFX}_05_compare.png`, 6.9, 2.6, 5.8, 3.6, "left");
  caption(s, "ScenarioCompare: key results vs the baseline (Live or Stored)", 6.9, q.y + q.h + 0.12, 5.8);
  s.addNotes("The macro copies each definition into the live column, recalculates, runs the ETS goal seek where "
    + "needed, and stores the results as values (StoredOutputs, sorted; every lookup by output code). The dashboard "
    + "reads Live (LiveOutputs) or Stored results; charts show only scenarios with results.");
}

// 6b. Speed, dashboard and data (v6.6-v7.1) -----------------------------------------------------------------------
{
  const s = pres.addSlide({ masterName: "CONTENT", sectionTitle: "Using the workbook" });
  header(s, "USER GUIDE · SPEED AND SIZE", "Half the recalculation time of legacy, about half the file size");
  stat(s, "5 s", "recalculation after a change (legacy CPAT: about 10 s); opens with its values, no recalculation",
    0.6, 1.6, 3.6, TEAL);
  stat(s, "10 MB", "binary (.xlsb) today; 12-13 MB expected with all countries and the remaining modules "
    + "(legacy CPAT: over 21 MB)", 4.5, 1.6, 3.6);
  stat(s, String(FACTS.links.length), "data tabs linked to the data workbook (local file or SharePoint)", 8.4, 1.6, 3.6,
    AMBER);
  item(s, 1, "Recalculate now / Recalculation on", "Green buttons on ScenarioCompare: a timed full recalculation, or "
    + "automatic calculation for interactive work.", 0.6, 3.5, 6.0);
  item(s, 2, "Update data tables", "Choose the data source on ScenarioCompare; each table is copied by column name; "
    + "the status is on the Cover.", 6.7, 3.5, 6.0);
  card(s, 0.6, 5.0, 12.1, 1.0, CARD, LINE, [
    H("LINKED TABS"),
    { text: FACTS.links.join("  ·  "), options: { fontSize: 15, color: INK } }]);
  s.addNotes("Timings and sizes measured by the user in Excel 365 (2026-10-22): legacy about 10 s per recalculation, "
    + "CPAT-AI about 5 s; CPAT-AI about 10 MB as .xlsb, legacy over 21 MB. Why: short formulas, one formula per block, "
    + "two scenario groups shipped, values stored. v6.6: values stored, OFFSET and COUNTIFS replaced (formulas 568k -> 404k). v7.1: Balances, EnergyCons, "
    + "Prices_dom, HHSurvey, IO_GTAP, HH_Elast (rows of the country); WEO, GDPRatios, UNPop (all rows). Data workbook: "
    + "data/workbooks/CPAT_Data_dummy_python.xlsx (dummy values).");
}

// 7. Results -----------------------------------------------------------------------------------------------------
pres.addSection({ title: "Model and results" });
{
  const s = pres.addSlide({ masterName: "CONTENT", sectionTitle: "Model and results" });
  const below = DATA.co2_ets.every((v, i) => DATA.co2_cap[i] === 0 || v <= DATA.co2_cap[i] + 1e-6);
  header(s, "RESULTS", below ? "Policies cut CO2; Package B keeps covered CO2 under its cap"
    : "Policies cut CO2; the ETS price of Package B is still an estimate");
  lineChart(s, ids.map((k) => ({ name: short[k] || DATA.names[k], labels: years, values: DATA.co2[k] })),
    0.6, 1.5, 6.6, 4.9, "CO2 from fuel combustion incl. power (MtCO2)", SCEN_COLORS);
  lineChart(s, [{ name: "Covered CO2", labels: years, values: DATA.co2_ets },
                { name: "Cap", labels: years, values: DATA.co2_cap }],
    7.5, 1.5, 5.2, 4.9, "Package B: covered CO2 and cap (MtCO2)", [TEAL, AMBER]);
  const c30 = (k) => at("co2", k, 2030);
  caption(s, `2030 vs baseline: $20 ${pct(c30(3) / c30(1) - 1)}, Package A ${pct(c30(4) / c30(1) - 1)}, `
    + `Package B ${pct(c30(5) / c30(1) - 1)}. Package B ETS price 2030: `
    + `${f0(DATA.ets_p[DATA.years.indexOf(2030)])} $/tCO2 (quick estimate).`, 0.6, 6.55, 12.1);
  s.addNotes("Stored scenario results (StoredOutputs). Baseline = no carbon price; Package A = carbon tax to $50 + "
    + "feebates; Package B = ETS on power and industry + carbon tax elsewhere. Builds store a new ETS at its quick "
    + "price estimate; the batch macro's goal seek on the cap is tested separately by the user (issue I30).");
}

// 8. Power: the legacy model ---------------------------------------------------------------------------------------
{
  const s = pres.addSlide({ masterName: "CONTENT", sectionTitle: "Model and results" });
  header(s, "POWER SECTOR · THE MODEL", "The legacy power model, its data from the legacy tabs");
  flow(s, ["H. Demand", "I. Dispatch", "K. Capacity, retirement", "L. Investment", "G. Prices"], 1.6, NAVY);
  lineChart(s, ids.map((k) => ({ name: short[k] || DATA.names[k], labels: years, values: DATA.vre[k] })),
    0.6, 2.55, 6.3, 4.1, "Variable renewable share of generation", SCEN_COLORS, "0%");
  card(s, 7.2, 2.6, 5.5, 3.85, CARD, LINE, [
    H("SAME METHOD AS LEGACY"),
    BL("Power data computed from the legacy Power, CoC and GHGs tabs"),
    BL("Legacy bugs fixed: demand, capacity factors, hydro, WACC, sizing"),
    GAP,
    H("IN THE RESULTS"),
    BL("Electricity demand as memo lines by sector"),
    BL("Power fuel use, revenue and CO2 in the totals", true),
  ]);
  s.addNotes("Demand responds to last year's price; dispatch fills demand from capacity; investment follows a logit on "
    + "levelised cost within scale-up limits, sized for next year's generation estimated from this year's growth (L67, no circular reference). The power data step on Inputs "
    + "reproduces legacy Mitigation section 4 with L52-L56 fixed. A carbon price raises the VRE share.");
}

// 9. Power: engineer features ---------------------------------------------------------------------------------------
{
  const s = pres.addSlide({ masterName: "CONTENT", sectionTitle: "Model and results" });
  header(s, "POWER SECTOR · OPTIONS", "Every legacy power input can change by scenario");
  card(s, 0.6, 1.5, 5.6, 4.95, TEAL_T, "C7E3DE", [
    H("ENGINEER OPTIONS, AS LEGACY"),
    BL("Capacity factors, efficiency, WACC, lifetimes, scale-up and retirement"),
    BL("Gas capacity-factor cap; final deficit to gas"),
    BL("Long-term storage for high VRE shares"),
    BL("Manual capacity and investment"),
    BL("Coal implicit cost (GoalSeekCoal tab)"),
    GAP,
    H("POWER POLICIES"),
    BL("PPAs for coal and gas; renewable subsidies"),
    BL("Electricity excise, revenue rebate, price floor", true),
  ]);
  const p = picture(s, `${PFX}_03_power.png`, 6.5, 1.5, 6.2, 4.7);
  caption(s, "Section 3, baseline: generation, VRE share, capacity, investment, prices", 6.5, p.y + p.h + 0.12, 6.2);
  s.addNotes("Power plan P1-P5 (v5.4, v5.6): every ScenarioDefinition power input is read in the scenario's own column; section "
    + "3 sub-table A0 applies them. Defaults keep Egypt's results. Legacy bugs fixed on the way: L107, L108, L114, L118.");
}

// 10. Road transport ------------------------------------------------------------------------------------------------
{
  const s = pres.addSlide({ masterName: "CONTENT", sectionTitle: "Model and results" });
  header(s, "ROAD TRANSPORT", `Engineer road model as an option, ${TR.nfix} legacy bugs fixed`);
  flow(s, ["Ownership", "Stock", "Cost of ownership", "EV choice", "Fuel economy, distance", "Fuel use"], 1.6, NAVY);
  barChart(s, [
    { name: "Legacy engineer run", labels: TR.years.map(String), values: TR.road_legacy },
    { name: "With the fixes", labels: TR.years.map(String), values: TR.road_fixed }],
    0.6, 2.55, 6.3, 4.1, "Egypt road fuel use, baseline (ktoe)", [AMBER, TEAL]);
  card(s, 7.2, 2.6, 5.5, 3.6, CARD, LINE, [
    H("SAME METHOD AS LEGACY"),
    BL("Reproduces the cached legacy run (to 4e-14)"),
    BL(`Fixes: ownership calibration two-sided, depreciation, buses; EV share of new cars 2035 `
      + `${pct(TR.ev_legacy[1])} -> ${pct(TR.ev_fixed[1])}`),
    GAP,
    H("IN THE WORKBOOK"),
    BL("Switch TrModel per scenario (default: elasticities, as Egypt)"),
    BL("Feebates, distance tax, EV subsidies, purchase taxes, charging subsidies", true),
  ]);
  caption(s, `The road bugs: register section 3.2 (${REG}); method: Transport_Method.md.`, 0.6, 6.75, 12.1);
  s.addNotes("Legacy computes the engineer road model but the Egypt run uses the elasticity approach. The fixes cut the "
    + "engineer baseline by about a third by 2035, mainly through the ownership calibration (L27). Further work on "
    + "the engineer road model was dropped by the user (2026-10-20).");
}

// 11. GHGs, methane, NDC, GDP ---------------------------------------------------------------------------------------
{
  const s = pres.addSlide({ masterName: "CONTENT", sectionTitle: "Model and results" });
  header(s, "GHGS, NDC AND GDP", "All greenhouse gases, compared with the NDC target");
  lineChart(s, ids.map((k) => ({ name: short[k] || DATA.names[k], labels: years, values: DATA.ghg[k] })),
    0.6, 1.5, 6.3, 4.95, "GHG emissions excl. LULUCF (Mt CO2e)", SCEN_COLORS);
  const g30 = (k) => at("ghg", k, 2030);
  stat(s, pct(at("ndc_gap", 4, 2030)), "of the NDC reduction achieved by Package A in 2030 (BAU target, -27%)",
    7.2, 1.55, 2.6, TEAL);
  stat(s, pct(g30(4) / g30(1) - 1), "GHGs in 2030, Package A against the baseline", 10.1, 1.55, 2.6, NAVY);
  card(s, 7.2, 3.35, 5.5, 3.1, CARD, LINE, [
    H("IN THE WORKBOOK"),
    BL("Methane by source; methane fee in revenue and in the fiscal space"),
    BL("Producer methane follows world demand, as legacy"),
    BL("NDC comparison: five NDC types, conditional or not"),
    BL("GDP effect of the revenue use, by use and by year", true),
  ]);
  s.addNotes("Section 14 projects every gas from the GHGs inventory; 14c compares the selected NDC with the scenario "
    + "(comparison only, no NDC goal seek). Section 16 turns revenue into fiscal space and a GDP effect with the "
    + "legacy multipliers; the GDP effect enters growth once (legacy bug L24 fixed). The methane fee counts in the fiscal "
    + "space on the scenario's own activity, as legacy.");
}

// 12. Distribution -------------------------------------------------------------------------------------------------
{
  const s = pres.addSlide({ masterName: "CONTENT", sectionTitle: "Model and results" });
  const D = DATA.distn;
  header(s, "DISTRIBUTION", "Who pays, by decile, and how recycling changes it");
  const dec = ["1", "2", "3", "4", "5", "6", "7", "8", "9", "10"];
  barChart(s, [{ name: "Price effects", labels: dec, values: D.tef.map((v) => v / 100) },
               { name: "Net effect after recycling", labels: dec, values: D.net.map((v) => v / 100) }],
    0.6, 1.5, 6.3, 4.95, `Effect by decile, ${D.year}, carbon price $20 (% of consumption)`, [AMBER, TEAL], "0.0%");
  card(s, 7.2, 1.5, 5.5, 4.95, TEAL_T, "C7E3DE", [
    H("THE LEGACY CHAIN, IN ONE TAB"),
    BL("Direct and indirect price effects (GTAP input-output)"),
    BL("Revenue recycling: tax cuts, investment, spending, transfers"),
    BL("ASPIRE and poverty-line transfers; compensation"),
    BL("Gini, Lorenz curves, urban and rural, top-20 sectors"),
    GAP,
    H("CHECKED"),
    BL(`Legacy distribution bugs fixed (D10-D31)`),
    BL(`Equal to a Python reference (${FACTS.distn_ref ? FACTS.distn_ref[0] : ""} values)`, true),
  ]);
  caption(s, "Deciles across, one analysis year (ScenarioDefinition YearDistn); scenario groups as on Mitigation.",
    0.6, 6.6, 12.1);
  s.addNotes(`Distribution tab, scenario group 2. Gini change with recycling: ${D.gini_rec.toFixed(2)}%. Eleven charts `
    + "on the tab. Method: Distribution_Method.md.");
}

// 13. Results sections ---------------------------------------------------------------------------------------------
{
  const s = pres.addSlide({ masterName: "CONTENT", sectionTitle: "Model and results" });
  header(s, "RESULTS SECTIONS", "Legacy's post-processing, rebuilt inside each scenario");
  const b = (t, last = false) => ({ text: t, options: { bullet: true, fontSize: 16, color: INK, breakLine: !last,
    paraSpaceAfter: 6 } });
  card(s, 0.6, 1.5, 6.6, 4.95, CARD, LINE, [
    H("ROWS IN EVERY SCENARIO BLOCK"),
    b("2: average prices and price indices"),
    b("11b, 13b, 14b: changes by fuel and sector; Kaya"),
    b("12d, 12e: revenue by fuel and by policy, % of GDP"),
    b("14c: NDC comparison"),
    b("16, 16b: GDP effects; net energy imports"),
    b("17: implicit carbon price, effective rate, coverage"),
    b("18: social cost of carbon, damages avoided, welfare", true),
  ]);
  const W = 2031;
  card(s, 7.5, 1.5, 5.2, 4.95, TEAL_T, LINE, [
    H("EGYPT, CARBON PRICE $20 (SCENARIO 3)"),
    b(`Coverage of energy CO2, 2030: ${pct(at("cov", 3, 2030), 1)}`),
    b(`Implicit carbon price of fossil fuels, 2022: ${f0(at("cpi", 3, 2022))} $/tCO2`),
    b(`Net energy imports, 2030: ${f1(at("xnim", 3, 2030))} bn USD`),
    b(`Climate damages avoided, ${W}: ${f1(at("wcli", 3, W))} bn USD (SCC ${f0(at("scc", 3, W))} $/t)`),
    b(`Efficiency cost, ${W}: ${f1(at("eff", 3, W))} bn USD (negative = gain)`),
    b(`National welfare, ${W}: ${f1(at("wel_usd", 3, W))} bn USD`, true),
  ]);
  caption(s, "Method: ResultsSections_Method.md. Every new row is recomputed in Python in every scenario.", 0.6, 6.6, 12.1);
  s.addNotes("Legacy's results area moved into the scenario sections, as memos or lettered sub-blocks, plus sections "
    + "17 and 18. Values from StoredOutputs (scenario 3 = the $20 carbon price of scenario 2). A negative implicit "
    + "carbon price means fossil fuels are subsidised on balance.");
}

// 14. Quality ----------------------------------------------------------------------------------------------------
{
  const s = pres.addSlide({ masterName: "CONTENT", sectionTitle: "Model and results" });
  header(s, "QUALITY", "Every number is checked independently");
  stat(s, FACTS.errors, "error values when LibreOffice recalculates the shipped file", 0.6, 1.7, 2.8, TEAL);
  stat(s, FACTS.formulas, "formulas, none longer than 100 characters", 3.7, 1.7, 2.8);
  stat(s, FACTS.codes, `output codes; ${FACTS.changed} of ${FACTS.shared} changed against the last release`, 6.8, 1.7, 2.8);
  stat(s, String(BUGS), "legacy bugs found; none replicated in the prototype", 9.9, 1.7, 2.8, AMBER);
  item(s, 1, "Independent recomputation", "Python recomputes prices, fuel use, power, revenue, emissions and "
    + "distribution from the source data for the test scenarios.", 0.6, 3.9, 6.0);
  item(s, 2, "Copy-paste and LAMBDAs tested", "Pasted groups equal the stored results; the LAMBDA group equals "
    + "the plain formulas of the last release.", 6.7, 3.9, 6.0);
  item(s, 3, "Differences listed", "Tab 'Version Log, About, and Diff' lists every difference with legacy CPAT and why.",
    0.6, 5.3, 6.0);
  item(s, 4, "Documented", "The model in equations, method notes and every formula; one register of bugs and issues.", 6.7, 5.3, 6.0);
  s.addNotes(`Quick check check_quick_report_v${VER}.md: ${FACTS.quick}.`
    + (FACTS.full_overall ? ` Full check check_report_v${VER}.md: ${FACTS.full_overall}.` : ""));
}

// 15. Getting started --------------------------------------------------------------------------------------------
pres.addSection({ title: "Next steps" });
{
  const s = pres.addSlide({ masterName: "CONTENT", sectionTitle: "Next steps" });
  header(s, "GETTING STARTED", "Open, run the check, then explore");
  item(s, 1, "Open the .xlsm and enable macros", "Debug > Compile VBAProject once, then First-run test: PASS.",
    0.6, 1.7, 7.0);
  item(s, 2, "Change a scenario", "Edit its ScenarioDefinition column, then click Recalculate now.",
    0.6, 2.9, 7.0);
  item(s, 3, "Run many scenarios", "Run? = Yes on the definitions, click Run stored scenarios; read the dashboard.",
    0.6, 4.1, 7.0);
  item(s, 4, "Read more", "Cover tab, QuickStart and equations; the bugs and issues register in Word.", 0.6, 5.3, 7.0);
  s.addShape(pres.shapes.RECTANGLE, { x: 8.1, y: 1.5, w: 4.6, h: 5.0, fill: { color: NAVY }, line: { color: NAVY },
    objectName: nm("card") });
  s.addText([
    { text: "WHAT REMAINS", options: { bold: true, fontSize: 11, color: GOLD, charSpacing: 2, breakLine: true } },
    { text: "Review in Excel 365: timings, macros, links (I1)", options: { bullet: true, breakLine: true } },
    { text: "Send bugs and fix plans to the CPAT team (U4)", options: { bullet: true, breakLine: true } },
    { text: "Align codes: Excel, Python, master list", options: { bullet: true, breakLine: true } },
    { text: "Link the other data tabs (GHGs, EF_GHG ...)", options: { bullet: true, breakLine: true } },
    { text: "DATA REQUESTS", options: { bold: true, fontSize: 11, color: GOLD, charSpacing: 2, breakLine: true } },
    { text: "GAINS emission-factor paths (I64)", options: { bullet: true, breakLine: true } },
    { text: "Blank VAT cells in the price data (I65)", options: { bullet: true, breakLine: true } },
    { text: "Proprietary tables, other countries (I13)", options: { bullet: true, breakLine: true } },
    { text: "Historical GHGs 2018-2020 (I68)", options: { bullet: true } },
  ], { x: 8.35, y: 1.75, w: 4.1, h: 4.6, fontSize: 14, color: "FFFFFF", valign: "top", margin: 0, paraSpaceAfter: 8,
    isTextBox: true, objectName: nm("next") });
  s.addNotes(`Files: CPAT-AI-Mitigation-Prototype-v${VER}.xlsm (repository root), QuickStart.md, `
    + `documentation/${REG}. Also open: reconcile with legacy file 459 (U2); ETS goal seek user test (I30). `
    + "Open items from issues_register.py; I52 and I53 wait for features not planned.");
}

(async () => {
  await pres.writeFile({ fileName: OUT });
  await applyTheme(OUT, THEME);
  fs.copyFileSync(OUT, LATEST);
  console.log("wrote", OUT, "and", LATEST);
})();
