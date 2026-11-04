"""Build the SOC Document Kit.

Reads soc-kit/src/<group>/*.md, writes Word files to docs/downloads/soc-kit/<group>/ and the
download page docs/soc-kit/index.md.

Source format (a small markdown subset):

    ---
    id: SOP-01
    title: Shift Start and Platform Health Check
    owner: SOC Lead
    audience: L1 analyst, shift lead
    review: Every 6 months
    summary: One sentence on what the document is for.
    ---
    ## Heading 2 / ### Heading 3
    Paragraph text with **bold**, *italic* and `code`.
    - bullet            1. numbered step        - [ ] checkbox
    | table | header |  (first row is the header; |---| separator line is skipped)
    > NOTE: callout     (NOTE, TIP, WARNING, EXAMPLE)
    ```lang ... ```     code block
    ---page---          page break

Usage: python soc-kit/build.py
"""
import os
import re
import sys
import glob

from docx import Document
from docx.enum.section import WD_ORIENT
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.enum.text import WD_ALIGN_PARAGRAPH, WD_BREAK, WD_TAB_ALIGNMENT
from docx.oxml import OxmlElement
from docx.oxml.ns import qn
from docx.shared import Pt, Cm, Inches, RGBColor

ROOT = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(ROOT)
SRC = os.path.join(ROOT, 'src')
OUT = os.path.join(REPO, 'docs', 'downloads', 'soc-kit')
PAGE = os.path.join(REPO, 'docs', 'soc-kit', 'index.md')

NAVY = RGBColor(0x1F, 0x38, 0x64)
GREY = RGBColor(0x59, 0x59, 0x59)
FONT = 'Calibri'
CODE_FONT = 'Consolas'
HEAD_FILL = 'DEEAF6'
LABEL_FILL = 'F2F2F2'
CALLOUT = {'NOTE': ('DEEAF6', 'Note'), 'TIP': ('E2F0D9', 'Tip'),
           'WARNING': ('FBE5E5', 'Warning'), 'EXAMPLE': ('FFF2CC', 'Example')}

GROUPS = {
    'gov': ('GOV', 'Governance', 'Governance Document'),
    'sop': ('SOP', 'Standard Operating Procedures', 'Standard Operating Procedure'),
    'pb': ('PB', 'Incident Response Playbooks', 'Incident Response Playbook'),
    'tpl': ('TPL', 'Forms, Reports and Records', 'Form and Record'),
}

# Characters that make a document look machine-written; replaced on the way in.
PLAIN = [('—', ', '), ('–', '-'), ('→', 'to'), ('·', '|'), ('…', '...')]


def plain(text):
    for a, b in PLAIN:
        text = text.replace(a, b)
    return text


# ---------------------------------------------------------------- low-level helpers

def shade(cell, fill):
    tcPr = cell._tc.get_or_add_tcPr()
    shd = OxmlElement('w:shd')
    shd.set(qn('w:val'), 'clear')
    shd.set(qn('w:color'), 'auto')
    shd.set(qn('w:fill'), fill)
    tcPr.append(shd)


def borders(table, color='BFBFBF'):
    tblPr = table._tbl.tblPr
    b = OxmlElement('w:tblBorders')
    for side in ('top', 'left', 'bottom', 'right', 'insideH', 'insideV'):
        e = OxmlElement(f'w:{side}')
        e.set(qn('w:val'), 'single')
        e.set(qn('w:sz'), '4')
        e.set(qn('w:color'), color)
        b.append(e)
    tblPr.append(b)


def repeat_header(row):
    trPr = row._tr.get_or_add_trPr()
    e = OxmlElement('w:tblHeader')
    e.set(qn('w:val'), 'true')
    trPr.append(e)


