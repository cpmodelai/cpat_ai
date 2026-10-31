// Build coded/cpat_documentation/Coded-CPAT_Overview_v<version>.pptx: the overview deck of Coded CPAT, the Python
// model of CPAT. Same style as the Excel-AI core deck (excel_ai/mitigation/docs/presentation/build_deck.js): navy / teal /
// amber, Cambria headings, Calibri body. The numbers come from facts.json (make_facts.py), so the deck stays current.
//
//   python make_facts.py && NODE_PATH=<node_modules with pptxgenjs> PPTX_SKILL=<pptx skill dir> node build_deck.js
const fs = require("fs");
const path = require("path");
const pptxgen = require("pptxgenjs");
const { applyTheme } = require(process.env.PPTX_SKILL + "/scripts/apply_theme.js");

const HERE = __dirname;
const F = JSON.parse(fs.readFileSync(path.join(HERE, "facts.json"), "utf8"));
const OUT = path.join(HERE, "..", `Coded-CPAT_Overview_v${F.version}.pptx`);
const LATEST = path.join(HERE, "..", "..", "..", "docs", "presentations", "03_Coded-CPAT_Overview_latest.pptx");   // website permalink
const fmt = (x) => x.toLocaleString("en-US");

const THEME = {
  name: "Coded CPAT",
  headFontFace: "Cambria",
  bodyFontFace: "Calibri",
  colors: {
    dk1: "1F1F2E", lt1: "FFFFFF", dk2: "1E2761", lt2: "F4F6FB",
    accent1: "1E2761", accent2: "0F7B6C", accent3: "E08A1E", accent4: "D4A24C",
    accent5: "5C667A", accent6: "D5DAE3", hlink: "0F7B6C", folHlink: "5C667A",
  },
};
const NAVY = "1E2761", TEAL = "0F7B6C", AMBER = "E08A1E", INK = "1F1F2E", GREY = "5C667A";
const CARD = "F4F6FB", LINE = "D5DAE3", TEAL_T = "EAF4F2", AMBER_T = "FDF3E6", ICE = "CADCFC";

const pres = new pptxgen();
pres.layout = "LAYOUT_WIDE";
pres.title = `Coded CPAT v${F.version}: overview`;
pres.theme = { headFontFace: THEME.headFontFace, bodyFontFace: THEME.bodyFontFace };

pres.defineSlideMaster({
  title: "TITLE_DARK",
  background: { color: NAVY },
  objects: [
    { placeholder: { options: { name: "title", type: "title", x: 0.7, y: 1.7, w: 8.5, h: 1.3, fontFace: "Cambria",
      fontSize: 48, bold: true, color: "FFFFFF", valign: "top", align: "left", margin: 0 }, text: "" } },
    { placeholder: { options: { name: "body", type: "body", x: 0.7, y: 3.15, w: 8.5, h: 1.6, fontFace: "Calibri",
      fontSize: 20, color: ICE, valign: "top", align: "left", margin: 0 }, text: "" } },
  ],
});
pres.defineSlideMaster({
  title: "CONTENT",
  background: { color: "FFFFFF" },
  objects: [
    { placeholder: { options: { name: "label", type: "body", x: 0.6, y: 0.32, w: 12.1, h: 0.3, fontFace: "Calibri",
      fontSize: 11, bold: true, color: TEAL, charSpacing: 2, margin: 0 }, text: "" } },
    { placeholder: { options: { name: "title", type: "title", x: 0.6, y: 0.62, w: 12.1, h: 0.75, fontFace: "Cambria",
      fontSize: 30, bold: true, color: NAVY, valign: "top", align: "left", margin: 0 }, text: "" } },
    { text: { text: `Coded CPAT v${F.version}  ·  replicates Excel-AI ${F.excel_ai} and Distribution ${F.distribution}`,
      options: { x: 0.6, y: 7.05, w: 9.5, h: 0.25, fontSize: 9, color: GREY, margin: 0 } } },
  ],
  slideNumber: { x: 12.3, y: 7.05, w: 0.5, h: 0.25, fontSize: 9, color: GREY, align: "right" },
});

