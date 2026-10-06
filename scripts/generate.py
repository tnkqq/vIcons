#!/usr/bin/env python3
"""Generate four reference-inspired icon themes, with dark/light SVG variants."""
import html
import json
from pathlib import Path
import xml.etree.ElementTree as ET
from design import GROUPS, SHAPES

ROOT = Path(__file__).resolve().parents[1]
CATALOGUE = json.loads((ROOT.parent / 'vip-file-extensions.json').read_text(encoding='utf-8'))
CATALOGUE['.vill'] = 'Дополнительное расширение .vill; в исходном проекте используются библиотеки .vil.'
PALETTES = {
    'violet': {'label': 'Violet Orbit', 'body': ('#C4A2FF', '#9867E8'), 'orbit': ('#91ECE1', '#35BFB8'), 'star': '#F4BE69'},
    'blue': {'label': 'Blue Orbit', 'body': ('#8EAFFF', '#4775E8'), 'orbit': ('#A0E8FF', '#42B9EA'), 'star': '#C3C5FF'},
    'amber': {'label': 'Amber Orbit', 'body': ('#FFAD43', '#F56A08'), 'orbit': ('#FFE486', '#F8BC25'), 'star': '#FFE1A0'},
    'mono': {'label': 'Monochrome Orbit', 'body': ('#EEEEEE', '#B8B8B8'), 'orbit': ('#AAAAAA', '#777777'), 'star': '#DADADA'},
}
# All native VIP formats stay within the selected theme's palette.
VIP_FORMATS = set('vip vih vpp vil vill vin obj inc var const fnc prj vpr ver lot gcd dic mem tbl dlg win mnu mnh tb bmc frm pro frn fr3 lst old'.split())
CORE = ['vip', 'vih', 'vpp', 'vil', 'vill', 'prj']
# Full-height lettermarks use the extension's letters, never corner badges.
LETTERMARKS = {'vip': 'V', 'vih': 'VH', 'vpp': 'VP', 'vil': 'VL',
               'vill': 'LL', 'prj': 'P', 'vin': 'VN', 'obj': 'VO', 'inc': 'VI'}
GLYPHS = {
    'V': '<path d="M0 0 3.5 12 7 0"/>',
    'H': '<path d="M0 0v12M7 0v12M0 6h7"/>',
    'P': '<path d="M0 12V0h3.5a3.5 3.5 0 0 1 0 7H0"/>',
    'L': '<path d="M0 0v12h7"/>',
    'N': '<path d="M0 12V0l7 12V0"/>',
    'O': '<rect x="0" y="0" width="7" height="12" rx="3.5"/>',
    'I': '<path d="M0 0h7M3.5 0v12M0 12h7"/>',
}


def lettermark(ext):
    letters = LETTERMARKS[ext]
    # Every glyph uses the same 7×12 grid and 2.6 stroke, without scaling or slant.
    positions = [8.5] if len(letters) == 1 else [3, 14]
    shapes = []
    for index, (x, ch) in enumerate(zip(positions, letters)):
        ink = 'body' if index == 0 else 'orbit'
        shapes.append(f'<g data-letter="{ch}" transform="translate({x} 6)" stroke="url(#{ink})">' + GLYPHS[ch] + '</g>')
    return '<g data-lettermark="' + letters + '" fill="none" stroke-width="2.6" stroke-linecap="round" stroke-linejoin="round">' + ''.join(shapes) + '</g>'


def write_json(path, data):
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')


def colours(palette, ext, group_colour, light):
    p = PALETTES[palette]
    if palette == 'mono':
        return (('#6A6A6A', '#303030'), ('#909090', '#606060'), '#454545') if light else (p['body'], p['orbit'], p['star'])
    if ext in VIP_FORMATS or ext.startswith('folder'):
        body, orbit, star = p['body'], p['orbit'], p['star']
    else:
        # Companion formats have semantic colours, independent of VIP brand colours.
        c = '#22A06B' if ext in {'xml', 'json', 'yml', 'iml'} else '#4388DC' if ext in {'docx', 'rtf', 'txt', 'lst'} else group_colour
        body, orbit, star = (c, c), p['orbit'], p['star']
    if light:
        def darker(c):
            return '#' + ''.join(f'{int(int(c[n:n+2],16)*.72):02X}' for n in (1, 3, 5))
        body = tuple(darker(c) for c in body)
        orbit = tuple(darker(c) for c in orbit)
        star = darker(star)
    return body, orbit, star


