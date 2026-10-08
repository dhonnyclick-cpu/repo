"""Generate simple SVG product images for seed data."""
from pathlib import Path

OUT = Path(__file__).parent / 'static' / 'img' / 'products'
OUT.mkdir(parents=True, exist_ok=True)

def svg(name, body, bg='#f1f5f9'):
    return f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 300 300">
<rect width="300" height="300" rx="16" fill="{bg}"/>
{body}
</svg>'''

IMAGES = {
    'laptop.svg': '''
<rect x="60" y="80" width="180" height="110" rx="8" fill="#1e293b"/>
<rect x="70" y="90" width="160" height="90" rx="4" fill="#38bdf8"/>
<rect x="85" y="105" width="70" height="8" rx="4" fill="#e0f2fe"/>
<rect x="85" y="120" width="110" height="6" rx="3" fill="#bae6fd"/>
<rect x="85" y="133" width="90" height="6" rx="3" fill="#bae6fd"/>
<rect x="45" y="195" width="210" height="14" rx="7" fill="#334155"/>
<rect x="130" y="199" width="40" height="6" rx="3" fill="#64748b"/>''',

    'monitor.svg': '''
<rect x="45" y="55" width="210" height="135" rx="10" fill="#1e293b"/>
<rect x="55" y="65" width="190" height="115" rx="4" fill="#0ea5e9"/>
<rect x="70" y="80" width="80" height="10" rx="5" fill="#e0f2fe"/>
<rect x="70" y="98" width="140" height="7" rx="3.5" fill="#bae6fd"/>
<rect x="70" y="113" width="120" height="7" rx="3.5" fill="#bae6fd"/>
<rect x="130" y="190" width="40" height="30" fill="#334155"/>
<rect x="105" y="220" width="90" height="12" rx="6" fill="#475569"/>''',

    'keyboard.svg': '''
<rect x="40" y="110" width="220" height="80" rx="10" fill="#1e293b"/>
<g fill="#475569">
<rect x="52" y="122" width="24" height="18" rx="3"/><rect x="82" y="122" width="24" height="18" rx="3"/><rect x="112" y="122" width="24" height="18" rx="3"/><rect x="142" y="122" width="24" height="18" rx="3"/><rect x="172" y="122" width="24" height="18" rx="3"/><rect x="202" y="122" width="24" height="18" rx="3"/><rect x="232" y="122" width="16" height="18" rx="3"/>
<rect x="52" y="146" width="24" height="18" rx="3"/><rect x="82" y="146" width="24" height="18" rx="3"/><rect x="112" y="146" width="24" height="18" rx="3"/><rect x="142" y="146" width="24" height="18" rx="3"/><rect x="172" y="146" width="24" height="18" rx="3"/><rect x="202" y="146" width="46" height="18" rx="3"/>
<rect x="52" y="170" width="36" height="12" rx="3"/><rect x="94" y="170" width="104" height="12" rx="3"/><rect x="204" y="170" width="44" height="12" rx="3"/>
</g>
<rect x="52" y="122" width="24" height="18" rx="3" fill="#0ea5e9"/>
<rect x="82" y="146" width="24" height="18" rx="3" fill="#8b5cf6"/>''',

    'paper.svg': '''
<rect x="75" y="60" width="150" height="185" rx="6" fill="#ffffff" stroke="#cbd5e1" stroke-width="3"/>
<g stroke="#94a3b8" stroke-width="4" stroke-linecap="round">
<line x1="95" y1="90" x2="205" y2="90"/><line x1="95" y1="112" x2="205" y2="112"/><line x1="95" y1="134" x2="185" y2="134"/><line x1="95" y1="156" x2="205" y2="156"/><line x1="95" y1="178" x2="170" y2="178"/><line x1="95" y1="200" x2="195" y2="200"/>
</g>
<rect x="85" y="45" width="130" height="30" rx="5" fill="#2a78d6"/>
<text x="150" y="66" font-family="sans-serif" font-size="16" fill="#fff" text-anchor="middle">A4</text>''',

    'pen.svg': '''
