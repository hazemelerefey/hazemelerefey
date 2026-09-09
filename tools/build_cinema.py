"""Build self-contained animated SVGs. Requires Pillow and fonttools.
Set CINEMA_FONT to a TrueType font if the default system font is unavailable.
Original generated key art is retained in assets/cinema/source/.
"""
from pathlib import Path
from io import BytesIO
import base64, html, math, os, random
from PIL import Image
from fontTools.ttLib import TTFont
from fontTools.pens.svgPathPen import SVGPathPen

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'assets/cinema'
FONT = TTFont(os.environ.get('CINEMA_FONT', '/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf'))
GLYPHS = FONT.getGlyphSet()
CMAP = FONT.getBestCmap()
EM = FONT['head'].unitsPerEm
INK, MUTED, RED, BASE = '#f3f0e8', '#aaa8ad', '#e50914', '#09090c'

def text(s,x,y,size=24,color=INK,spacing=0,bold=False):
    advance=0;result=[]
    for c in s:
        name=CMAP.get(ord(c),'.notdef');pen=SVGPathPen(GLYPHS);GLYPHS[name].draw(pen)
        if pen.getCommands():result.append(f'<path d="{pen.getCommands()}" transform="translate({x+advance:.2f} {y}) scale({size/EM:.6f} {-size/EM:.6f})"/>')
        advance+=GLYPHS[name].width*size/EM+spacing
    stroke=f' stroke="{color}" stroke-width="0.5"' if bold else ''
    return f'<g fill="{color}"{stroke} aria-label="{html.escape(s,quote=True)}">'+''.join(result)+'</g>'

CSS='''
@keyframes pulse{0%,100%{opacity:.25}50%{opacity:.9}}
@keyframes spin{to{transform:rotate(360deg)}}
@keyframes orbit{0%,100%{transform:translateY(0)}50%{transform:translateY(-13px)}}
@keyframes scan{0%{transform:translateY(-220px);opacity:0}12%{opacity:.85}85%{opacity:.7}100%{transform:translateY(300px);opacity:0}}
@keyframes dash{to{stroke-dashoffset:-600}}
@keyframes ember{0%{transform:translate(0,0);opacity:0}18%{opacity:.85}82%{opacity:.6}100%{transform:translate(20px,-140px);opacity:0}}
@keyframes reveal{0%{transform:scaleX(0)}100%{transform:scaleX(1)}}
@keyframes runner{0%{transform:translateX(-170px)}100%{transform:translateX(1250px)}}
@keyframes opening{0%,22%{opacity:1}100%{opacity:0;visibility:hidden}}
@keyframes ribbon{0%{transform:translateY(430px)}45%{transform:translateY(0)}100%{transform:translateY(-430px)}}
.pulse{animation:pulse 4s ease-in-out infinite}
.orbit{animation:orbit 8s ease-in-out infinite}
.spin{animation:spin 30s linear infinite;transform-box:fill-box;transform-origin:center}
.flow{stroke-dasharray:8 28;animation:dash 14s linear infinite}
.scan{animation:scan 7s ease-in-out infinite}
.ember{animation:ember 6s linear infinite}
@media(prefers-reduced-motion:reduce){*{animation:none!important}.scan,.ember,.runner{opacity:0!important}}
'''
DEFS='''
<linearGradient id="shade" x2="0" y2="1"><stop stop-color="#09090c" stop-opacity="0"/><stop offset="1" stop-color="#09090c"/></linearGradient>
<radialGradient id="aura"><stop stop-color="#e50914" stop-opacity=".48"/><stop offset="1" stop-color="#e50914" stop-opacity="0"/></radialGradient>
<radialGradient id="blue"><stop stop-color="#44bce4" stop-opacity=".42"/><stop offset="1" stop-color="#44bce4" stop-opacity="0"/></radialGradient>
<radialGradient id="violet"><stop stop-color="#8b55ed" stop-opacity=".45"/><stop offset="1" stop-color="#8b55ed" stop-opacity="0"/></radialGradient>
'''