def svg(ext, kind, palette, group_colour, light=False):
    body, orbit, star = colours(palette, ext, group_colour, light)
    defs = f'''<defs>
<linearGradient id="body" x1="0" y1="0" x2="1" y2="1"><stop stop-color="{body[0]}"/><stop offset="1" stop-color="{body[1]}"/></linearGradient>
<linearGradient id="orbit" gradientUnits="userSpaceOnUse" x1="1" y1="9" x2="23" y2="16"><stop stop-color="{orbit[0]}"/><stop offset="1" stop-color="{orbit[1]}"/></linearGradient>
</defs>'''
    if ext in LETTERMARKS:
        logo = lettermark(ext)
        if len(LETTERMARKS[ext]) == 1:
            # A surrounding orbit stays outside the glyph bounds. No front overlay,
            # satellite, clipping or scaled letters. Compound marks have no orbit.
            logo = '<ellipse data-orbit="surround" cx="12" cy="12" rx="10.7" ry="10.2" transform="rotate(-25 12 12)" fill="none" stroke="url(#orbit)" stroke-width="1.4"/>' + logo
    else:
        shape = SHAPES[kind]
        if ext == 'docx':
            shape = '<path d="M14 3H5v18h14V8l-5-5Zm0 0v5h5m-11 4 1.5 5 2-3 2 3 1.5-5"/>'
        elif ext == 'xml':
            shape = '<path d="m7 5-5 7 5 7m10-14 5 7-5 7m-3-16-4 18"/>'
        elif ext == 'rtf':
            shape = '<path d="M14 3H5v18h14V8l-5-5Zm0 0v5h5M8 11h8m-8 3h8m-8 3h5"/>'

        # A soft depth stroke and solid semantic silhouette match the rounded orbital style.
        logo = '<g fill="none" stroke="url(#body)" stroke-width="3.5" opacity=".16" stroke-linecap="round" stroke-linejoin="round">' + shape + '</g>'
        logo += '<g fill="none" stroke="url(#body)" stroke-width="2.1" stroke-linecap="round" stroke-linejoin="round">' + shape + '</g>'
    return '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24">' + defs + logo + '</svg>\n'


# Only remove old generated SVG/JSON output; user examples and scripts stay in place.
for path in (ROOT / 'icons').glob('*.svg'):
    path.unlink()
for path in (ROOT / 'themes').glob('*.json'):
    path.unlink()

specs = {}
for title, kind, colour, exts in GROUPS:
    for ext in exts.split():
        specs[ext] = (kind, colour)
specs.update({'file': ('file', '#64748B'), 'folder': ('folder', '#D97706'),
              'folder-open': ('folder-open', '#D97706'), 'git': ('git', '#EA580C')})
extensions = {ext: ext for ext in specs if '.' + ext in CATALOGUE}
assert set('.' + ext for ext in extensions) == set(CATALOGUE) - {'(без расширения)'}
contributions = []
for palette, info in PALETTES.items():
    definitions = {}
    for light in [False, True]:
        appearance = 'light' if light else 'dark'
        destination = ROOT / 'icons' / palette / appearance
        destination.mkdir(parents=True, exist_ok=True)
        for ext, (kind, colour) in specs.items():
            content = svg(ext, kind, palette, colour, light)
            ET.fromstring(content)
            (destination / f'{ext}.svg').write_text(content, encoding='utf-8')
            definitions[ext + ('-light' if light else '')] = {'iconPath': f'../icons/{palette}/{appearance}/{ext}.svg'}
    def bindings(suffix=''):
        return {'file': 'file' + suffix, 'folder': 'folder' + suffix, 'folderExpanded': 'folder-open' + suffix,
                'rootFolder': 'folder' + suffix, 'rootFolderExpanded': 'folder-open' + suffix,
                'fileExtensions': {ext: icon + suffix for ext, icon in extensions.items()},
                'fileNames': {'.gitignore': 'git' + suffix, '.name': 'file' + suffix}}
    filename = 'vip-icon-theme.json' if palette == 'violet' else f'vip-{palette}-icon-theme.json'
    write_json(ROOT / 'themes' / filename, {'iconDefinitions': definitions, **bindings(), 'light': bindings('-light')})
    contributions.append({'id': 'vip-file-icons' if palette == 'violet' else f'vip-file-icons-{palette}',
                          'label': 'vIcons — ' + info['label'], 'path': './themes/' + filename})
package = json.loads((ROOT / 'package.json').read_text())
package.setdefault('version', '0.2.3')
package['contributes']['iconThemes'] = contributions
write_json(ROOT / 'package.json', package)
write_json(ROOT / 'icon-groups.json', [{'name': title, 'symbol': kind, 'extensions': exts.split()} for title, kind, colour, exts in GROUPS])


