"""BAV, Arch. Cap. S. Pietro, *Madonne coronate*, tomo IV — the TEI transcription as a reading PDF.

The Vulgate.ai transcription of ff. 1r–302v (13 September 2026; see docs/CHAPTER-ARCHIVES.md) is
not kept in the repository. Of its two forms, `Arch.Cap.S.Pietro.Madonne.coron.4.tei.folios.xml`
is the one to give here: the text is identical to the plain `.tei.xml`, but each <pb> carries the
BAV folio (xml:id "f3r") and the viewer URL (corresp), which become the folio headings, their links
and the PDF bookmarks. The page images are not included; the text is printed as the OCR gives it.

The TEI is written out as HTML and printed with headless Chromium — the shell Playwright installs
under ~/.cache/ms-playwright, or the binary named in $CHROME — because the 8,000-odd combining
macrons need real mark positioning. FreeSerif (fonts-freefont-ttf) covers the macrons, the long s
and the MUFI abbreviations (ꝑ ꝛ ℟ ℣ ℔); Unifont catches the two or three signs it lacks.

Usage: python3 scripts/acsp_tei_to_pdf.py IN.tei.folios.xml [OUT.pdf]
(OUT defaults to IN's name with `.transcription.pdf` in place of `.tei.folios.xml`.)
"""
import glob
import os
import pathlib
import subprocess
import sys
import tempfile
from html import escape
from lxml import etree

TEI = '{http://www.tei-c.org/ns/1.0}'
XMLID = '{http://www.w3.org/XML/1998/namespace}id'
VIEWER = 'https://digi.vatlib.it/view/ARC_Arch.Cap.S.Pietro.Madonne.coron.4'

CSS = r"""
@page {
  size: A4;
  margin: 22mm 20mm 20mm 20mm;
  @top-center { content: "BAV, ACSP, Madonne coronate, tomo IV — machine transcription";
                font: italic 8pt FreeSerif, serif; color: #666; }
  @bottom-center { content: counter(page); font: 9pt FreeSerif, serif; color: #444; }
}
@page :first { @top-center { content: none; } @bottom-center { content: none; } }
html { font-family: FreeSerif, "DejaVu Serif", "Unifont Upper", Unifont, serif;
       font-size: 10.5pt; line-height: 1.38; color: #111; }
body { margin: 0; }
a { color: inherit; text-decoration: none; }
.title-page { page-break-after: always; text-align: center; padding-top: 45mm; }
.title-page h1 { font-size: 22pt; font-weight: normal; margin: 0 0 4mm; letter-spacing: .02em; }
.title-page .sub { font-size: 13pt; font-style: italic; margin-bottom: 14mm; }
.title-page .meta { font-size: 10pt; text-align: left; max-width: 135mm; margin: 0 auto; }
.title-page .meta p { margin: 0 0 3mm; }
.title-page table { border-collapse: collapse; margin: 4mm 0; font-size: 9.5pt; }
.title-page td { padding: 1mm 3mm 1mm 0; vertical-align: top; }
.title-page td:first-child { white-space: nowrap; color: #333; }
h2.folio { font-size: 9.5pt; font-weight: bold; margin: 7mm 0 2mm; padding-top: 1.5mm;
           border-top: .6pt solid #999; break-after: avoid; display: flex;
           justify-content: space-between; letter-spacing: .03em; }
h2.folio .aux { font-weight: normal; color: #666; font-size: 8.5pt; }
.blank { color: #888; font-style: italic; font-size: 9pt; margin: 0 0 2mm; }
p, .head, .l, .note, .fw { white-space: pre-line; }
p { margin: 0 0 2.2mm; text-align: justify; hyphens: auto; }
.head { text-align: center; font-weight: bold; margin: 3mm 0 2mm; break-after: avoid; }
.head.n1 { font-size: 13pt; }
.head.n2 { font-size: 11.5pt; }
.head.n3 { font-size: 10.5pt; font-weight: normal; font-style: italic; }
.note.margin { font-size: 8.8pt; color: #333; margin: 1mm 0 2mm 0; padding: .5mm 0 .5mm 3mm;
               border-left: 1.6pt solid #b9a46a; break-inside: avoid; }
.note .lbl, .fw .lbl { font-family: "DejaVu Sans", sans-serif; font-size: 6.5pt; color: #8a7a4a;
                       text-transform: uppercase; letter-spacing: .06em; margin-right: 1.5mm;
                       font-style: normal; }
.note.caption { font-size: 9pt; text-align: center; font-style: italic; margin: 1mm 0 2mm; }
.note.footnote { font-size: 8.8pt; border-top: .4pt solid #bbb; padding-top: 1mm; margin: 2mm 0; }
.fw { font-size: 8.5pt; color: #666; text-align: right; margin: 0 0 2mm; }
.lg { margin: 2mm 0 3mm 8mm; break-inside: avoid; }
.l { margin: 0; }
.milestone { text-align: center; color: #777; margin: 2mm 0; letter-spacing: .1em; }
table.tei { border-collapse: collapse; margin: 2mm 0 3mm; font-size: 9.5pt; }
table.tei td { padding: .6mm 3mm .6mm 0; vertical-align: top; }
ul.tei { margin: 1mm 0 2mm; padding-left: 0; list-style: none; }
.p-commentary { font-size: 9.5pt; color: #333; }
sup { font-size: 70%; line-height: 0; }
"""