def save(name,w,h,body,title):
    svg=f'<svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" width="{w}" height="{h}" viewBox="0 0 {w} {h}" role="img" aria-labelledby="title desc"><title id="title">{html.escape(title)}</title><desc id="desc">Original HAZEMFLIX artwork. Decorative animation respects reduced-motion preferences.</desc><defs>{DEFS}<clipPath id="bounds"><rect width="{w}" height="{h}" rx="8"/></clipPath></defs><style>{CSS}</style><g clip-path="url(#bounds)"><rect width="{w}" height="{h}" fill="{BASE}"/>{body}</g></svg>'
    (OUT/(name+'.svg')).write_text(svg)

def art(name,w,h):
    im=Image.open(OUT/'source'/f'{name}.png').convert('RGB');im.thumbnail((1800,1440))
    buf=BytesIO();im.save(buf,format='JPEG',quality=85,optimize=True)
    uri='data:image/jpeg;base64,'+base64.b64encode(buf.getvalue()).decode()
    return f'<image width="{w}" height="{h}" preserveAspectRatio="xMidYMid slice" xlink:href="{uri}"/>'

def line(x1,y1,x2,y2,color='#303037',width=1,extra=''):
    return f'<path d="M{x1} {y1}L{x2} {y2}" fill="none" stroke="{color}" stroke-width="{width}" {extra}/>'
def rect(x,y,w,h,fill,rx=0,extra=''):
    return f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{rx}" fill="{fill}" {extra}/>'
def circle(x,y,r,fill,extra=''):
    return f'<circle cx="{x}" cy="{y}" r="{r}" fill="{fill}" {extra}/>'
def embers(seed,area,color,count):
    rng=random.Random(seed);s='';x0,y0,x1,y1=area
    for i in range(count):
        x,y=rng.uniform(x0,x1),rng.uniform(y0,y1)
        s+=circle(round(x,1),round(y,1),round(rng.uniform(.6,1.6),1),color,f'class="ember" style="animation-delay:-{rng.uniform(0,8):.2f}s;animation-duration:{rng.uniform(5,10):.2f}s"')
    return s

def hero():
    s=art('hero',1200,400)+circle(850,184,190,'url(#aura)','class="pulse"')
    s+='<g opacity=".55">'+embers(8,(625,180,1140,395),'#ff755b',38)+'</g>'
    for rx,ry,rot in [(126,86,-26),(147,52,40),(111,100,-9)]:
        s+=f'<g transform="rotate({rot} 862 154)"><ellipse cx="862" cy="154" rx="{rx}" ry="{ry}" fill="none" stroke="#ff6b60" stroke-width="1.1" opacity=".55" class="flow"/></g>'
    s+=rect(0,397,1200,3,'#311014')+rect(0,397,170,3,RED,extra='class="runner" style="animation:runner 8s linear infinite"')
    # One opening ident; the readable hero remains the default static state.
    opening=rect(0,0,1200,400,BASE)
    for i in range(31):
        x=290+i*20
        opening+=rect(x,-20,3+(i%4)*2,440,['#65070e','#e50914','#ff253a','#8e1020'][i%4],extra=f'style="animation:ribbon 1.5s cubic-bezier(.22,.61,.36,1) both;animation-delay:{i*.011:.3f}s"')
    opening+=rect(324,150,550,100,BASE,8)+text('HAZEMFLIX',362,219,64,RED,2,bold=True)
    s+='<g opacity="0" style="animation:opening 1.8s ease-out both">'+opening+'</g>'
    save('hero',1200,400,s,'Hazem Elerefy · AI Engineer / Frontend Developer. Intelligence is the main character.')