def field(paragraph, code, size=8):
    """Insert a Word field such as PAGE or NUMPAGES."""
    run = paragraph.add_run()
    run.font.size = Pt(size)
    for kind, text in (('begin', None), (None, code), ('separate', None), (None, '1'), ('end', None)):
        if kind:
            e = OxmlElement('w:fldChar')
            e.set(qn('w:fldCharType'), kind)
            run._r.append(e)
        elif text == code:
            e = OxmlElement('w:instrText')
            e.set(qn('xml:space'), 'preserve')
            e.text = f' {code} '
            run._r.append(e)
        else:
            e = OxmlElement('w:t')
            e.text = text
            run._r.append(e)


def toc(doc):
    p = doc.add_paragraph()
    run = p.add_run()
    for kind, text in (('begin', None), ('instr', 'TOC \\o "2-2" \\h \\z \\u'), ('separate', None),
                       ('text', 'Right-click here and choose Update Field to build the table of contents.'), ('end', None)):
        if kind == 'instr':
            e = OxmlElement('w:instrText')
            e.set(qn('xml:space'), 'preserve')
            e.text = text
        elif kind == 'text':
            e = OxmlElement('w:t')
            e.text = text
        else:
            e = OxmlElement('w:fldChar')
            e.set(qn('w:fldCharType'), kind)
        run._r.append(e)
    run.font.color.rgb = GREY
    run.font.size = Pt(9)


INLINE = re.compile(r'(\*\*[^*]+\*\*|\*[^*\s][^*]*\*|`[^`]+`)')


def add_runs(paragraph, text, bold=False, size=None, color=None):
    text = plain(text)
    pos = 0
    for m in INLINE.finditer(text):
        if m.start() > pos:
            _run(paragraph, text[pos:m.start()], bold, size, color)
        t = m.group(0)
        if t.startswith('**'):
            _run(paragraph, t[2:-2], True, size, color)
        elif t.startswith('`'):
            _run(paragraph, t[1:-1], bold, size, color, code=True)
        else:
            _run(paragraph, t[1:-1], bold, size, color, italic=True)
        pos = m.end()
    if pos < len(text):
        _run(paragraph, text[pos:], bold, size, color)


def _run(p, text, bold, size, color, italic=False, code=False):
    r = p.add_run(text)
    r.bold = bold
    r.italic = italic
    if size:
        r.font.size = Pt(size)
    if color:
        r.font.color.rgb = color
    if code:
        r.font.name = CODE_FONT
        r._element.rPr.rFonts.set(qn('w:eastAsia'), CODE_FONT)
        r.font.size = Pt(9)
    return r


def spacing(p, before=0, after=4):
    p.paragraph_format.space_before = Pt(before)
    p.paragraph_format.space_after = Pt(after)


# ---------------------------------------------------------------- document skeleton

