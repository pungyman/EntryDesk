"""Render EntryDesk's three original vector diagrams; optionally export PNGs with CairoSVG."""
from html import escape
from pathlib import Path

HERE = Path(__file__).resolve().parent
INK, MUTED, LINE = '#202738', '#687182', '#a9b1bf'
PALETTES = {
    'green': ('#edf7ef', '#268354'),
    'purple': ('#f1edfc', '#7957bf'),
    'amber': ('#fff5e3', '#bb821c'),
    'blue': ('#edf3ff', '#4d76c8'),
    'neutral': ('#f5f7fb', '#758097'),
}


class Figure:
    def __init__(self, width, height, title, desc):
        self.width, self.height = width, height
        self.parts = [f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}" role="img" aria-labelledby="title desc">',
                      f'<title id="title">{escape(title)}</title><desc id="desc">{escape(desc)}</desc>',
                      f'<rect width="{width}" height="{height}" rx="28" fill="#ffffff"/>',
                      '<defs><marker id="arrow" markerWidth="9" markerHeight="9" refX="7.5" refY="4.5" orient="auto"><path d="M 1 1 L 7.5 4.5 L 1 8" fill="none" stroke="#a9b1bf" stroke-width="1.6"/></marker><marker id="purple-arrow" markerWidth="9" markerHeight="9" refX="7.5" refY="4.5" orient="auto"><path d="M 1 1 L 7.5 4.5 L 1 8" fill="none" stroke="#7957bf" stroke-width="1.6"/></marker></defs>']

    def text(self, x, y, value, size=24, color=INK, weight=400, anchor='start'):
        self.parts.append(f'<text x="{x}" y="{y}" fill="{color}" font-family="DejaVu Sans,Arial,sans-serif" font-size="{size}" font-weight="{weight}" text-anchor="{anchor}">{escape(value)}</text>')

    def box(self, x, y, w, h, palette='neutral', radius=22):
        fill, color = PALETTES[palette]
        self.parts.append(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{radius}" fill="{fill}" stroke="{color}" stroke-opacity=".35" stroke-width="1.8"/>')

    def line(self, path, purple=False, arrow=True, dashed=False):
        color = PALETTES['purple'][1] if purple else LINE
        marker = 'purple-arrow' if purple else 'arrow'
        self.parts.append(f'<path d="{path}" fill="none" stroke="{color}" stroke-width="2.7" stroke-linejoin="round" stroke-linecap="round"'+(f' marker-end="url(#{marker})"' if arrow else '')+(' stroke-dasharray="7 7"' if dashed else '')+'/>')

    def icon(self, x, y, kind, palette='purple', scale=1):
        color = PALETTES[palette][1]
        shapes = {
            'person': '<circle cx="24" cy="13" r="9"/><path d="M7 43v-6c0-9 8-14 17-14s17 5 17 14v6M18 25l6 8 6-8M24 33v10"/>',
            'market': '<path d="M5 40V9M5 40h39M11 31l10-12 9 5L43 9M35 9h8v8"/>',
            'calendar': '<rect x="5" y="8" width="38" height="35" rx="5"/><path d="M5 19h38M15 4v10M33 4v10M14 28h5M28 28h5M14 35h5"/>',
            'news': '<rect x="5" y="7" width="38" height="36" rx="4"/><path d="M13 15h22M13 23h9v11h-9zM28 23h7M28 30h7M13 38h22"/>',
            'quant': '<path d="M6 41h37M10 37V24h6v13M23 37V14h6v23M36 37V5h6v32"/>',
            'shield': '<path d="M24 4l17 7v13c0 10-8 17-17 22C15 41 7 34 7 24V11zM15 24l6 6 13-14"/>',
            'portfolio': '<rect x="4" y="12" width="40" height="31" rx="5"/><path d="M16 12V6h16v6M4 24h40M20 24v6h8v-6"/>',
            'model': '<rect x="4" y="5" width="13" height="10" rx="2"/><rect x="30" y="5" width="13" height="10" rx="2"/><rect x="17" y="33" width="13" height="10" rx="2"/><path d="M10 15v9h27v-9M24 24v9"/>',
            'wave': '<path d="M4 25c5-22 9-22 14 0s9 22 14 0 9-22 13-1M4 42h40"/>',
            'data': '<ellipse cx="24" cy="10" rx="18" ry="7"/><path d="M6 10v27c0 10 36 10 36 0V10M6 23c0 10 36 10 36 0"/>',
        }
        self.parts.append(f'<g transform="translate({x},{y}) scale({scale})" fill="none" stroke="{color}" stroke-width="2.8" stroke-linejoin="round" stroke-linecap="round">{shapes[kind]}</g>')

    def heading(self, eyebrow, title, subtitle):
        self.text(58, 52, eyebrow, 19, PALETTES['purple'][1], 650)
        self.text(58, 110, title, 44, INK, 650)
        self.text(58, 151, subtitle, 24, MUTED)

    def save(self, stem):
        svg = HERE / f'{stem}.svg'
        svg.write_text('\n'.join(self.parts + ['</svg>']) + '\n')
        try:
            import cairosvg
        except ImportError:
            print(f'Wrote {svg.name}; install cairosvg for PNG export.')
        else:
            cairosvg.svg2png(url=str(svg), write_to=str(HERE / f'{stem}.png'),
                            output_width=self.width * 3 // 2, output_height=self.height * 3 // 2)
            print(f'Wrote {stem}.svg and {stem}.png')


def overview():
    f = Figure(1600, 710, 'EntryDesk: four perspectives, one portfolio',
               'Four specialist analysts provide independent reports to a portfolio manager. The manager drafts a book. Deterministic risk and validation code supplies critique for one revision, then commits initial weights and cash. This overview omits fallback and exposure details, which are documented separately.')
    f.heading('ENTRYDESK  /  THE BIG PICTURE', 'Four perspectives. One portfolio.',
              'Independent evidence, agent judgment, deterministic commitment.')
    f.box(58, 207, 360, 360, 'green')
    f.text(83, 247, 'Analyst team', 29, PALETTES['green'][1], 650)
    for i, (icon, title, sub) in enumerate([
        ('market', 'Market', 'Regime + macro'), ('calendar', 'Earnings', 'Events + timing'),
        ('news', 'News', 'Company catalysts'), ('quant', 'Quant', 'Ranks + volatility')]):
        y = 277 + 68 * i
        f.icon(85, y, icon, 'green', .8)
        f.text(143, y + 18, title, 25, INK, 650)
        f.text(143, y + 45, sub, 21, MUTED)
    f.box(522, 292, 262, 237, 'purple')
    f.icon(628, 311, 'person', 'purple', 1.15)
    f.text(653, 411, 'Portfolio', 30, INK, 650, 'middle')
    f.text(653, 447, 'manager', 30, INK, 650, 'middle')
    f.text(653, 488, 'Weights + thesis', 22, MUTED, anchor='middle')
    f.box(884, 292, 290, 237, 'amber')
    f.icon(1001, 311, 'shield', 'amber', 1.15)
    f.text(1029, 411, 'Risk & validation', 28, INK, 650, 'middle')
    f.text(1029, 453, 'Measure the proposal', 22, MUTED, anchor='middle')
    f.text(1029, 488, 'Enforce constraints', 22, MUTED, anchor='middle')
    f.box(1274, 292, 268, 237, 'blue')
    f.icon(1380, 311, 'portfolio', 'blue', 1.15)
    f.text(1408, 411, 'Initial portfolio', 28, INK, 650, 'middle')
    f.text(1408, 453, 'Stock weights', 22, MUTED, anchor='middle')
    f.text(1408, 488, '+ cash', 22, MUTED, anchor='middle')
    f.line('M418 411 H507');f.text(468, 388, 'Reports', 19, MUTED, anchor='middle')
    f.line('M784 411 H869');f.text(834, 388, 'Draft', 19, MUTED, anchor='middle')
    f.line('M1174 411 H1259');f.text(1224, 388, 'Commit', 19, MUTED, anchor='middle')
    f.line('M1029 292 V232 H653 V277', purple=True)
    f.text(841, 217, 'Risk feedback · one revision', 22, PALETTES['purple'][1], anchor='middle')
    f.text(238, 615, 'Evidence in parallel', 23, PALETTES['green'][1], 650, 'middle')
    f.text(840, 615, 'A bounded decision loop', 23, PALETTES['purple'][1], 650, 'middle')
    f.text(1408, 615, 'Then hold', 23, PALETTES['blue'][1], 650, 'middle')
    f.save('entry-overview')
    f.save('entry-mechanism')  # Preserve existing external image links.


def review_loop():
    f = Figure(1600, 780, 'EntryDesk: from a draft to checked initial weights',
               'A portfolio-manager draft contains weights, thesis, and conditions. Code checks risk and feasibility against equal-exposure references. The same manager confirms or revises once. The final valid book passes through exposure sizing and precision-safe commitment. If no valid entry survives, a deterministic inverse-volatility fallback is used.')
    f.heading('ENTRYDESK  /  INSIDE THE ENTRY', 'A proposal earns its way into the portfolio.',
              'The manager gets a measured critique, then one chance to reconsider.')
    xs = [68, 602, 1136]
    for x, color in zip(xs, ['purple', 'amber', 'purple']):f.box(x, 259, 396, 270, color)
    f.icon(97, 287, 'person', 'purple');f.text(162, 319, 'Draft the book', 30, INK, 650)
    for i, label in enumerate(['Stock weights', 'Investment thesis', 'Plan conditions']):
        f.text(99, 389 + 42 * i, label, 25, MUTED)
    f.icon(631, 287, 'shield', 'amber');f.text(696, 319, 'Show the risks', 30, INK, 650)
    for i, label in enumerate(['Concentration + volatility', 'Beta + fees + constraints', 'Same-gross reference books']):
        f.text(632, 389 + 42 * i, label, 23, MUTED)
    f.icon(1165, 287, 'person', 'purple');f.text(1230, 319, 'Confirm or revise', 28, INK, 650)
    f.text(1167, 389, 'Same portfolio manager', 24, MUTED)
    f.text(1167, 433, 'One follow-up', 24, MUTED)
    f.text(1167, 477, 'A revision is checked again', 23, MUTED)
    f.line('M464 393 H587');f.text(533, 370, 'Proposal', 19, MUTED, anchor='middle')
    f.line('M998 393 H1121');f.text(1067, 370, 'Report', 19, MUTED, anchor='middle')
    f.line('M1334 259 V210 H266 V244', purple=True, dashed=True)
    f.text(800, 194, 'At most one revision', 23, PALETTES['purple'][1], anchor='middle')
    f.line('M1334 529 V574')
    f.box(1136, 592, 396, 110, 'blue')
    f.icon(1166, 621, 'portfolio', 'blue', .8)
    f.text(1221, 634, 'Validated weights + cash', 24, INK, 650)
    f.text(1221, 675, 'Exposure sizing stays in code', 21, MUTED)
    f.text(69, 626, 'If no valid entry survives', 23, INK, 650)
    f.text(69, 665, 'Use the inverse-volatility fallback.', 23, MUTED)
    f.text(800, 749, 'The draft, critique, revision and final weights stay in the decision record.', 23, MUTED, anchor='middle')
    f.save('entry-review')


def forecasting():
    f = Figure(1600, 700, 'EntryDesk: two forecasting lenses inform the quant analyst',
               'Point-in-time data feeds a daily cross-sectional return ensemble and HAR volatility forecasters in parallel. Purged walk-forward training produces ranks; daily, weekly, and monthly variance features produce one- and three-session volatility forecasts. These are evidence for the quant analyst, not autonomous trading orders.')
    f.heading('ENTRYDESK  /  THE FORECASTING LAYER', 'Two forecasts. Different questions.',
              'Which names look stronger? How much risk might they carry?')
    f.box(65, 307, 290, 190, 'neutral')
    f.icon(183, 329, 'data', 'neutral', 1.05)
    f.text(210, 421, 'Point-in-time data', 26, INK, 650, 'middle')
    f.text(210, 461, 'Available by the cutoff', 21, MUTED, anchor='middle')
    f.box(492, 216, 550, 180, 'blue')
    f.icon(521, 242, 'model', 'blue');f.text(591, 277, 'Daily return ensemble', 30, INK, 650)
    f.text(522, 327, 'Purged walk-forward training', 24, MUTED)
    f.text(522, 364, 'Output: cross-sectional ranks', 24, PALETTES['blue'][1], 650)
    f.box(492, 437, 550, 180, 'amber')
    f.icon(521, 463, 'wave', 'amber');f.text(591, 498, 'HAR volatility', 30, INK, 650)
    f.text(522, 548, 'Daily, weekly + monthly variance', 24, MUTED)
    f.text(522, 585, 'Output: 1- and 3-session forecasts', 24, PALETTES['amber'][1], 650)
    f.line('M355 402 H410 V306 H477')
    f.line('M410 402 V527 H477')
    f.box(1179, 307, 352, 190, 'green')
    f.icon(1329, 326, 'quant', 'green', 1.05)
    f.text(1355, 421, 'Quant analyst', 29, INK, 650, 'middle')
    f.text(1355, 461, 'Evidence for the entry', 23, MUTED, anchor='middle')
    f.line('M1042 306 H1100 V402 H1164');f.line('M1042 527 H1100 V402', arrow=False)
    f.text(800, 670, 'Forecasts inform the decision. The portfolio manager chooses the allocation.', 24, MUTED, anchor='middle')
    f.save('forecasting-stack')


if __name__ == '__main__':
    overview()
    review_loop()
    forecasting()