let n = 0;
const nm = (s) => `${s}-${++n}`;
const content = (section, label, title) => {
  const s = pres.addSlide({ masterName: "CONTENT", sectionTitle: section });
  s.addText(label, { placeholder: "label" });
  s.addText(title, { placeholder: "title" });
  return s;
};
function badge(slide, txt, x, y, color, size = 0.5) {
  slide.addShape(pres.shapes.OVAL, { x, y, w: size, h: size, fill: { color }, line: { color }, objectName: nm("badge") });
  slide.addText(txt, { x, y, w: size, h: size, align: "center", valign: "middle", fontSize: 16, bold: true,
    color: "FFFFFF", margin: 0, isTextBox: true, objectName: nm("badgeText") });
}
function card(slide, x, y, w, h, fill, lineC, runs) {
  slide.addShape(pres.shapes.RECTANGLE, { x, y, w, h, fill: { color: fill }, line: { color: lineC }, objectName: nm("card") });
  slide.addText(runs, { x: x + 0.2, y: y + 0.15, w: w - 0.4, h: h - 0.3, valign: "top", margin: 0, isTextBox: true,
    objectName: nm("cardText") });
}
const head = (t, color = INK) => ({ text: t, options: { bold: true, fontSize: 16, color, breakLine: true } });
const body = (t) => ({ text: t, options: { fontSize: 16, color: GREY } });
function stat(slide, big, small, x, y, w, color = NAVY, smallColor = GREY) {
  slide.addText([
    { text: big, options: { fontSize: 44, bold: true, color, fontFace: "Cambria", breakLine: true } },
    { text: small, options: { fontSize: 14, color: smallColor } },
  ], { x, y, w, h: 1.6, valign: "top", margin: 0, isTextBox: true, objectName: nm("stat") });
}
function flow(slide, steps, y, h = 1.25) {
  const k = steps.length, gap = 0.35, w = (12.1 - gap * (k - 1)) / k;
  steps.forEach(([t, sub, color], i) => {
    const x = 0.6 + i * (w + gap);
    slide.addShape(pres.shapes.ROUNDED_RECTANGLE, { x, y, w, h, rectRadius: 0.08, fill: { color }, line: { color },
      objectName: nm("step") });
    slide.addText([{ text: t, options: { bold: true, fontSize: 15, color: "FFFFFF", breakLine: true } },
      { text: sub, options: { fontSize: 12, color: "FFFFFF" } }],
      { x: x + 0.1, y: y + 0.08, w: w - 0.2, h: h - 0.16, align: "center", valign: "middle", margin: 0, isTextBox: true,
        objectName: nm("stepText") });
    if (i < k - 1) {
      slide.addShape(pres.shapes.RIGHT_TRIANGLE, { x: x + w + 0.08, y: y + h / 2 - 0.13, w: 0.2, h: 0.26, rotate: 90,
        fill: { color: LINE }, line: { color: LINE }, objectName: nm("arrow") });
    }
  });
}

// 1. Title
pres.addSection({ title: "Coded CPAT" });
let s = pres.addSlide({ masterName: "TITLE_DARK", sectionTitle: "Coded CPAT" });
s.addText("Coded CPAT", { placeholder: "title" });
s.addText(`The Python model of CPAT: Excel-AI number for number, readable first\nVersion ${F.version}`,
  { placeholder: "body" });
stat(s, fmt(F.codes_per_scenario), "result codes per scenario, equal to Excel-AI", 9.6, 1.7, 3.2, "FFFFFF", "CADCFC");
stat(s, "0", "known differences", 9.6, 3.5, 3.2, AMBER, "CADCFC");
s.addNotes("Coded CPAT is the Python version of CPAT. It reproduces the Excel-AI prototypes exactly and is written to be read.");

