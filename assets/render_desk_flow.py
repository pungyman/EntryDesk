"""Render the single portfolio overview. Mini charts are schematic, not results."""
from render_entry_mechanism import Figure, PALETTES, INK, MUTED


def draw():
    f = Figure(2000, 960, 'EntryDesk: specialist evidence to portfolio weights',
        'Market charts and macro indicators feed the market analyst; earnings calendars, past reactions and stock context feed the earnings analyst; company headlines and price moves feed the news analyst; model ranks, volatility forecasts and portfolio signals feed the quant analyst. Each supplies an independent report to the portfolio manager, which chooses stock weights. Code supplies a risk critique for one confirm-or-revise step and applies validation and exposure sizing. Charts and allocations are schematic; optional SEC filing text is omitted from the recorded contest entry.')

    def text(x,y,s,size=20,color=MUTED,weight=400,anchor='middle'):
        f.text(x,y,s,size,color,weight,anchor)

    def path(d,c,w=3,fill='none',extra=''):
        f.parts.append(f'<path d="{d}" stroke="{c}" stroke-width="{w}" fill="{fill}" stroke-linejoin="round" stroke-linecap="round" {extra}/>')

    def rect(x,y,w,h,fill,rx=6,stroke='none'):
        f.parts.append(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{rx}" fill="{fill}" stroke="{stroke}"/>')

    def circle(x,y,r,fill):
        f.parts.append(f'<circle cx="{x}" cy="{y}" r="{r}" fill="{fill}"/>')

    def chart(x,y,c,variant=0):
        for yy in [8,32,56]:path(f'M{x} {y+yy}h160','#e8ecf1',1)
        points = ([52,46,50,29,35,21,26,9,16,4] if variant==0 else
                  [38,28,40,20,30,15,26,13,20,9])
        d='M'+' L'.join(f'{x+i*17} {y+p}' for i,p in enumerate(points))
        path(d+f' L{x+153} {y+64} H{x} Z','none',0,c,extra='fill-opacity=".10"')
        path(d,c,3)

    def calendar(x,y,c):
        rect(x,y,112,80,'#ffffff',9,c)
        rect(x+1,y+1,110,22,c,8)
        for i in range(4):
            for j in range(2):
                xx,yy=x+19+i*25,y+40+j*24
                if (i,j)==(2,1): circle(xx,yy,10,c)
                else: circle(xx,yy,3,'#cbd1dc')
        path(f'M{x+25} {y-5}v12 M{x+85} {y-5}v12',c,4)

    def reactions(x,y,c):
        path(f'M{x} {y+38}h155','#d6dce6',1.4)
        for i,h in enumerate([24,-18,35,-13,20,-24]):
            rect(x+7+i*24,y+38-max(h,0),14,abs(h),c if h>0 else '#c2cad8',3)

    def news(x,y,c):
        for i in [2,1,0]:rect(x+i*8,y-i*6,136,80,'#ffffff',7,'#d4dbe6')
        rect(x+11,y+13,32,27,c+'25',4)
        path(f'M{x+18} {y+34}l7-9 7 4 5-9',c,2)
        for yy,ww in [(15,66),(27,75),(48,110),(60,93)]:
            rect(x+(53 if yy<40 else 11),y+yy,ww,4,c if yy==15 else '#d5dce7',2)

    def ranking(x,y,c):
        for i,w in enumerate([120,93,66,42]):
            text(x,y+14+i*19,str(i+1),15,c,650)
            rect(x+17,y+3+i*19,w,11,c,4)

    def volatility(x,y,c):
        path(f'M{x} {y+67}h150','#e1e6ef',1)
        path(f'M{x} {y+50}l12-8 12 6 12-22 12 11 12-29 12 24 12-13 12 20',c,3)
        path(f'M{x+108} {y+39}l14-12 14 7 14-10',c,3,extra='stroke-dasharray="4 5"')

    def signals(x,y,c):
        # A mean-reversion trace and two reference portfolio shapes.
        path(f'M{x} {y+20}h145','#d1d8e6',1,extra='stroke-dasharray="4 5"')
        path(f'M{x} {y+12}c15 0 15 40 32 29s20-40 37-27 22 24 37 12 24-16 39-6',c,2.6)
        for i,w in enumerate([34,28,44,22]):rect(x+i*38,y+65-w/2,25,w/2,c+'90',3)

    f.text(44,54,'ENTRYDESK',20,PALETTES['purple'][1],700)
    f.text(44,105,'Four analysts. One portfolio manager.',43,INK,650)
    text(428,148,'SPECIALIST EVIDENCE',16,MUTED,650)
    text(1040,148,'ANALYST AGENTS',16,MUTED,650)
    text(1660,148,'PORTFOLIO CONSTRUCTION',16,MUTED,650)

    rows=[(174,'green','Market','market', ['Market + regime','Macro + sectors','Volatility + correlation']),
          (350,'amber','Earnings','calendar',['Earnings calendar','Past earnings reactions','Stock returns + risk']),
          (526,'blue','News','news',['Company headlines','Event timing','Recent price move']),
          (702,'purple','Quant','quant',['Return-model ranks','HAR + realized volatility','OU + reference weights'])]
    for y,palette,name,icon,labels in rows:
        pale,c=PALETTES[palette]
        f.box(44,y,780,152,palette,20)
        # Three graphic inputs, each with only a short caption.
        for x in [304,564]:path(f'M{x} {y+24}v100',c+'25',1)
        for x,label in zip([174,434,694],labels):text(x,y+132,label,18,INK)
        if name=='Market':
            chart(94,y+24,c)
            for xx,label,h in [(361,'VIX',39),(417,'10Y',24),(473,'XLK',52)]:
                rect(xx,y+83-h,32,h,c+'80',4);text(xx+16,y+104,label,13,c,650)
            # A compact correlation matrix.
            for i in range(4):
                for j in range(4):
                    rect(625+i*25,y+20+j*20,21,16,c,3)
                    f.parts[-1]=f.parts[-1].replace('/>',f' opacity="{[.15,.3,.5,.8][abs(i-j)]}"/>')
            path(f'M{747} {y+32}v53 M{740} {y+39}l7-7 7 7',c,2.4)
        elif name=='Earnings':
            calendar(118,y+19,c);reactions(358,y+24,c);chart(617,y+26,c,1)
        elif name=='News':
            news(101,y+23,c)
            path(f'M366 {y+66}h140',c+'80',2)
            for xx,rr in [(378,5),(417,8),(447,5),(491,6)]:circle(xx,y+66,rr,c)
            text(434,y+40,'72h',19,c,650)
            path(f'M491 {y+85}v-39',c,1.5)
            chart(617,y+27,c,1)
        else:
            ranking(103,y+20,c);volatility(359,y+23,c);signals(618,y+21,c)

        f.line(f'M824 {y+76} H894')
        f.box(912,y+9,256,134,palette,18)
        # Human agent with a small specialist badge.
        f.icon(935,y+36,'person',palette,1.1)
        circle(984,y+83,15,'#ffffff');f.icon(973,y+71,icon,palette,.46)
        text(1073,y+64,name,26,c,650)
        text(1073,y+94,'analyst',20,INK)

        # A visible report artifact on each independent connection.
        f.line(f'M1168 {y+76} H1211',arrow=False)
        rect(1213,y+54,31,43,'#ffffff',4,c)
        for yy,ww in [(65,16),(74,16),(83,11)]:path(f'M1220 {y+yy}h{ww}',c,1.6)
        f.line(f'M1245 {y+76} H1280',arrow=False)

    # All four independent reports meet at one decision-maker.
    f.line('M1280 250 V778',arrow=False)
    f.line('M1280 514 H1340')
    text(1280,209,'Reports',18,MUTED)

    f.box(1358,363,260,301,'purple',24)
    f.icon(1446,389,'person','purple',1.8)
    text(1488,518,'Portfolio',30,INK,650)
    text(1488,555,'manager',30,INK,650)
    text(1488,607,'Chooses stock weights',20,PALETTES['purple'][1],550)

    f.line('M1618 514 H1712',purple=True)
    text(1666,489,'Weights',17,PALETTES['purple'][1])
    f.box(1730,363,226,301,'blue',24)
    text(1843,408,'Allocation',27,INK,650)
    # A schematic weight vector avoids inventing an official allocation.
    for i,(name,w) in enumerate([('A',115),('B',86),('C',66),('…',39)]):
        yy=441+i*40
        text(1756,yy+15,name,17,MUTED,550)
        rect(1775,yy,151,21,'#dde7fb',5)
        rect(1775,yy,w,21,PALETTES['blue'][1],5)
    text(1843,636,'Relative stock weights',17,MUTED)

    # Keep the implemented bounded review subordinate to the main story.
    f.box(1360,736,596,119,'neutral',18)
    f.icon(1380,758,'shield','neutral',1.1)
    text(1461,774,'Code checks risk',22,INK,650,'start')
    text(1461,806,'Confirm or revise once',19,MUTED,400,'start')
    f.line('M1430 664 V721')
    f.line('M1547 736 V679',purple=True)
    f.line('M1843 664 V721')
    text(1843,776,'Validate + size',21,INK,650)
    text(1843,807,'Initial weights + cash',18,MUTED)
    path('M1731 758v72','#d5dce7',1)

    text(44,903,'Point-in-time inputs · independent reports · one bounded decision',20,MUTED,400,'start')
    text(44,936,'Schematic charts and allocation. Shared clock/book context omitted; SEC filing text excluded in the recorded entry.',16,MUTED,400,'start')
    f.save('entry-desk-flow')


if __name__ == '__main__':
    draw()
