const fs=require('fs');
const {Document,Packer,Paragraph,TextRun,Table,TableRow,TableCell,WidthType,ShadingType,HeadingLevel,PageOrientation,AlignmentType,LevelFormat,BorderStyle,Footer,PageNumber}=require('docx');
const A=JSON.parse(fs.readFileSync('partA.json')), B=JSON.parse(fs.readFileSync('partB.json'));
const FONT='Calibri', MONO='Consolas';
const P=(t,o={})=>new Paragraph({spacing:{after:80},...o,children:(Array.isArray(t)?t:[new TextRun({text:t,font:FONT,size:20})])});
const R=(t,o={})=>new TextRun({text:t,font:FONT,size:20,...o});
const M=(t)=>new TextRun({text:t,font:MONO,size:16});
const bullet=(runs)=>new Paragraph({numbering:{reference:'b',level:0},spacing:{after:60},children:runs});
const W=[1000,4900,4900,2100,1938];
const border={style:BorderStyle.SINGLE,size:4,color:'BFBFBF'};
const cell=(children,w,head=false)=>new TableCell({width:{size:w,type:WidthType.DXA},margins:{top:60,bottom:60,left:80,right:80},
  borders:{top:border,bottom:border,left:border,right:border},
  shading:head?{type:ShadingType.CLEAR,color:'auto',fill:'1F3864'}:undefined,children});