def inline(el):
    """Serialize the mixed content of el (text + <hi>) as HTML."""
    out = [escape(el.text or '')]
    for ch in el:
        tag = ch.tag.replace(TEI, '') if isinstance(ch.tag, str) else None
        if tag == 'hi':
            rend = ch.get('rend', '')
            t = {'italic': 'i', 'bold': 'b', 'sup': 'sup'}.get(rend, 'span')
            out.append(f'<{t}>{inline(ch)}</{t}>')
        elif tag is not None:
            out.append(inline(ch))
        out.append(escape(ch.tail or ''))
    return ''.join(out)


def block(el, html):
    tag = el.tag.replace(TEI, '')
    if tag == 'p':
        cls = f' class="p-{el.get("type")}"' if el.get('type') == 'commentary' else ''
        html.append(f'<p{cls}>{inline(el)}</p>')
    elif tag == 'head':
        html.append(f'<div class="head n{el.get("n", "2")}">{inline(el)}</div>')
    elif tag == 'note':
        kind = el.get('type') or ('margin' if el.get('place') == 'margin' else 'note')
        if kind == 'margin' or el.get('place') == 'margin':
            html.append(f'<div class="note margin"><span class="lbl">marg.</span>{inline(el)}</div>')
        elif kind == 'caption':
            html.append(f'<div class="note caption"><span class="lbl">caption</span>{inline(el)}</div>')
        else:
            html.append(f'<div class="note footnote">{inline(el)}</div>')
    elif tag == 'fw':
        lbl = {'catchword': 'catchword', 'signature': 'signature'}.get(el.get('type'), '')
        lbl = f'<span class="lbl">{lbl}</span>' if lbl else ''
        html.append(f'<div class="fw">{lbl}{inline(el)}</div>')
    elif tag == 'lg':
        html.append('<div class="lg">')
        for l in el:
            html.append(f'<div class="l">{inline(l)}</div>')
        html.append('</div>')
    elif tag == 'milestone':
        html.append(f'<div class="milestone">{escape(el.get("rend") or "—")}</div>')
    elif tag == 'table':
        html.append('<table class="tei">')
        for row in el:
            html.append('<tr>' + ''.join(f'<td>{inline(c)}</td>' for c in row) + '</tr>')
        html.append('</table>')
    elif tag == 'list':
        html.append('<ul class="tei">' + ''.join(f'<li>{inline(i)}</li>' for i in el) + '</ul>')
    else:
        raise ValueError(f'unhandled element <{tag}>')