def buttons():
    items=[('play','PLAY PORTFOLIO',INK,BASE),('catalog','BROWSE THE CATALOG','#202025',INK),('contact',"LET'S COLLABORATE",'#202025',INK)]
    for name,label,bg,fg in items:
        s=rect(0,0,390,68,bg,7)
        if name=='play':s+=f'<path d="M32 22L32 46L51 34Z" fill="{fg}"/>'
        elif name=='catalog':
            for x,y in [(29,22),(43,22),(29,36),(43,36)]:s+=rect(x,y,9,9,fg,1)
        else:s+=f'<path d="M28 24H54V44H28Z M28 24L41 35L54 24" fill="none" stroke="{fg}" stroke-width="2"/>'
        s+=text(label,72,41,18,fg,1,bold=True)
        save('button-'+name,390,68,s,label)

def section(name,number,title,right):
    s=rect(26,35,4,29,RED)+text(number,48,57,17,RED,2)+text(title,112,58,27,INK,bold=True)
    s+=text(right,864,56,12,MUTED,1)+line(26,85,1174,85,'#24242a')
    save(name,1200,99,s,title)

def posters():
    for name,color,title in [('dafesteel','#ff7044','DAFEsteel: computer vision for steel-surface inspection'),('neuroscope','#8edfff','NeuroScope: an interactive 3D deep-learning architecture workspace'),('signal','#ffc66d','SIGNAL: social intelligence and content agents built with n8n')]:
        s=art(name,400,600)
        if name=='dafesteel':
            s+='<g clip-path="url(#artzone)"><g class="scan">'+rect(35,225,330,44,'url(#shade)')+line(35,270,365,270,color,1.8)+line(35,267,365,267,'#fff1dd',.7)+'</g></g>'
            for x,y in [(174,140),(210,205),(239,317)]:s+=f'<path d="M{x-12} {y-5}v-7h8 M{x+12} {y+5}v7h-8" fill="none" stroke="{color}" stroke-width="1.2" class="pulse"/>'
        elif name=='neuroscope':
            for i in range(4):s+=f'<ellipse cx="200" cy="{138+i*61}" rx="{56+i*8}" ry="{12+i*2}" fill="none" stroke="{color}" stroke-width=".9" class="flow" opacity=".6"/>'
            for x,y in [(200,93),(169,168),(248,217),(200,281),(217,347)]:s+=circle(x,y,4,color,'class="pulse"')
        else:
            for x in [37,83,138,256,310,366]:s+=f'<path d="M{x} 403 Q{x} 307 197 238" stroke="{color}" stroke-width=".9" fill="none" class="flow" opacity=".75"/>'
        s+=embers(21,(40,110,360,445),color,15)
        s+=rect(0,595,400,5,'#25252b')+rect(0,595,155,5,color,extra='style="animation:reveal 5s ease-in-out infinite alternate;transform-origin:left"')
        s='<defs><clipPath id="artzone"><rect x="20" y="75" width="360" height="360"/></clipPath></defs>'+s
        save(name,400,600,s,title)

def nebula():
    s=circle(382,166,230,'url(#violet)')+circle(467,80,130,'url(#blue)');rng=random.Random(12)
    for i in range(105):s+=circle(rng.randint(15,580),rng.randint(15,300),rng.choice([.6,.8,1.2]),'#b9b4db',f'opacity="{rng.uniform(.2,.8):.2f}"')
    orbit=''
    for i in range(15):orbit+=f'<ellipse cx="406" cy="148" rx="{abs(103*math.cos(i*math.pi/15)):.2f}" ry="102" fill="none" stroke="#bd9dff" stroke-width=".7" opacity=".55"/>'
    for i in range(9):
        dy=(i-4)*21
        orbit+=f'<ellipse cx="406" cy="{148+dy}" rx="{math.sqrt(max(0,102**2-dy**2)):.2f}" ry="12" fill="none" stroke="#b996f4" stroke-width=".7" opacity=".45"/>'
    s+='<g class="orbit">'+orbit+'<ellipse cx="406" cy="148" rx="156" ry="41" transform="rotate(-23 406 148)" stroke="#79d8f0" fill="none" stroke-width="1.2" class="flow"/>'+circle(501,80,5,INK,'class="pulse"')+'</g>'
    s+=rect(0,190,590,170,'url(#shade)')+text('WEBGL / INTERACTIVE WORLDS',26,37,12,'#d3b9ff',1)
    s+=text('NEBULA',26,279,50,INK,1,bold=True)+text('Custom shaders. Particles. Play.',28,311,16,MUTED)
    s+=text('REACT  /  THREE.JS  /  GLSL',28,338,11,'#d3b9ff',1)
    save('nebula',590,360,s,'Nebula: interactive 3D portfolio with custom shaders, particle fields and a mini-game')