def new_document(meta, group):
    doc = Document()
    sec = doc.sections[0]
    sec.page_width, sec.page_height = Cm(21), Cm(29.7)
    sec.orientation = WD_ORIENT.PORTRAIT
    for side in ('left_margin', 'right_margin'):
        setattr(sec, side, Cm(2))
    sec.top_margin, sec.bottom_margin = Cm(2), Cm(1.8)

    st = doc.styles['Normal']
    st.font.name = FONT
    st.element.rPr.rFonts.set(qn('w:eastAsia'), FONT)
    st.font.size = Pt(10.5)
    st.paragraph_format.space_after = Pt(4)
    for name, size in (('Heading 1', 18), ('Heading 2', 13.5), ('Heading 3', 11.5)):
        h = doc.styles[name]
        h.font.name = FONT
        h.element.rPr.rFonts.set(qn('w:eastAsia'), FONT)
        h.font.size = Pt(size)
        h.font.bold = True
        h.font.color.rgb = NAVY
        h.paragraph_format.space_before = Pt(12 if name != 'Heading 1' else 0)
        h.paragraph_format.space_after = Pt(4)
        h.paragraph_format.keep_with_next = True

    # header and footer
    hp = sec.header.paragraphs[0]
    hp.text = ''
    add_runs(hp, '[ORGANISATION]  |  Security Operations Center', size=8, color=GREY)
    stops = hp.paragraph_format.tab_stops
    for inherited in (Inches(3.25), Inches(6.5)):      # Header style defaults are for US Letter
        stops.add_tab_stop(inherited, WD_TAB_ALIGNMENT.CLEAR)
    stops.add_tab_stop(Cm(17), WD_TAB_ALIGNMENT.RIGHT)
    hp.add_run('\t')
    add_runs(hp, meta['id'], bold=True, size=8, color=NAVY)
    fp = sec.footer.paragraphs[0]
    add_runs(fp, f"{meta['id']} {meta['title']}  |  Version {meta.get('version', '1.0')}  |  "
                 f"Classification: {meta.get('classification', 'Internal')}  |  Page ", size=8, color=GREY)
    field(fp, 'PAGE')
    _run(fp, ' of ', False, 8, GREY)
    field(fp, 'NUMPAGES')

    # title block
    p = doc.add_paragraph()
    add_runs(p, GROUPS[group][2].upper(), bold=True, size=9, color=GREY)
    spacing(p, 0, 0)
    doc.add_heading(plain(meta['title']), level=1)
    if meta.get('summary'):
        p = doc.add_paragraph()
        add_runs(p, meta['summary'], color=GREY)

    rows = [('Document ID', meta['id']), ('Version', meta.get('version', '1.0')),
            ('Owner', meta.get('owner', 'SOC Lead')), ('Approved by', meta.get('approver', '[Name, role]')),
            ('Audience', meta.get('audience', 'SOC team')), ('Classification', meta.get('classification', 'Internal')),
            ('Effective date', '[dd-mmm-yyyy]'), ('Review', meta.get('review', 'Every 12 months, and after any major incident'))]
    if group == 'tpl':
        rows = [r for r in rows if r[0] in ('Document ID', 'Version', 'Owner', 'Classification')]
        rows.append(('When used', meta.get('used', 'As needed')))
    t = doc.add_table(rows=0, cols=4)
    borders(t)
    for i in range(0, len(rows), 2):
        cells = t.add_row().cells
        for j, (k, v) in enumerate(rows[i:i + 2]):
            cells[j * 2].text = ''
            add_runs(cells[j * 2].paragraphs[0], k, bold=True, size=9)
            shade(cells[j * 2], LABEL_FILL)
            add_runs(cells[j * 2 + 1].paragraphs[0], v, size=9)
    _widths(t, [3.2, 5.3, 3.2, 5.3])

    if group != 'tpl':
        p = doc.add_paragraph()
        spacing(p, 8, 2)
        add_runs(p, 'Version history', bold=True, size=9, color=NAVY)
        vt = doc.add_table(rows=1, cols=4)
        borders(vt)
        for c, h in zip(vt.rows[0].cells, ('Version', 'Date', 'Author', 'Change')):
            add_runs(c.paragraphs[0], h, bold=True, size=9)
            shade(c, HEAD_FILL)
        for v in (('1.0', '[dd-mmm-yyyy]', '[Name]', 'First release'), ('', '', '', '')):
            cells = vt.add_row().cells
            for c, x in zip(cells, v):
                add_runs(c.paragraphs[0], x, size=9)
        _widths(vt, [2, 3, 4, 8])
        if meta.get('toc', 'yes') == 'yes':
            p = doc.add_paragraph()
            spacing(p, 8, 2)
            add_runs(p, 'Contents', bold=True, size=9, color=NAVY)
            toc(doc)
    return doc


def _widths(table, cms):
    table.alignment = WD_TABLE_ALIGNMENT.CENTER
    table.autofit = False
    for row in table.rows:
        for cell, w in zip(row.cells, cms):
            cell.width = Cm(w)


# ---------------------------------------------------------------- body parser

def parse(path):
    text = open(path, encoding='utf-8').read().replace('\r\n', '\n')
    m = re.match(r'---\n(.*?)\n---\n', text, re.S)
    if not m:
        sys.exit(f'{path}: missing front matter')
    meta = {}
    for line in m.group(1).split('\n'):
        if ':' in line:
            k, v = line.split(':', 1)
            v = v.strip()
            if len(v) > 1 and v[0] == v[-1] and v[0] in '"\'':    # quoted value, e.g. a title with a colon
                v = v[1:-1]
            meta[k.strip()] = v
    for k in ('id', 'title'):
        if k not in meta:
            sys.exit(f'{path}: front matter needs {k}')
    return meta, text[m.end():]