def to_html(src, dst):
    body = etree.parse(src).getroot().find(f'{TEI}text/{TEI}body')
    kids = [k for k in body if isinstance(k.tag, str)]
    html = [f'<!doctype html><html lang="it"><head><meta charset="utf-8">'
            f'<title>Madonne coronate, tomo IV (1689–1714) — transcription</title>'
            f'<style>{CSS}</style></head><body>']
    first = kids[0].get(XMLID)[1:]
    last = [k for k in kids if k.tag == f'{TEI}pb'][-1].get(XMLID)[1:]
    html.append(f'''<section class="title-page">
<h1>Madonne coronate</h1>
<div class="sub">tomo IV · 1689 – 1714</div>
<div class="meta">
<p>Biblioteca Apostolica Vaticana, Archivio del Capitolo di San Pietro,
<i>Madonne coronate</i>, tomo IV.</p>
<p>Machine transcription (OCR, Vulgate.ai, 13 September 2026) of ff. {first}–{last};
ff. 303r–v were not transcribed. The text is uncorrected: expect broken words, OCR misreadings
and garbled abbreviations. Check every reading against the page images:
<a href="{VIEWER}">{VIEWER.replace("https://", "")}</a>.</p>
<table>
<tr><td><b>f. 3r</b> · img 0007</td><td>Folio, per the BAV foliation, and the image number in the
BAV viewer. Each folio heading links to that image; the PDF bookmarks list every folio.</td></tr>
<tr><td>num. 2 3</td><td>Number(s) written or printed on the leaf itself, where the transcription records them.</td></tr>
<tr><td><span style="border-left:1.6pt solid #b9a46a;padding-left:2mm">marg.</span></td><td>Marginal note,
most often the archivist's (image, church, concession date, cross-reference to <i>Capsulae</i> or decree registers).</td></tr>
<tr><td>catchword, signature</td><td>Running elements at the foot of a page (forme work).</td></tr>
</table>
</div></section>''')
    content_since_pb = True
    for k in kids:
        if k.tag == f'{TEI}pb':
            if not content_since_pb:
                html.append('<div class="blank">[no text transcribed]</div>')
            fid = k.get(XMLID)[1:]
            img = k.get('corresp', '').rsplit('/', 1)[-1]
            printed = k.get('printed')
            aux = f'img {img}' + (f' · num. {escape(printed)}' if printed else '')
            html.append(f'<h2 class="folio" id="f{fid}"><a href="{escape(k.get("corresp", ""))}">f. {fid}</a>'
                        f'<span class="aux">{aux}</span></h2>')
            content_since_pb = False
        else:
            block(k, html)
            content_since_pb = True
    if not content_since_pb:
        html.append('<div class="blank">[no text transcribed]</div>')
    html.append('</body></html>')
    with open(dst, 'w', encoding='utf-8') as f:
        f.write('\n'.join(html))


def chrome():
    if os.environ.get('CHROME'):
        return os.environ['CHROME']
    found = sorted(glob.glob(os.path.expanduser(
        '~/.cache/ms-playwright/chromium_headless_shell-*/*/chrome-headless-shell')))
    if not found:
        sys.exit('no headless Chromium: run `npx playwright install chromium-headless-shell` or set $CHROME')
    return found[-1]


def main(src, dst=None):
    src = pathlib.Path(src).resolve()
    dst = pathlib.Path(dst or str(src).replace('.tei.folios.xml', '.transcription.pdf')).resolve()
    if dst == src:
        sys.exit('give an output path')
    with tempfile.TemporaryDirectory() as tmp:
        html = pathlib.Path(tmp, 'transcription.html')
        to_html(src, html)
        subprocess.run([chrome(), '--no-sandbox', '--disable-gpu', '--no-pdf-header-footer',
                        '--generate-pdf-document-outline', f'--print-to-pdf={dst}', html.as_uri()],
                       check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    print(dst)


if __name__ == '__main__':
    if not 2 <= len(sys.argv) <= 3:
        sys.exit(__doc__)
    main(*sys.argv[1:])