def card(ext, desc, showcase=False):
    sizes = [16, 24, 48] if showcase else [16, 24]
    samples = ''.join(f'<img width="{size}" height="{size}" data-icon="{ext}" src="icons/violet/dark/{ext}.svg" alt="">' for size in sizes)
    if ext in LETTERMARKS:
        desc = LETTERMARKS[ext] + ' · ' + desc
    return f'<article data-extension="{ext}"><div class="samples">{samples}</div><strong>{html.escape(ext if ext in ["file", "folder", "folder-open", "git"] else "." + ext)}</strong><p>{html.escape(desc)}</p></article>'

sections = ['<section><h2>Основные VIP-файлы · 16 / 24 / 48 px</h2><div class="grid showcase">' + ''.join(card(ext, CATALOGUE['.'+ext], True) for ext in CORE) + '</div></section>']
for title, kind, colour, exts in GROUPS:
    sections.append(f'<section><h2>{html.escape(title)}</h2><div class="grid">' + ''.join(card(ext, CATALOGUE['.' + ext]) for ext in exts.split()) + '</div></section>')
sections.append('<section><h2>Служебные файлы и папки</h2><div class="grid">' + ''.join(card(ext, desc) for ext, desc in [('file', 'Прочие файлы / .name'), ('git', '.gitignore'), ('folder', 'Папка'), ('folder-open', 'Открытая папка')]) + '</div></section>')
options = ''.join(f'<option value="{key}">{info["label"]}</option>' for key, info in PALETTES.items())
page = '''<!doctype html>
<html lang="ru"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>vIcons · Orbit</title>
<style>
:root{color-scheme:dark;--bg:#16171c;--panel:#202229;--fg:#ededf3;--muted:#a1a5b3;--border:#363943}
body.light{color-scheme:light;--bg:#f7f8fc;--panel:#fff;--fg:#20212b;--muted:#626776;--border:#dde0e8}
*{box-sizing:border-box}body{margin:0;background:var(--bg);color:var(--fg);font:14px system-ui,sans-serif}
main{max-width:1280px;margin:auto;padding:32px 24px}header{display:flex;justify-content:space-between;gap:24px;align-items:center;flex-wrap:wrap}
h1{font-size:30px;margin:0 0 8px}h2{font-size:17px;margin:32px 0 12px}p{color:var(--muted);line-height:1.5;margin:8px 0 0}
.controls{display:flex;gap:10px;align-items:center;flex-wrap:wrap}button,select,input{background:var(--panel);color:var(--fg);border:1px solid var(--border);padding:10px 14px;border-radius:8px;font:inherit}
button,select{cursor:pointer}.grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(min(100%,260px),1fr));gap:12px}
article{padding:18px;background:var(--panel);border:1px solid var(--border);border-radius:12px}.samples{display:flex;gap:16px;align-items:center;min-height:40px;margin-bottom:12px}
.showcase .samples{min-height:56px}article p{font-size:12px}strong{font:600 15px ui-monospace,monospace}[hidden]{display:none!important}
</style></head><body><main><header><div><h1>vIcons · Orbit</h1><p>4 палитры · 57 расширений · прозрачные SVG · знак V с орбитой</p></div>
<div class="controls"><label for="palette">Палитра</label><select id="palette">OPTIONS</select><button type="button" id="background" aria-pressed="false">Светлый фон</button></div></header>
<p>Основные знаки: V · VH · VP · VL · LL · P. Буквы одного размера и толщины; у парных знаков орбита отсутствует. В монохромной теме расширение определяется буквами и формой. Для светлого фона используются более темные версии значков.</p>
<p><label for="search">Найти расширение </label><input id="search" type="search" placeholder="vip, xml, docx…"></p>
SECTIONS
</main><script>
const palette=document.getElementById('palette'), background=document.getElementById('background');
function update(){const light=document.body.classList.contains('light');document.querySelectorAll('img[data-icon]').forEach(img=>{img.src='icons/'+palette.value+'/'+(light?'light':'dark')+'/'+img.dataset.icon+'.svg';});}
palette.addEventListener('change',update);
background.addEventListener('click',()=>{const light=document.body.classList.toggle('light');background.textContent=light?'Темный фон':'Светлый фон';background.setAttribute('aria-pressed',String(light));update();});
document.getElementById('search').addEventListener('input',event=>{const value=event.target.value.trim().toLowerCase().replace(/^\\./,'');document.querySelectorAll('article').forEach(card=>{card.hidden=!card.dataset.extension.includes(value);});document.querySelectorAll('section').forEach(section=>{section.hidden=!section.querySelector('article:not([hidden])');});});
</script></body></html>
'''.replace('OPTIONS', options).replace('SECTIONS', ''.join(sections))
(ROOT / 'preview.html').write_text(page, encoding='utf-8')
print(f'Generated {len(contributions)} themes, {len(specs)*8} SVGs, {len(extensions)} extension mappings per theme')