def jobpulse():
    s=circle(421,116,230,'url(#blue)')
    for x in range(26,590,41):s+=line(x,62,x,220,'#18232b')
    for y in range(65,224,31):s+=line(26,y,565,y,'#18232b')
    points=[(38,190),(78,181),(118,186),(158,154),(198,164),(238,120),(278,129),(318,94),(358,100),(398,56),(438,85),(478,64),(548,45)]
    path='M'+' L'.join(f'{x} {y}' for x,y in points)
    s+=f'<path d="{path} L548 223H38Z" fill="#36909d" opacity=".09"/><path d="{path}" stroke="#72e2cf" stroke-width="3" fill="none"/><path d="{path}" stroke="#eafffa" stroke-width="3.4" fill="none" class="flow"/>'
    s+=circle(398,56,7,'#8be8d9','class="pulse"')
    for x,y,w in [(68,78,90),(265,172,76),(427,118,103)]:s+=rect(x,y,w,32,'#10222a',5,extra='stroke="#28505a"')+line(x+10,y+16,x+w-10,y+16,'#77c4be',3)
    s+=rect(0,185,590,175,'url(#shade)')+text('DATA / PRODUCT INTERFACES',26,37,12,'#8be8d9',1)
    s+=text('JOBPULSE',26,279,50,INK,1,bold=True)+text('A clearer view of the job market.',28,311,16,MUTED)
    s+=text('NEXT.JS  /  TYPESCRIPT  /  RECHARTS',28,338,11,'#8be8d9',1)
    save('jobpulse',590,360,s,'JobPulse: market intelligence dashboard. Artwork is illustrative, not a screenshot.')

def stack():
    s=text('THE PRODUCTION KIT',28,46,25,INK,bold=True)+text('CAST BY WHAT I BUILD',876,43,12,MUTED,1)+line(28,68,1172,68,'#25252c')
    columns=[(28,'01','INTELLIGENCE',RED,['Python · PyTorch · YOLO','Scikit-learn · Pandas · SQL','n8n · AI agents · MCP']),(430,'02','EXPERIENCE','#91d8ec',['React · Next.js · TypeScript','Three.js · GLSL · GSAP','Tailwind CSS · Figma']),(832,'03','DELIVERY','#efc286',['FastAPI · Docker','PostgreSQL · REST APIs','Git · Power BI'])]
    for x,n,label,c,rows in columns:
        s+=text(n,x,108,15,c,1)+text(label,x+39,108,16,c,1,bold=True)
        for i,row in enumerate(rows):s+=text(row,x,154+i*35,17,INK)
    s+=line(405,92,405,238,'#25252c')+line(807,92,807,238,'#25252c')+line(28,269,1172,269,'#25252c')
    s+=f'<path d="M28 269H1172" stroke="{RED}" stroke-width="2" class="flow"/>'
    for x,label in [(28,'FRAME THE PROBLEM'),(430,'BUILD THE INTELLIGENCE'),(832,'MAKE IT USABLE')]:s+=text(label,x,302,12,MUTED,1)
    save('stack',1200,330,s,'Stack: AI and deep learning; frontend and interactive 3D; APIs, deployment and analytics')