// 2. The message
pres.addSection({ title: "Summary" });
s = content("Summary", "IN ONE SLIDE", "One model, two forms, the same numbers");
[[TEAL, "Exact", `Every result code of Egypt's scenarios equals Excel-AI ${F.excel_ai} within 1e-9; the distribution module equals Distribution ${F.distribution}.`],
 [NAVY, "Fast", "One country and two scenarios run in under a second; a rerun computes only the scenarios that changed."],
 [AMBER, "Readable", `One small function per equation (${F.equations} equations), named with the codes of the Excel models; a documentation book on the website.`],
 [TEAL, "Honest", "Excel-AI's bugs are not copied: eight found by the replication were fixed in the prototype and in Python."]]
  .forEach(([c, h, b], i) => {
    const x = 0.6 + (i % 2) * 6.15, y = 1.9 + Math.floor(i / 2) * 2.4;
    card(s, x, y, 5.95, 2.0, i % 2 ? CARD : TEAL_T, LINE, [head(h, c), body(b)]);
  });
s.addNotes("Four messages: it matches Excel-AI exactly, it is fast, it is readable, and it does not copy bugs.");

// 3. What it is
pres.addSection({ title: "What it is" });
s = content("What it is", "WHAT IT IS", "Excel-AI is the specification; Coded CPAT is its Python twin");
flow(s, [["Excel-AI", "the prototypes: mitigation and distribution", NAVY],
  ["Coded CPAT", "the same rows, codes and equations in Python", TEAL],
  ["Run it", "command line, Python, Shiny app", AMBER]], 1.9, 1.4);
card(s, 0.6, 3.75, 5.95, 2.2, CARD, LINE, [head("What it computes"), body(
  "Energy prices, power, fuel use, emissions, revenues, GDP effects, welfare and efficient prices for 2022-2041, and the effect on households by decile, for any scenario set of Excel-AI's inputs.")]);
card(s, 6.75, 3.75, 5.95, 2.2, CARD, LINE, [head("How it stays equal"), body(
  "Every Excel-AI row has an output code. The tests compare Python with the workbooks code by code and year by year; a block is done only when all its codes match.")]);

// 4. Status in numbers
pres.addSection({ title: "Status" });
s = content("Status", "STATUS", "Every number checked against Excel-AI");
stat(s, fmt(F.codes_per_scenario), "mitigation result codes per scenario, scenarios 1-2", 0.6, 1.8, 3.9);
stat(s, fmt(F.distribution_codes), "distribution codes: basket and ten deciles", 4.7, 1.8, 3.9, TEAL);
stat(s, fmt(F.stored_codes), "key codes of the stored scenarios 1 and 3-6", 8.8, 1.8, 3.9, AMBER);
stat(s, String(F.tests_passed), `tests passing, ${F.tests_failed} failing`, 0.6, 4.3, 3.9, TEAL);
stat(s, String(F.equations), "equations, each with its function", 4.7, 4.3, 3.9);
stat(s, "1e-9", "tolerance: relative above 1, absolute below", 8.8, 4.3, 3.9, AMBER);

// 5. How a run works
pres.addSection({ title: "How it works" });
s = content("How it works", "HOW A RUN WORKS", "Baseline first, then each scenario, in three stages");
flow(s, [["Scenario set", "inputs by name, baseline first", NAVY], ["Prepare", "all years: prices, policies, costs", TEAL],
  ["Year loop", "2022-2041: power, fuel use, emissions, GDP", TEAL], ["Finish", "all-year rows (NDC)", TEAL],
  ["Distribution", "households by decile", AMBER], ["Results", "by output code", NAVY]], 1.9, 1.5);
card(s, 0.6, 3.85, 12.1, 1.9, CARD, LINE, [head("Why it is fast"), body(
  "Block rows stay numpy arrays and become labelled arrays only when read from outside. The baseline run, the data steps and every scenario already run are cached, so a rerun computes only what changed: 5.3 s before the speed work, 0.8 s with the baseline cached, under 0.1 s for an unchanged rerun.")]);