def render_body(doc, body):
    lines = body.split('\n')
    i, num = 0, 0
    while i < len(lines):
        line = lines[i]
        s = line.strip()
        if not s:
            num = 0
            i += 1
            continue
        if s == '---page---':
            doc.add_paragraph().add_run().add_break(WD_BREAK.PAGE)
        elif s.startswith('```'):
            code = []
            i += 1
            while i < len(lines) and not lines[i].strip().startswith('```'):
                code.append(lines[i])
                i += 1
            _code_block(doc, code)
        elif s.startswith('|'):
            rows = []
            while i < len(lines) and lines[i].strip().startswith('|'):
                r = lines[i].strip()
                if not re.match(r'^\|[\s:|-]+\|$', r):
                    rows.append([c.strip() for c in r.strip('|').split('|')])
                i += 1
            _table(doc, rows)
            continue
        elif s.startswith('>'):
            block = []
            while i < len(lines) and lines[i].strip().startswith('>'):
                block.append(lines[i].strip()[1:].strip())
                i += 1
            _callout(doc, block)
            continue
        elif s.startswith('### '):
            doc.add_heading(plain(s[4:]), level=3)
        elif s.startswith('## '):
            doc.add_heading(plain(s[3:]), level=2)
        elif re.match(r'^- \[[ xX]\] ', s):
            p = doc.add_paragraph()
            p.paragraph_format.left_indent = Cm(0.9 + _indent(line))
            p.paragraph_format.first_line_indent = Cm(-0.6)
            spacing(p, 0, 2)
            mark = '☑' if s[3] in 'xX' else '☐'
            _run(p, mark + '  ', False, 11, NAVY)
            add_runs(p, s[6:])
        elif s.startswith('- '):
            p = doc.add_paragraph(style='List Bullet' if _indent(line) == 0 else 'List Bullet 2')
            spacing(p, 0, 2)
            add_runs(p, s[2:])
        elif re.match(r'^\d+\. ', s):
            num += 1
            n, rest = s.split('. ', 1)
            p = doc.add_paragraph()
            p.paragraph_format.left_indent = Cm(0.9 + _indent(line))
            p.paragraph_format.first_line_indent = Cm(-0.6)
            spacing(p, 0, 3)
            _run(p, f'{n}.  ', True, None, NAVY)
            add_runs(p, rest)
        else:
            p = doc.add_paragraph()
            add_runs(p, s)
        i += 1