def credits():
    s=circle(1040,110,300,'url(#aura)')+text('THE NEXT ORIGINAL',30,42,13,'#ff6169',2)
    s+=text('A great idea deserves',28,103,43,INK,bold=True)+text('a remarkable execution.',28,156,43,INK,bold=True)
    s+=text('AI SYSTEMS  /  IMMERSIVE FRONTENDS  /  THOUGHTFUL PRODUCTS',31,197,13,MUTED,1)
    s+=line(30,220,1170,220,'#3d2026')+text('HAZEM ELEREFY',30,251,15,INK,1)+text('CAIRO, EGYPT',940,251,13,MUTED,1)
    reel=circle(1040,114,48,'none','stroke="#ff4e5e" stroke-width="2"')
    for i in range(5):reel+=circle(round(1040+28*math.cos(i*math.tau/5),2),round(114+28*math.sin(i*math.tau/5),2),10,'#47141d','stroke="#b93d49"')
    s+='<g class="spin">'+reel+'</g>'
    save('credits',1200,274,s,'The next original: a great idea deserves a remarkable execution. Hazem Elerefy, Cairo, Egypt.')

def mobile():
    for name,label,bg,fg in [('play','PORTFOLIO',INK,BASE),('catalog','PROJECTS','#202025',INK),('contact','CONTACT','#202025',INK)]:
        s=rect(0,0,280,100,bg,8)+text(label,22,60,30,fg,1,bold=True)
        save('button-'+name+'-mobile',280,100,s,label)
    for name,n,title in [('ai','01','THE AI ORIGINALS'),('web','02','THE INTERFACE COLLECTION')]:
        s=rect(18,29,4,30,RED)+text(n,37,52,18,RED)+text(title,80,52,25,INK,bold=True)
        s+=line(18,76,582,76,'#24242a')
        save('section-'+name+'-mobile',600,92,s,title)
    s=text('THE PRODUCTION KIT',24,46,27,INK,bold=True)
    columns=[('INTELLIGENCE',RED,['Python · PyTorch · YOLO','Scikit-learn · Pandas · SQL','n8n · AI agents · MCP']),('EXPERIENCE','#91d8ec',['React · Next.js · TypeScript','Three.js · GLSL · GSAP','Tailwind CSS · Figma']),('DELIVERY','#efc286',['FastAPI · Docker','PostgreSQL · REST APIs','Git · Power BI'])]
    for i,(label,c,rows) in enumerate(columns):
        y=96+i*158
        s+=line(24,y-23,576,y-23,'#25252c')+text('0'+str(i+1),24,y+8,18,c)+text(label,65,y+8,20,c,1,bold=True)
        for j,row in enumerate(rows):s+=text(row,24,y+49+j*29,23,INK)
    s+=line(24,555,576,555,RED)+text('FRAME. BUILD. MAKE IT USABLE.',24,591,17,MUTED,1)
    save('stack-mobile',600,620,s,'The production kit: intelligence, experience and delivery')
    s=circle(567,64,240,'url(#aura)')+text('THE NEXT ORIGINAL',24,36,15,'#ff6169',2)
    for i,t in enumerate(['A great idea deserves','a remarkable','execution.']):s+=text(t,24,102+i*56,43,INK,bold=True)
    s+=line(24,250,576,250,'#3d2026')+text('HAZEM ELEREFY',24,282,18,INK,1)
    s+=text('AI SYSTEMS / IMMERSIVE FRONTENDS',24,317,17,MUTED)
    save('credits-mobile',600,344,s,'A great idea deserves a remarkable execution. Hazem Elerefy.')

if __name__=='__main__':
    OUT.mkdir(parents=True,exist_ok=True)
    hero();buttons();posters()
    section('section-ai','01','THE AI ORIGINALS','3 TITLES / SELECTED WORK')
    section('section-web','02','THE INTERFACE COLLECTION','2 TITLES / FRONTEND')
    nebula();jobpulse();stack();credits();mobile()
    for p in sorted(OUT.glob('*.svg')):print(p.name,round(p.stat().st_size/1024),'KiB')