// 6. Speed chart
s = content("How it works", "SPEED", "From 5 seconds to under one");
s.addChart(pres.charts.BAR, [{ name: "Seconds", labels: ["Before (two scenarios)", "Baseline cached", "Unchanged rerun"],
  values: [5.3, 0.8, 0.05] }], { dataLabelFormatCode: "0.00", valAxisLabelFormatCode: "0", x: 0.6, y: 1.6, w: 7.4, h: 5.1, barDir: "bar", chartColors: [TEAL],
  showValue: true, dataLabelPosition: "outEnd", dataLabelFontSize: 14, dataLabelColor: INK, dataLabelFontFace: "+mn-lt",
  catAxisLabelFontFace: "+mn-lt", valAxisLabelFontFace: "+mn-lt", catAxisLabelColor: GREY, valAxisLabelColor: GREY,
  catAxisLabelFontSize: 14, valAxisLabelFontSize: 12, valGridLine: { color: LINE, size: 0.5 },
  catGridLine: { style: "none" }, showLegend: false, showTitle: true, title: "Seconds, Egypt", titleFontSize: 14,
  titleColor: GREY, titleFontFace: "+mn-lt" });
card(s, 8.3, 1.6, 4.4, 2.75, TEAL_T, LINE, [head("The target was one second", TEAL), body(
  "Plan task 5.4: one country and two scenarios in under a second (D11). Met with the baseline and the data cached.")]);
card(s, 8.3, 4.55, 4.4, 2.15, CARD, LINE, [head("Checked by a test"), body(
  "test_speed.py: a cached run equals a fresh one exactly and takes under 2 s (a loose bound for slower machines).")]);

// 7. The database
pres.addSection({ title: "Data" });
s = content("Data", "THE DATABASE", "Tidy CSV, one table per file, the same numbers as Excel-AI");
stat(s, String(F.tables), "tables in data/Public01/tidy/ (the dummy database)", 0.6, 1.8, 3.6);
stat(s, String(F.proprietary), "tidy tables from the four proprietary tables: only Egypt's public rows committed", 0.6, 4.2, 3.6, AMBER);
card(s, 4.5, 1.8, 8.2, 2.2, CARD, LINE, [head("Format"), body(
  "Long tables: keys first (country ISO3, year, codes), then the value. A converter turns them into Excel-AI's legacy layout and back, exactly, so both models read the same numbers.")]);
card(s, 4.5, 4.2, 8.2, 2.4, AMBER_T, LINE, [head("Where", AMBER), body(
  "Dummy: data/Public01/tidy/ in the repository (Egypt has its base tables). Full: every country, in a private repository; set FULL_DATA_PATH and run with database 'full'. A country without its base tables stops with a clear message.")]);

// 8. Testing
pres.addSection({ title: "Testing" });
s = content("Testing", "TESTING", "Five comparisons, all passing");
s.addChart(pres.charts.BAR, [{ name: "Codes compared", labels: ["Mitigation, scenarios 1-2", "Distribution, groups 1-2",
  "Stored scenarios 1, 3-6", "Independent recomputation"], values: [2 * F.codes_per_scenario, F.distribution_codes,
  F.stored_codes, 35] }], { x: 0.6, y: 1.6, w: 7.4, h: 5.1, barDir: "bar", chartColors: [NAVY], showValue: true,
  dataLabelPosition: "outEnd", dataLabelFontSize: 13, dataLabelColor: INK, dataLabelFontFace: "+mn-lt",
  catAxisLabelFontFace: "+mn-lt", valAxisLabelFontFace: "+mn-lt", catAxisLabelColor: GREY, valAxisLabelColor: GREY,
  catAxisLabelFontSize: 13, valAxisLabelFontSize: 12, valGridLine: { color: LINE, size: 0.5 },
  catGridLine: { style: "none" }, showLegend: false, showTitle: true, title: "Codes compared, all within 1e-9",
  titleFontSize: 14, titleColor: GREY, titleFontFace: "+mn-lt" });
card(s, 8.3, 1.6, 4.4, 5.1, CARD, LINE, [head("How to run them"), body(
  "pytest from coded/ (about a minute) before every commit. The documentation book shows the last test status, regenerated from the tests. Legacy CPAT: the Egypt baseline is compared with legacy's cached run; the gaps are Excel-AI's documented fixes and newer data.")]);