<g transform="rotate(35 150 150)">
<rect x="140" y="45" width="20" height="170" rx="4" fill="#0f172a"/>
<rect x="140" y="45" width="20" height="45" rx="4" fill="#2a78d6"/>
<rect x="143" y="45" width="6" height="170" fill="#334155"/>
<polygon points="140,215 160,215 150,250" fill="#cbd5e1"/>
<polygon points="146,235 154,235 150,250" fill="#0f172a"/>
</g>''',

    'coffee.svg': '''
<path d="M95 100 h90 v70 a45 45 0 0 1 -90 0 z" fill="#78350f"/>
<path d="M185 115 a30 30 0 0 1 0 55" fill="none" stroke="#92400e" stroke-width="12"/>
<ellipse cx="140" cy="100" rx="45" ry="12" fill="#451a03"/>
<ellipse cx="140" cy="100" rx="35" ry="8" fill="#92400e"/>
<path d="M118 60 q8 -14 0 -28 M140 55 q8 -14 0 -28 M162 60 q8 -14 0 -28" fill="none" stroke="#a8a29e" stroke-width="5" stroke-linecap="round"/>
<rect x="85" y="215" width="110" height="12" rx="6" fill="#e7e5e4"/>''',

    'water.svg': '''
<rect x="100" y="70" width="100" height="160" rx="14" fill="#bae6fd" opacity="0.9"/>
<rect x="125" y="50" width="50" height="26" rx="6" fill="#0284c7"/>
<rect x="128" y="44" width="44" height="14" rx="4" fill="#0369a1"/>
<rect x="112" y="110" width="76" height="60" rx="6" fill="#ffffff" opacity="0.85"/>
<path d="M150 122 c-10 14 -16 22 -16 30 a16 16 0 0 0 32 0 c0 -8 -6 -16 -16 -30z" fill="#0ea5e9"/>
<rect x="110" y="80" width="14" height="130" rx="7" fill="#ffffff" opacity="0.5"/>''',

    'printer.svg': '''
<rect x="55" y="120" width="190" height="75" rx="10" fill="#1e293b"/>
<rect x="70" y="135" width="160" height="34" rx="5" fill="#475569"/>
<rect x="95" y="85" width="110" height="55" rx="5" fill="#ffffff" stroke="#cbd5e1" stroke-width="2"/>
<g stroke="#94a3b8" stroke-width="3" stroke-linecap="round"><line x1="110" y1="100" x2="190" y2="100"/><line x1="110" y1="112" x2="190" y2="112"/><line x1="110" y1="124" x2="165" y2="124"/></g>
<rect x="70" y="185" width="160" height="30" rx="5" fill="#334155"/>
<circle cx="215" cy="160" r="6" fill="#22c55e"/>
<rect x="55" y="215" width="190" height="12" rx="6" fill="#0f172a"/>''',

    'ink.svg': '''
<rect x="105" y="95" width="90" height="120" rx="10" fill="#0f172a"/>
<rect x="125" y="65" width="50" height="35" rx="6" fill="#334155"/>
<rect x="132" y="55" width="36" height="14" rx="4" fill="#475569"/>
<rect x="115" y="125" width="70" height="55" rx="5" fill="#1e40af"/>
<text x="150" y="150" font-family="sans-serif" font-size="13" fill="#fff" text-anchor="middle">BLACK</text>
<text x="150" y="168" font-family="sans-serif" font-size="11" fill="#93c5fd" text-anchor="middle">100ml</text>''',

    'marker.svg': '''
<g transform="rotate(20 150 150)">
<rect x="135" y="60" width="30" height="140" rx="6" fill="#0f172a"/>
<rect x="135" y="60" width="30" height="35" rx="6" fill="#2a78d6"/>
<rect x="140" y="95" width="8" height="95" fill="#1e293b"/>
<polygon points="135,200 165,200 158,235 142,235" fill="#475569"/>
<rect x="142" y="235" width="16" height="14" rx="3" fill="#1e293b"/>
</g>
<circle cx="235" cy="90" r="18" fill="#0ea5e9" opacity="0.6"/>''',
}

for fname, body in IMAGES.items():
    (OUT / fname).write_text(svg(fname, body), encoding='utf-8')
    print('wrote', fname)
