"""Semantic families and vector silhouettes for VIP File Icons."""
# Core VIP files have exclusive silhouettes with a shared V monogram.
GROUPS = [
    ('VIP · знак стека', 'vip-brand', '#8B5CF6', 'vip vih vpp vil vill prj'),
    ('VIP · объявления', 'interface', '#6366F1', 'vin obj inc'),
    ('VIP · значения', 'values', '#A855F7', 'var const fnc'),
    ('Проекты и сборка', 'project', '#D97706', 'vpr ver'),
    ('Словарь и данные', 'database', '#0891B2', 'lot gcd dic mem tbl sql'),
    ('Окна и меню', 'window', '#0284C7', 'dlg win mnu mnh tb'),
    ('Печатные формы', 'report', '#DB2777', 'frm pro frn fr3'),
    ('Сценарии и сервисы', 'terminal', '#16A34A', 'cmd bat sh service'),
    ('Python и зависимости', 'package', '#CA8A04', 'py whl'),
    ('Веб-интерфейс', 'web', '#EA580C', 'html css'),
    ('Конфигурация', 'config', '#64748B', 'json yml xml iml'),
    ('Документы и списки', 'document', '#475569', 'txt docx rtf lst'),
    ('Табличные отчеты', 'sheet', '#059669', 'slk ods ots xlsx xlsm xltx xltm'),
    ('Графические ресурсы', 'image', '#E11D48', 'bmc bmp ico jpg'),
    ('Архив исходников', 'archive', '#78716C', 'old'),
]
# V is drawn as geometry, without font dependencies. Decorations remain outside it.
BRAND_V = '<path d="m8 8 4 9 4-9" stroke-width="2.8"/>'
SHAPES = {
    'vip': '<path d="m5 5 7-3 7 3v10l-7 7-7-7V5Z"/>' + BRAND_V,
    'vih': '<path d="M6 3H3v18h3M18 3h3v18h-3"/>' + BRAND_V,
    'vpp': '<path d="m5 4-3 3 3 3m14 4 3 3-3 3M10 3h4M10 21h4"/>' + BRAND_V,
    'vil': '<path d="M3 6h3M18 6h3M3 18h3M18 18h3M3 6v12M21 6v12"/>' + BRAND_V,
    'vill': '<path d="M2 5h4M18 5h4M2 19h4M18 19h4M2 5v14M22 5v14M3 12h3M18 12h3"/>' + BRAND_V,
    'prj': '<path d="M3 5h7l2 2h9v14H3V5Z"/><path d="m8 10 4 8 4-8" stroke-width="2.8"/>',

    'code': '<path d="m8 7-5 5 5 5m8-10 5 5-5 5m-3-12-2 14"/>',
    'interface': '<rect x="3" y="3" width="7" height="7" rx="2"/><rect x="14" y="14" width="7" height="7" rx="2"/><path d="M10 6h7v8M6 10v7h8"/>',
    'values': '<path d="M9 3H6v7l-3 2 3 2v7h3m6-18h3v7l3 2-3 2v7h-3M11 9h2m-2 6h2"/>',
    'project': '<path d="m12 3 9 5-9 5-9-5 9-5Zm-9 9 9 5 9-5M3 16l9 5 9-5"/>',
    'database': '<ellipse cx="12" cy="5" rx="8" ry="3"/><path d="M4 5v14c0 4 16 4 16 0V5M4 12c0 4 16 4 16 0"/>',
    'window': '<rect x="3" y="4" width="18" height="16" rx="2"/><path d="M3 9h18M7 6.5h1m-1 6h4m-4 4h10"/>',
    'report': '<path d="M14 3H5v18h14V8l-5-5Zm0 0v5h5M8 17v-4m4 4v-7m4 7v-2"/>',
    'terminal': '<rect x="2" y="4" width="20" height="16" rx="3"/><path d="m6 9 4 3-4 3m7 0h5"/>',
    'package': '<path d="m12 3 9 5v9l-9 5-9-5V8l9-5Zm-9 5 9 5 9-5m-9 5v9M7.5 5.5l9 5v4"/>',
    'web': '<circle cx="12" cy="12" r="9"/><ellipse cx="12" cy="12" rx="4" ry="9"/><path d="M3 12h18"/>',
    'config': '<path d="M5 3v18M12 3v18M19 3v18"/><path d="M2 8h6m1 8h6m1-9h6" stroke-width="4"/>',
    'document': '<path d="M14 3H5v18h14V8l-5-5Zm0 0v5h5M8 12h8m-8 4h6"/>',
    'sheet': '<rect x="3" y="3" width="18" height="18" rx="2"/><path d="M3 9h18M3 15h18M9 3v18"/>',
    'image': '<rect x="3" y="3" width="18" height="18" rx="2"/><circle cx="8" cy="8" r="1.5"/><path d="m3 18 6-6 4 4 3-3 5 5"/>',
    'archive': '<rect x="3" y="3" width="18" height="5" rx="1"/><path d="M5 8v13h14V8m-10 5h6"/>',
    'file': '<path d="M14 3H5v18h14V8l-5-5Zm0 0v5h5"/>',
    'folder': '<path d="M3 6h7l2 3h9v11H3V6Z"/>',
    'folder-open': '<path d="M3 18V6h7l2 3h8v3M3 20l3-8h16l-3 8H3Z"/>',
    'git': '<path d="m12 2 10 10-10 10L2 12 12 2Zm-4 6 8 8M8 8h7"/><circle cx="8" cy="8" r="1"/><circle cx="16" cy="16" r="1"/>',
}

