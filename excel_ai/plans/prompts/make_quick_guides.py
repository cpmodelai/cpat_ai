"""Writes the Word quick guides (CPAT-AI_<Module>_QuickGuide.docx) from the starter-prompt files.

    python make_quick_guides.py [outdir]

A quick guide is the starter file in Word, after six steps to start GitHub Copilot in local mode.
It is a minimal .docx written by hand (a few KB), small enough to attach to an e-mail; the illustrated
guides are written by make_prompt_guides.js.
"""
import re
import sys
import zipfile
from pathlib import Path
from xml.sax.saxutils import escape

HERE = Path(__file__).parent
GUIDES = [('TCB_starter_prompts.md', 'CPAT-AI_TransportCobenefits_QuickGuide.docx', 'CPAT-AI_Prompt_TransportCobenefits.docx'),
          ('AP_starter_prompts.md', 'CPAT-AI_AirPollution_QuickGuide.docx', 'CPAT-AI_Prompt_AirPollution.docx'),
          ('Distribution_starter_prompts.md', 'CPAT-AI_Distribution_QuickGuide.docx', 'CPAT-AI_HowTo_Distribution.docx')]
START = [
    'Sync the repo: double-click SyncRepo.bat in C:\\Users\\WB<PID>\\Repos\\CPAT-AI.',
    'In the GitHub Copilot app, open the CPAT-AI folder (Projects, +, Open folder) and start a session (+ next to it).',
    'Under the prompt box: workspace Current checkout (local mode); model Claude Opus (Auto off); mode Interactive.',
    'Type @ to attach AGENTS.md and the module prompt file, then send the starter prompt below.',
    'Approve each step; refuse deletions, changes to excel_ai/legacy/ and pushes. Read each report before the next prompt.',
    'Send one starter query or phase at a time.',
]

W = 'xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main"'


def run(text, bold=False, mono=False, size=21, color=None):
    props = ['<w:rFonts w:ascii="Consolas" w:hAnsi="Consolas"/>' if mono else '<w:rFonts w:ascii="Arial" w:hAnsi="Arial"/>']
    if bold:
        props.append('<w:b/>')
    if color:
        props.append(f'<w:color w:val="{color}"/>')
    props.append(f'<w:sz w:val="{size}"/>')
    return f'<w:r><w:rPr>{"".join(props)}</w:rPr><w:t xml:space="preserve">{escape(text)}</w:t></w:r>'


def inline(text, size=21):
    """`code` in Consolas, **bold** in bold, the rest in Arial."""
    out = []
    for part in re.split(r'(`[^`]+`|\*\*[^*]+\*\*)', text):
        if not part:
            continue
        if part.startswith('`'):
            out.append(run(part[1:-1], mono=True, size=size - 2))
        elif part.startswith('**'):
            out.append(run(part[2:-2], bold=True, size=size))
        else:
            out.append(run(part, size=size))
    return ''.join(out)


def para(runs, after=100, num=None, shade=False, indent=None):
    ppr = []                                   # schema order: numPr, pBdr, shd, spacing, ind
    if num is not None:
        ppr.append(f'<w:numPr><w:ilvl w:val="0"/><w:numId w:val="{num}"/></w:numPr>')
    if shade:
        ppr.append('<w:pBdr><w:top w:val="single" w:sz="4" w:space="2" w:color="BFBFBF"/>'
                   '<w:left w:val="single" w:sz="4" w:space="4" w:color="BFBFBF"/>'
                   '<w:bottom w:val="single" w:sz="4" w:space="2" w:color="BFBFBF"/>'
                   '<w:right w:val="single" w:sz="4" w:space="4" w:color="BFBFBF"/></w:pBdr>'
                   '<w:shd w:val="clear" w:color="auto" w:fill="F2F2F2"/>')
    ppr.append(f'<w:spacing w:after="{after}"/>')
    if indent:
        ppr.append(f'<w:ind w:left="{indent}"/>')
    return f'<w:p><w:pPr>{"".join(ppr)}</w:pPr>{runs}</w:p>'


def heading(text, size=26):
    return para(run(text, bold=True, size=size, color='00AE49'), after=80)