def _indent(line):
    return 0.6 * ((len(line) - len(line.lstrip(' '))) // 2)


def _table(doc, rows):
    cols = max(len(r) for r in rows)
    t = doc.add_table(rows=0, cols=cols)
    borders(t)
    for ri, r in enumerate(rows):
        cells = t.add_row().cells
        for ci in range(cols):
            v = r[ci] if ci < len(r) else ''
            add_runs(cells[ci].paragraphs[0], v, bold=(ri == 0), size=9)
            if ri == 0:
                shade(cells[ci], HEAD_FILL)
        if ri == 0:
            repeat_header(t.rows[0])
    total = 17.0
    if cols == 2:
        w = [5.5, 11.5]
    elif cols >= 4:
        # first column usually holds the row label, give it more room
        longest = max(len(r[0]) for r in rows if r)
        w0 = 1.6 if longest <= 6 else min(5.0, total * 0.3)
        w = [w0] + [(total - w0) / (cols - 1)] * (cols - 1)
    else:
        w = [total / cols] * cols
    _widths(t, w)
    doc.add_paragraph().paragraph_format.space_after = Pt(2)


def _callout(doc, block):
    kind = 'NOTE'
    m = re.match(r'^(NOTE|TIP|WARNING|EXAMPLE):\s*', block[0])
    if m:
        kind = m.group(1)
        block[0] = block[0][m.end():]
    fill, label = CALLOUT[kind]
    t = doc.add_table(rows=1, cols=1)
    borders(t, 'D9D9D9')
    c = t.rows[0].cells[0]
    shade(c, fill)
    p = c.paragraphs[0]
    add_runs(p, label + ': ', bold=True, size=9.5, color=NAVY)
    add_runs(p, ' '.join(x for x in block if x), size=9.5)
    _widths(t, [17])
    doc.add_paragraph().paragraph_format.space_after = Pt(2)


def _code_block(doc, code):
    t = doc.add_table(rows=1, cols=1)
    borders(t, 'D9D9D9')
    c = t.rows[0].cells[0]
    shade(c, 'F7F7F7')
    p = c.paragraphs[0]
    for k, line in enumerate(code):
        if k:
            p.add_run().add_break()
        _run(p, plain(line) or ' ', False, None, None, code=True)
    _widths(t, [17])
    doc.add_paragraph().paragraph_format.space_after = Pt(2)


# ---------------------------------------------------------------- download page

def write_page(built):
    order = ['gov', 'sop', 'pb', 'tpl']
    out = ['# SOC Document Kit', '',
           'Editable Word documents that a Security Operations Center (SOC) needs to run day to day: governance documents, '
           'standard operating procedures (SOPs), incident response playbooks, and the forms and reports the team fills in.', '',
           '!!! abstract "At a glance"',
           '    - Audience: SOC analysts, shift leads, SOC managers, anyone building a SOC',
           '    - Format: Microsoft Word (.docx), free to adapt under CC BY 4.0',
           '    - Outcome: a ready document set you can brand and approve for your own organisation in days, not months', '',
           '## How to use the kit', '',
           '- [ ] Download the document and replace every `[PLACEHOLDER]` in square brackets, starting with `[ORGANISATION]`.',
           '- [ ] Change tool names to the ones you run. Each document names the capability first and the tool as an example.',
           '- [ ] Right-click the table of contents and choose Update Field.',
           '- [ ] Get the document approved, fill in the version history, and set a review date.', '',
           'The full list of planned documents is in the '
           '[catalogue](https://github.com/alnomanbd/The-Defensive-Mind/blob/main/soc-kit/CATALOGUE.md). '
           'New documents are added in batches.', '']
    for g in order:
        items = sorted(built.get(g, []), key=lambda x: _sort_key(x[0]['id']))
        out += [f'## {GROUPS[g][1]}', '']
        if not items:
            out += ['Coming soon.', '']
            continue
        out += ['| ID | Document | Download |', '|---|---|---|']
        for meta, rel in items:
            out.append(f"| {meta['id']} | {plain(meta['title'])} | [Word (.docx)](../downloads/soc-kit/{rel}) |")
        out.append('')
    out += ['## Related pages', '', '- [SOC Training](../training/index.md)', '- [Daily routine](../02-daily-operations/daily-routine.md)',
            '- [Playbooks](../04-playbooks/index.md)', '- [Templates](../09-templates/index.md)', '']
    os.makedirs(os.path.dirname(PAGE), exist_ok=True)
    open(PAGE, 'w', encoding='utf-8', newline='\n').write('\n'.join(out))


def _sort_key(doc_id):
    m = re.match(r'([A-Z]+)-(\d+)', doc_id)
    return (m.group(1), int(m.group(2))) if m else (doc_id, 0)


def main():
    built = {}
    for g in GROUPS:
        for path in sorted(glob.glob(os.path.join(SRC, g, '*.md'))):
            meta, body = parse(path)
            doc = new_document(meta, g)
            render_body(doc, body)
            name = os.path.splitext(os.path.basename(path))[0] + '.docx'
            os.makedirs(os.path.join(OUT, g), exist_ok=True)
            doc.save(os.path.join(OUT, g, name))
            built.setdefault(g, []).append((meta, f'{g}/{name}'))
            print('built', meta['id'], name)
    write_page(built)
    print('page', os.path.relpath(PAGE, REPO))


if __name__ == '__main__':
    main()
