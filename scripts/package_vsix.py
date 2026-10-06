#!/usr/bin/env python3
"""Package this declarative icon theme without Node.js or external dependencies."""
import json
import posixpath
import struct
from pathlib import Path
from zipfile import ZipFile, ZIP_DEFLATED
import xml.etree.ElementTree as ET

ROOT = Path(__file__).resolve().parents[1]
pkg = json.loads((ROOT / 'package.json').read_text())
NS = 'http://schemas.microsoft.com/developer/vsx-schema/2011'
ET.register_namespace('', NS)
def element(parent, name, attrs=None, text=None):
    child = ET.SubElement(parent, '{' + NS + '}' + name, attrs or {})
    child.text = text
    return child
manifest = ET.Element('{' + NS + '}PackageManifest', {'Version': '2.0.0'})
metadata = element(manifest, 'Metadata')
element(metadata, 'Identity', {'Language': 'en-US', 'Id': pkg['name'], 'Version': pkg['version'], 'Publisher': pkg['publisher']})
element(metadata, 'DisplayName', text=pkg['displayName'])
element(metadata, 'Description', {'{http://www.w3.org/XML/1998/namespace}space': 'preserve'}, pkg['description'])
element(metadata, 'Tags', text='VIP,Galaktika,icons,theme')
element(metadata, 'Categories', text=','.join(pkg['categories']))
element(metadata, 'GalleryFlags', text='Public')
icon_path = None
if pkg.get('icon'):
    icon_path = (ROOT / pkg['icon']).resolve()
    assert icon_path.is_relative_to(ROOT.resolve()), 'Icon must be inside the extension'
    icon_data = icon_path.read_bytes()
    assert icon_data[:8] == b'\x89PNG\r\n\x1a\n', 'Marketplace icon must be PNG'
    assert all(size >= 128 for size in struct.unpack('>II', icon_data[16:24])), 'Icon must be at least 128×128'
    icon_asset_path = 'extension/' + icon_path.relative_to(ROOT.resolve()).as_posix()
    element(metadata, 'Icon', text=icon_asset_path)
properties = element(metadata, 'Properties')
for key, value in {
    'Microsoft.VisualStudio.Code.Engine': pkg['engines']['vscode'],
    'Microsoft.VisualStudio.Code.ExtensionDependencies': '',
    'Microsoft.VisualStudio.Code.ExtensionPack': '',
    'Microsoft.VisualStudio.Code.ExtensionKind': 'ui',
    'Microsoft.VisualStudio.Code.ExecutesCode': 'false',
    'Microsoft.VisualStudio.Services.GitHubFlavoredMarkdown': 'true',
    'Microsoft.VisualStudio.Services.Content.Pricing': 'Free',
}.items():
    element(properties, 'Property', {'Id': key, 'Value': value})
installation = element(manifest, 'Installation')
element(installation, 'InstallationTarget', {'Id': 'Microsoft.VisualStudio.Code'})
element(manifest, 'Dependencies')
assets = element(manifest, 'Assets')
for kind, path in [('Microsoft.VisualStudio.Code.Manifest', 'extension/package.json'),
                   ('Microsoft.VisualStudio.Services.Content.Details', 'extension/README.md'),
                   ('Microsoft.VisualStudio.Services.Content.Changelog', 'extension/CHANGELOG.md')]:
    element(assets, 'Asset', {'Type': kind, 'Path': path, 'Addressable': 'true'})
if icon_path:
    element(assets, 'Asset', {'Type': 'Microsoft.VisualStudio.Services.Icons.Default', 'Path': icon_asset_path, 'Addressable': 'true'})
content_ns = 'http://schemas.openxmlformats.org/package/2006/content-types'
content = ET.Element('Types', {'xmlns': content_ns})
for extension, mime in [('json', 'application/json'), ('svg', 'image/svg+xml'),
                        ('md', 'text/markdown'), ('png', 'image/png'), ('vsixmanifest', 'text/xml')]:
    ET.SubElement(content, 'Default', {'Extension': extension, 'ContentType': mime})
files = [ROOT / 'package.json', ROOT / 'README.md', ROOT / 'CHANGELOG.md']
if icon_path:
    files.append(icon_path)
files += sorted((ROOT / 'icons').rglob('*.svg'))
files += sorted((ROOT / 'themes').glob('*.json'))
output = ROOT / f"{pkg['name']}-{pkg['version']}.vsix"
with ZipFile(output, 'w', ZIP_DEFLATED) as archive:
    archive.writestr('extension.vsixmanifest', ET.tostring(manifest, encoding='utf-8', xml_declaration=True))
    archive.writestr('[Content_Types].xml', ET.tostring(content, encoding='utf-8', xml_declaration=True))
    for path in files:
        archive.write(path, 'extension/' + path.resolve().relative_to(ROOT.resolve()).as_posix())
with ZipFile(output) as archive:
    assert archive.testzip() is None
    ET.fromstring(archive.read('extension.vsixmanifest'))
    ET.fromstring(archive.read('[Content_Types].xml'))
    packed_pkg = json.loads(archive.read('extension/package.json'))
    if packed_pkg.get('icon'):
        assert archive.read(icon_asset_path) == icon_path.read_bytes()
        packed_manifest = ET.fromstring(archive.read('extension.vsixmanifest'))
        assert packed_manifest.find('{' + NS + '}Metadata/{' + NS + '}Icon').text == icon_asset_path
    for contribution in packed_pkg['contributes']['iconThemes']:
        theme_path = posixpath.normpath('extension/' + contribution['path'])
        theme = json.loads(archive.read(theme_path))
        for icon in theme['iconDefinitions'].values():
            path = posixpath.normpath(posixpath.join(posixpath.dirname(theme_path), icon['iconPath']))
            svg = ET.fromstring(archive.read(path))
            assert svg.attrib['viewBox'] == '0 0 24 24'
        for bindings in [theme, theme.get('light', {})]:
            for key in ['fileExtensions', 'fileNames']:
                assert all(value in theme['iconDefinitions'] for value in bindings.get(key, {}).values())
    print(f'{output}: {len(archive.namelist())} files; ZIP, manifests and all icon paths validated')
