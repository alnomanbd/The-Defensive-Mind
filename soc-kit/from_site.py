"""Turn published site playbooks into SOC Document Kit sources.

Reads docs/04-playbooks/<page>.md and writes soc-kit/src/pb/PB-XX-<page>.md in the
build.py source format, so the Word playbook and the web page say the same thing.

Conversions: H1 and the "At a glance" box are dropped (they become front matter),
admonitions become callouts, content tabs become a bold label plus the code block,
site links become plain text (external links keep the address in brackets).

Usage: python soc-kit/from_site.py   then   python soc-kit/build.py
"""
import os
import re

ROOT = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(ROOT)
SITE = os.path.join(REPO, 'docs', '04-playbooks')
DEST = os.path.join(ROOT, 'src', 'pb')

PAGES = ['phishing', 'business-email-compromise', 'account-compromise', 'brute-force',
         'credential-leak-dark-web', 'malware-infostealer', 'ransomware', 'web-application-attack',
         'data-exfiltration', 'insider-threat', 'ddos', 'cloud-account-compromise']

KIND = {'warning': 'WARNING', 'danger': 'WARNING', 'note': 'NOTE', 'tip': 'TIP',
        'info': 'NOTE', 'example': 'EXAMPLE', 'success': 'TIP', 'question': 'NOTE'}
LINK = re.compile(r'\[([^\]]+)\]\(([^)]+)\)')


def unlink(text):
    def repl(m):
        label, url = m.group(1), m.group(2)
        return f'{label} ({url})' if url.startswith('http') else label
    return LINK.sub(repl, text)


def quote(v):
    return f'"{v}"' if ':' in v else v


def convert(page):
    lines = open(os.path.join(SITE, page + '.md'), encoding='utf-8').read().replace('\r\n', '\n').split('\n')
    title = re.sub(r'^#\s+(Playbook:\s*)?', '', lines[0]).strip()
    meta = {'title': title, 'audience': '', 'owner': 'SOC Lead', 'id': '', 'summary': ''}
    body, i, in_code = [], 1, False
    while i < len(lines):
        line = lines[i]
        s = line.strip()
        if s.startswith('```'):
            in_code = not in_code
        if not in_code and s.startswith('!!! '):
            m = re.match(r'!!!\s+(\w+)(?:\s+"([^"]*)")?', s)
            kind, head = m.group(1), m.group(2) or ''
            block = []
            i += 1
            while i < len(lines) and (lines[i].startswith('    ') or not lines[i].strip()):
                if lines[i].strip():
                    block.append(lines[i].strip())
                i += 1
                if i < len(lines) and not lines[i].strip() and (i + 1 >= len(lines) or not lines[i + 1].startswith('    ')):
                    break
            if kind == 'abstract':
                for b in block:
                    if b.startswith('- Audience:'):
                        meta['audience'] = b.split(':', 1)[1].strip()
                continue
            text = ' '.join(re.sub(r'^- (\[ \] )?', '', b) for b in block)
            body.append(f'> {KIND.get(kind, "NOTE")}: ' + unlink((head + '. ' if head else '') + text))
            body.append('')
            continue
        if not in_code and s.startswith('=== '):
            body.append('**' + s[4:].strip().strip('"') + '**')
            body.append('')
            i += 1
            while i < len(lines) and (lines[i].startswith('    ') or not lines[i].strip()):
                if lines[i].strip() == '' and i + 1 < len(lines) and not lines[i + 1].startswith('    '):
                    break
                body.append(lines[i][4:] if lines[i].startswith('    ') else '')
                i += 1
            continue
        if not in_code and s.startswith('| **') and '|' in s[3:]:
            cells = [c.strip() for c in s.strip('|').split('|')]
            key = cells[0].strip('*').lower()
            if key == 'id':
                meta['id'] = cells[1]
            elif key == 'owner':
                meta['owner'] = cells[1]
        if not in_code and not meta['summary'] and s and not s.startswith(('|', '!', '#', '-', '>')) and not any(x.strip() for x in body):
            meta['summary'] = unlink(s)
            i += 1
            continue
        body.append(line if in_code else unlink(line))
        i += 1
    text = '\n'.join(body).strip('\n')
    text = re.sub(r'^\| Field \| Value \|', '## Playbook card\n\n| Field | Value |', text, count=1, flags=re.M)
    text = re.sub(r'## Downloads\n.*?(?=\n## )', '', text, flags=re.S)
    text = text.replace('## Related pages', '## Related documents')
    front = ['---', f"id: {meta['id']}", f"title: {quote(meta['title'])}", f"owner: {quote(meta['owner'])}",
             f"audience: {quote(meta['audience'])}",
             'review: Every 12 months, and after every real incident that used this playbook',
             f"summary: {quote(meta['summary'])}", '---', '']
    name = f"{meta['id']}-{page}.md"
    os.makedirs(DEST, exist_ok=True)
    open(os.path.join(DEST, name), 'w', encoding='utf-8').write('\n'.join(front) + text + '\n')
    return name


if __name__ == '__main__':
    for p in PAGES:
        print('wrote', convert(p))
