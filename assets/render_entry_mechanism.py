"""Regenerate the entry mechanism diagram (standard library; optional cairosvg for PNG)."""
from pathlib import Path
from html import escape

HERE = Path(__file__).resolve().parent
W,H=1600,1250
INK='#eef4ff'; MUTED='#a9bad1'; CYAN='#65d9ed'; PURPLE='#bba8ff'; GREEN='#82e2b9'; BG='#0c1425'; PANEL='#142138'; LINE='#344965'
parts=[f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" role="img" aria-labelledby="title desc">',
'<title id="title">From evidence to initial portfolio weights: the Desk v3 entry mechanism</title>',
'<desc id="desc">Point-in-time data feeds four independent analysts. A portfolio manager drafts weights, a thesis, and conditions. Code validates and quantifies risk against same-gross baselines; the manager confirms or revises once. Code validates the final book, applies a configured exposure overlay, and records precision-safe target weights and cash. If no valid entry survives, a deterministic inverse-volatility fallback is used. The implemented contest entry then holds the book.</desc>',
f'<rect width="{W}" height="{H}" rx="28" fill="{BG}"/>',
'<defs><marker id="arrow" markerWidth="10" markerHeight="10" refX="8" refY="5" orient="auto"><path d="M 1 1 L 8 5 L 1 9" fill="none" stroke="#65d9ed" stroke-width="1.5"/></marker><marker id="loop" markerWidth="10" markerHeight="10" refX="8" refY="5" orient="auto"><path d="M 1 1 L 8 5 L 1 9" fill="none" stroke="#bba8ff" stroke-width="1.5"/></marker></defs>']
def text(x,y,s,size=25,color=INK,weight=400,anchor='start'):
 parts.append(f'<text x="{x}" y="{y}" fill="{color}" font-family="DejaVu Sans,Arial,sans-serif" font-size="{size}" font-weight="{weight}" text-anchor="{anchor}">{escape(s)}</text>')
def path(d,color=CYAN,marker=True,dashed=False):
 parts.append(f'<path d="{d}" fill="none" stroke="{color}" stroke-width="2.5"'+(' marker-end="url(#'+('loop' if color==PURPLE else 'arrow')+')"' if marker else '')+(' stroke-dasharray="7 7"' if dashed else '')+'/>')
def card(x,y,w,h,title,lines,accent=CYAN):
 parts.append(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="16" fill="{PANEL}"/>')
 parts.append(f'<rect x="{x}" y="{y+20}" width="4" height="{h-40}" rx="2" fill="{accent}"/>')
 text(x+23,y+36,title,26,INK,650)
 for i,line in enumerate(lines):text(x+23,y+70+i*29,line,22,MUTED)
def label(y,num,title,detail=''):
 text(72,y,num,22,CYAN,650);text(119,y,title,27,INK,650)
 if detail:text(1525,y,detail,21,MUTED,anchor='end')
text(72,68,'ICAIF 2026  /  AGENTIC PORTFOLIO CONSTRUCTION',20,CYAN,650)
text(72,130,'A portfolio is decided before it is traded.',48,INK,650)
text(72,179,'Separate evidence. Make a proposal. Measure its risks. Commit only what passes.',25,MUTED)
path('M 72 211 H 1528',LINE,False)
label(248,'01','Freeze the evidence','Every input is cut at the decision deadline')
sources=[('Market context',['Regime, macro,','returns and correlations']),('Daily ensemble',['Purged walk-forward','cross-sectional ranks']),('HAR volatility',['1- and 3-session','variance forecasts']),('Events + news',['Earnings timing,','eligible headlines']),('Universe context',['Broader stock ranking;','30 tradable names'])]
for i,(title,lines) in enumerate(sources):
 x=72+i*295;card(x,270,277,116,title,lines)
 path(f'M {x+138} 386 V 408',LINE,False)
path('M 210 408 H 1390',LINE,False)
roles=[('Market analyst','Macro + market structure'),('Earnings analyst','Event timing + reactions'),('News analyst','Company-specific catalysts'),('Quant analyst','Ranks + risk + context')]
for i,(title,desc) in enumerate(roles):
 x=72+i*374;path(f'M {x+166} 408 V 434');card(x,438,333,92,title,[desc],PURPLE)
 path(f'M {x+166} 530 V 554',LINE,False)
path('M 238 554 H 1360',LINE,False)
text(1525,587,'Four independent reports; PM sees a compact market table',20,MUTED,anchor='end')
label(618,'02','Deliberate with a bounded critique')
path('M 800 554 V 638 H 272 V 650')
card(72,654,402,152,'PM drafts the book',['Weights + investment thesis','Machine-checkable conditions'],PURPLE)
path('M 474 730 H 528')
card(544,654,500,152,'Code turns the draft into numbers',['Validation + risk / concentration / fees','Inverse-vol + risk-parity at same gross'],GREEN)
path('M 1044 730 H 1096')
card(1112,654,416,152,'PM confirms or revises',['One follow-up; no open-ended loop','A revision is validated again'],PURPLE)
path('M 1300 806 V 844 H 272 V 808',PURPLE,True,True)
parts.append(f'<rect x="500" y="828" width="510" height="34" rx="12" fill="{BG}"/>')
text(755,852,'One chance to revise. Every version is recorded.',20,PURPLE,anchor='middle')
label(914,'03','Commit through deterministic code')
card(72,940,438,143,'Final validity gate',['Known names · long-only · caps','Gross rule + evaluable conditions'],GREEN)
path('M 510 1008 H 552')
card(568,940,389,143,'Separate the exposure dial',['Scale the valid equity mix','to the configured invested share'],CYAN)
path('M 957 1008 H 998')
card(1014,940,514,143,'Initial weights + cash',['Precision-safe targets + audit trail','Then hold: the implemented entry stage'],GREEN)
path('M 1317 806 V 883 H 48 V 1008 H 68')
text(72,1130,'NO VALID ENTRY?',20,PURPLE,650)
text(290,1130,'Deterministic inverse-vol fallback at the configured exposure.',23,INK)
text(72,1186,'REUSABLE PATTERN',19,CYAN,650)
text(326,1186,'Specialists propose evidence; the agent decides; code owns constraints and commitment.',22,MUTED)
parts.append('</svg>')
(HERE/'entry-mechanism.svg').write_text('\n'.join(parts)+'\n')
if __name__=='__main__':
 try:import cairosvg
 except ImportError:print('SVG written. Install cairosvg to also regenerate the PNG.')
 else:
  cairosvg.svg2png(url=str(HERE/'entry-mechanism.svg'),write_to=str(HERE/'entry-mechanism.png'),output_width=1920,output_height=1500)
  print('Wrote entry-mechanism.svg and entry-mechanism.png')