const hc=(t,w)=>cell([new Paragraph({children:[R(t,{bold:true,color:'FFFFFF',size:18})]})],w,true);
const mc=(t,w)=>cell([new Paragraph({children:String(t).split('\n').map((x,i)=>i?new TextRun({text:x,font:MONO,size:16,break:1}):M(x))})],w);   // multi-line formulas (Alt+Enter)
const tc=(t,w)=>cell([new Paragraph({children:[R(t,{size:17})]})],w);
function fixTable(fx){
  return new Table({width:{size:W.reduce((a,b)=>a+b),type:WidthType.DXA},columnWidths:W,rows:[
    new TableRow({tableHeader:true,children:[hc('Cell',W[0]),hc('Now (legacy)',W[1]),hc('Change to',W[2]),hc('Fill',W[3]),hc('Policy block',W[4])]}),
    ...fx.map(f=>new TableRow({children:[mc(f.cell,W[0]),mc(f.now,W[1]),mc(f.new,W[2]),tc(f.fill,W[3]),tc(f.policy,W[4])]}))]});
}
function bugBlock(b){
  const out=[new Paragraph({heading:HeadingLevel.HEADING_2,spacing:{before:240,after:80},children:[new TextRun({text:`${b.id} (${b.pri}): ${b.title}`,font:FONT})]})];
  out.push(P([R('Where: ',{bold:true}),R(b.where)]));
  out.push(P([R('What is wrong: ',{bold:true}),R(b.why)]));
  if(b.fixes.length) out.push(fixTable(b.fixes));
  else out.push(P([R('Fix: ',{bold:true}),R(b.status==='struct'?'structural (no existing cell to edit), see steps below.':'no cell to change.',{bold:true,color:'C00000'})]));
  if(b.fixes.length && b.status && b.status!=='fix') out.push(P([R('Status: ',{bold:true}),R(b.status+' (the cells above plus the steps in the note).',{bold:true,color:'C00000'})]));
  if(b.note) out.push(P([R('Note: ',{bold:true}),R(b.note)],{spacing:{before:80,after:80}}));
  if(b.ref && b.ref!=='n/a') out.push(P([R('Legacy reference: ',{bold:true}),R(b.ref)],{spacing:{before:80,after:80}}));
  out.push(P([R('Expected effect: ',{bold:true}),R(b.effect)]));
  return out;
}
function summary(list){
  const w=[900,1200,6200,6538];
  return new Table({width:{size:14838,type:WidthType.DXA},columnWidths:w,rows:[
    new TableRow({tableHeader:true,children:[hc('ID',w[0]),hc('Priority',w[1]),hc('Bug',w[2]),hc('Cells to change (baseline)',w[3])]}),
    ...list.map(b=>new TableRow({children:[tc(b.id,w[0]),tc(b.pri,w[1]),tc(b.title,w[2]),tc(b.fixes.length?b.fixes.map(f=>f.fill.split(' ')[0].replace(/,$/,'')).join(', ')+(b.status&&b.status!=='fix'?' + '+b.status:''):(b.status==='struct'?'Insert rows (see L22)':'None: not reproduced'),w[3])]}))]});
}
const H1=(t)=>new Paragraph({heading:HeadingLevel.HEADING_1,spacing:{before:360,after:120},children:[new TextRun({text:t,font:FONT})]});
const intro=[
 new Paragraph({heading:HeadingLevel.TITLE,children:[new TextRun({text:'Legacy CPAT bug fixes: cell-by-cell plan',font:FONT})]}),
 P('Workbook: CPAT 1.0pre_456_NoPropData.xlsb, sheet Mitigation unless stated. Prepared 2026-10-15 from the formulas stored in the file (defined names recovered from the .xlsb) and its cached Egypt values. Bug IDs are those of the repo register (excel_ai/working_version/LegacyBugFixes_v3_8.md).'),
 H1('How to apply every fix'),
 bullet([R('Work in a copy of the workbook and fix one bug at a time (excel_ai/bugs_and_legacy/fixes/procedure/BugFixProcedure.md; macro template FixL1_ServicesElectricity.bas).')]),
 bullet([R('Year columns: K = 2021, L = 2022, M = 2023 … AE = 2041. Type the new formula in the cell named, then drag right as stated under "Fill".')]),
 bullet([R('Policy block: copy the fixed baseline row and Paste Special → Formulas onto the policy row given. Up to row ~6070 the policy block is the baseline + 6,331 rows; from the other-energy-use block (row 6066) on it is + 6,317. A paste works in both cases except L43 (its formulas point back to driver rows at + 6,331), where the policy edit is spelled out.')]),
 bullet([R('Recalculate fully, check legacy\'s own check cells (e.g. B6602, B7640 must still read "OK"), and compare with the expected effect.')]),
 bullet([R('Expected effects: Part A from the repo\'s Python copy of the legacy power model (power_model_ref_v3_8.py, which matches the cached legacy rows to 1e-13, price feedback to other sectors excluded); Part B from cached values and the register. Nothing here was recalculated in Excel.')]),
 bullet([R('Out of scope: the engineer road-transport bugs L25-L41 (separate list) and L17 (an prototype bug, not legacy).')]),
];
const all=[...A,...B];
const doc=new Document({
 styles:{default:{document:{run:{font:FONT,size:20}}},paragraphStyles:[
  {id:'Heading1',name:'Heading 1',basedOn:'Normal',next:'Normal',quickFormat:true,run:{size:30,bold:true,color:'1F3864',font:FONT},paragraph:{outlineLevel:0}},
  {id:'Heading2',name:'Heading 2',basedOn:'Normal',next:'Normal',quickFormat:true,run:{size:24,bold:true,color:'2E5597',font:FONT},paragraph:{outlineLevel:1}}]},
 numbering:{config:[{reference:'b',levels:[{level:0,format:LevelFormat.BULLET,text:'•',alignment:AlignmentType.LEFT,style:{paragraph:{indent:{left:360,hanging:260}}}}]}]},
 sections:[{properties:{page:{size:{width:11906,height:16838,orientation:PageOrientation.LANDSCAPE},margin:{top:1000,bottom:1000,left:1000,right:1000}}},
  footers:{default:new Footer({children:[new Paragraph({alignment:AlignmentType.RIGHT,children:[R('Page ',{size:16}),new TextRun({children:[PageNumber.CURRENT],size:16,font:FONT})]})]})},
  children:[...intro,
   H1('Summary'),P(`${all.length} entries: 12 engineer power model bugs (Part A), 18 other mitigation bugs from the register (Part B, of which L15 and L18 do not reproduce in this file and L22 needs new rows), and 2 new defects found while checking (N1, N2).`),summary(all),
   H1('Part A. Engineer power model (sections D6, H-L)'),P('Suggested order: L1, L3, L2 (demand), then L5, L6, then the Low items. All 10 result-changing fixes together: 2040 generation +12.6% (baseline) and +9.2% (carbon-tax run).'),
   ...A.flatMap(bugBlock),
   H1('Part B. Other mitigation bugs (outside the power and road engineer models)'),P('Suggested order: L20, L24 (macro drivers, everything downstream), L13, L42, L43 (fuel use), L19, L21 (GHG), then the Low items. L14 changes nothing for Egypt but is a real formula error.'),
   ...B.flatMap(bugBlock)]}]});
Packer.toBuffer(doc).then(b=>fs.writeFileSync(process.argv[2],b));