// 9. Bugs found
s = content("Testing", "BUGS FOUND BY THE REPLICATION", "Writing it twice found eight bugs in the prototype");
const rows = [["Bug", "What", "Status"],
  ["M15", "VAT on efficient prices at the 2022 rate in every year", "Fixed (0.9.2)"],
  ["M16", "Freight BEV feebate at the ICEV truck's distance", "Fixed (0.9.2)"],
  ["M17", "Plug-in hybrid cost mixed two price bases", "Fixed (0.9.2)"],
  ["M18", "Bus electricity scaled by every fuel", "Withdrawn: as legacy"],
  ["M19", "Nominal GDP divided by a billion twice", "Fixed (0.9.2)"],
  ["M20", "LNG and European gas prices swapped", "Fixed (0.9.2)"],
  ["M21", "Methane fee: division by zero", "Fixed (0.9.2)"],
  ["M22", "Distribution: a % added to amounts in LCU", "Fixed (Distribution 0.1.4)"]];
s.addTable(rows.map((r, i) => r.map((c) => ({ text: c, options: { bold: i === 0, color: i === 0 ? "FFFFFF" : INK,
  fill: { color: i === 0 ? NAVY : (i % 2 ? "FFFFFF" : CARD) }, fontSize: 13 } }))),
  { x: 0.6, y: 1.6, w: 8.2, colW: [0.9, 5.0, 2.3], rowH: 0.5, border: { type: "solid", color: LINE, pt: 0.5 },
    objectName: nm("bugs") });
card(s, 9.1, 1.6, 3.6, 4.5, TEAL_T, LINE, [head("The rule", TEAL), body(
  "Bugs are never copied into Python; issues (potential improvements) are logged and copied for now. Each bug is registered, fixed in the prototype, and Python follows.")]);

// 10. Using it
pres.addSection({ title: "Using it" });
s = content("Using it", "FOUR WAYS IN", "Command line, Python, app, documentation");
[["1", "Command line", "python run_model.py: a scenario-set file in, results by country out (CSV, workbook)", NAVY],
 ["2", "Python", "cpat_model.run(scenarios): Results by output code; the distribution by decile", TEAL],
 ["3", "Shiny app", "shiny run app.py: build carbon-tax scenarios, run, tables and six graphs", AMBER],
 ["4", "Website", "the Coded CPAT tab: what you need to know first, every reference in appendices", NAVY]]
  .forEach(([k, h, b, c], i) => {
    const x = 0.6 + (i % 2) * 6.15, y = 1.8 + Math.floor(i / 2) * 2.45;
    card(s, x, y, 5.95, 2.15, CARD, LINE, [{ text: "", options: { breakLine: true } }]);
    badge(s, k, x + 0.25, y + 0.3, c);
    s.addText([head(h), body(b)], { x: x + 0.95, y: y + 0.25, w: 4.8, h: 1.7, valign: "top", margin: 0,
      isTextBox: true, objectName: nm("way") });
  });

// 11. Next steps
pres.addSection({ title: "Next" });
s = pres.addSlide({ masterName: "TITLE_DARK", sectionTitle: "Next" });
s.addText("Next steps", { placeholder: "title" });
s.addText([
  { text: "Every country on the full database (private)", options: { bullet: true, breakLine: true } },
  { text: "Legacy CPAT 465 and every country, through the register", options: { bullet: true, breakLine: true } },
  { text: "The other demand forms (ModelForm) in Excel-AI and Python together", options: { bullet: true, breakLine: true } },
  { text: "The live air-pollution and transport co-benefits modules", options: { bullet: true } },
], { placeholder: "body" });

pres.writeFile({ fileName: OUT }).then(async () => {
  await applyTheme(OUT, THEME);
  fs.copyFileSync(OUT, LATEST);
  console.log("wrote " + OUT + " and " + LATEST);
});