def body(md_text, full_guide):
    lines = md_text.splitlines()
    out = []
    title = lines[0].lstrip('# ').strip()
    out.append(para(run(title, bold=True, size=32, color='00AE49'), after=60))
    out.append(para(inline('CPAT-AI quick guide · prompts in `excel_ai/plans/prompts/` · illustrated guide: '
                           f'`{full_guide}`', size=18), after=160))
    out.append(heading('How to start (GitHub Copilot, local mode)'))
    out += [para(inline(s), num=2, after=40) for s in START]
    code, label = None, None
    for line in lines[1:]:
        if line.startswith('```'):
            if code is None:
                code = []
            else:
                out.append(para(''.join(run(c, mono=True, size=18) + '<w:br/>' for c in code)[:-len('<w:br/>')],
                                shade=True, after=120, indent=360 if label else None))
                code, label = None, None
            continue
        if code is not None:
            code.append(line)
        elif line.startswith('## '):
            out.append(heading(line[3:]))
        elif line.startswith('- '):
            label = line[2:]
            out.append(para(inline(label), num=1, after=40))
        elif line.strip():
            out.append(para(inline(re.sub(r'\[([^\]]+)\]\([^)]+\)', r'\1', line))))
    return ''.join(out)


def numbering():
    def absn(i, fmt, text):
        return (f'<w:abstractNum w:abstractNumId="{i}"><w:lvl w:ilvl="0"><w:start w:val="1"/><w:numFmt w:val="{fmt}"/>'
                f'<w:lvlText w:val="{text}"/><w:lvlJc w:val="left"/><w:pPr><w:ind w:left="360" w:hanging="270"/></w:pPr>'
                '</w:lvl></w:abstractNum>')
    return (f'<?xml version="1.0" encoding="UTF-8" standalone="yes"?><w:numbering {W}>'
            + absn(0, 'bullet', '\u2022') + absn(1, 'decimal', '%1.')
            + '<w:num w:numId="1"><w:abstractNumId w:val="0"/></w:num><w:num w:numId="2"><w:abstractNumId w:val="1"/></w:num>'
            '</w:numbering>')


def write(md_file, out_path, full_guide):
    doc = (f'<?xml version="1.0" encoding="UTF-8" standalone="yes"?><w:document {W}><w:body>'
           + body((HERE / md_file).read_text(encoding='utf-8'), full_guide)
           + '<w:sectPr><w:pgSz w:w="12240" w:h="15840"/><w:pgMar w:top="1080" w:right="1080" w:bottom="1080" '
             'w:left="1080" w:header="720" w:footer="720" w:gutter="0"/></w:sectPr></w:body></w:document>')
    ct = ('<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
          '<Types xmlns="http://schemas.openxmlformats.org/package/2006/content-types">'
          '<Default Extension="rels" ContentType="application/vnd.openxmlformats-package.relationships+xml"/>'
          '<Default Extension="xml" ContentType="application/xml"/>'
          '<Override PartName="/word/document.xml" ContentType="application/vnd.openxmlformats-officedocument.'
          'wordprocessingml.document.main+xml"/>'
          '<Override PartName="/word/numbering.xml" ContentType="application/vnd.openxmlformats-officedocument.'
          'wordprocessingml.numbering+xml"/></Types>')
    rels = ('<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
            '<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">'
            '<Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/'
            'officeDocument" Target="word/document.xml"/></Relationships>')
    drels = ('<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
             '<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">'
             '<Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/'
             'numbering" Target="numbering.xml"/></Relationships>')
    with zipfile.ZipFile(out_path, 'w', zipfile.ZIP_DEFLATED, compresslevel=9) as z:
        for name, text in (('[Content_Types].xml', ct), ('_rels/.rels', rels), ('word/document.xml', doc),
                           ('word/_rels/document.xml.rels', drels), ('word/numbering.xml', numbering())):
            z.writestr(name, text)
    print(out_path, out_path.stat().st_size)


if __name__ == '__main__':
    out = Path(sys.argv[1]) if len(sys.argv) > 1 else HERE
    for md, docx, full in GUIDES:
        write(md, out / docx, full)
