#!/usr/bin/env python3
"""Generate Mayhoa Phase 2 rice, corn and carrot sprites plus PixiJS atlas."""
import argparse, json, math, random
from pathlib import Path
from PIL import Image, ImageDraw

M,S,C=512,3,192
A=(256,350)
CROPS=("rice","corn","carrot")
STAGES=("stage-01_seeded","stage-02_sprout","stage-03_young","stage-04_mature","stage-05_harvestable")
K={"o":(62,80,43,235),"sh":(58,47,32,62),"d":(70,111,55,255),"g":(91,139,69,255),"l":(132,166,86,255),"s":(78,119,56,255),"gold":(203,166,78,255),"gl":(232,205,119,255),"or":(214,108,55,255),"ol":(239,144,76,255)}

def q(v): return int(round(v*S))
def P(p): return q(p[0]),q(p[1])
def curve(a,b,c,n=18):
    return [((1-t)**2*a[0]+2*(1-t)*t*b[0]+t*t*c[0],(1-t)**2*a[1]+2*(1-t)*t*b[1]+t*t*c[1]) for t in (i/n for i in range(n+1))]
def leaf(d,a,c,bend,w,fill):
    dx,dy=c[0]-a[0],c[1]-a[1]; z=max(1,math.hypot(dx,dy)); n=(-dy/z,dx/z)
    mid=((a[0]+c[0])/2+n[0]*bend,(a[1]+c[1])/2+n[1]*bend); ctr=curve(a,mid,c,20); L=[]; R=[]
    for i,(x,y) in enumerate(ctr):
        t=i/(len(ctr)-1); ww=w*math.sin(math.pi*min(.98,t))*(1-.25*t) if i<len(ctr)-1 else 0
        x2,y2=ctr[min(i+1,len(ctr)-1)] if i<len(ctr)-1 else ctr[i-1]; ddx,ddy=x2-x,y2-y; zz=max(1,math.hypot(ddx,ddy)); nn=(-ddy/zz,ddx/zz)
        L.append((x+nn[0]*ww,y+nn[1]*ww)); R.append((x-nn[0]*ww,y-nn[1]*ww))
    d.polygon([P(x) for x in L+R[::-1]],fill=fill,outline=K["o"],width=q(.8)); d.line([P(x) for x in ctr],fill=(94,126,67,180),width=q(.6),joint="curve")
def sh(d,w):
    x,y=A; d.ellipse((q(x-w/2),q(y-5),q(x+w/2),q(y+8)),fill=K["sh"])
def stem(d,a,b,w=2.2):
    d.line((P(a),P(b)),fill=K["o"],width=q(w+1)); d.line((P(a),P(b)),fill=K["s"],width=q(w))
def base(): return Image.new("RGBA",(M*S,M*S),(0,0,0,0))
def finish(im): return im.resize((M,M),Image.Resampling.LANCZOS)

def rice(st,r):
    im=base(); d=ImageDraw.Draw(im,"RGBA"); ns=(1,4,8,14,18); hs=(8,26,56,104,118); sh(d,(10,28,52,74,82)[st])
    for i in range(ns[st]):
        bx=A[0]+(i-(ns[st]-1)/2)*3.7+r.uniform(-2,2); by=A[1]+r.uniform(-2,2); h=hs[st]*r.uniform(.82,1.08); tip=(bx+r.uniform(-14,14),by-h)
        leaf(d,(bx,by),tip,r.uniform(-7,7),max(1.4,3.5-st*.25),K["g"] if i%3 else K["l"])
        if st==4 and i%2==0:
            end=(tip[0]+r.uniform(-10,10),tip[1]+r.uniform(10,23)); d.line((P(tip),P(end)),fill=K["gold"],width=q(1.2))
            for j in range(4):
                t=(j+1)/5; x=tip[0]+(end[0]-tip[0])*t; y=tip[1]+(end[1]-tip[1])*t; side=-1 if j%2 else 1
                d.ellipse((q(x+side*1.2-1.5),q(y-1.2),q(x+side*1.2+1.5),q(y+1.2)),fill=K["gl"],outline=K["o"],width=q(.35))
    return finish(im)

def corn(st,r):
    im=base(); d=ImageDraw.Draw(im,"RGBA"); hs=(10,42,82,126,140); ns=(1,3,6,9,10); sh(d,(10,28,45,60,66)[st]); x,y=A; top=(x+r.uniform(-1.5,1.5),y-hs[st]); stem(d,(x,y),top,2.2 if st<2 else 3)
    for i in range(ns[st]):
        t=(i+1)/(ns[st]+1); yy=y-hs[st]*t; side=-1 if i%2==0 else 1; ln=(16+st*8)*(.72+.28*math.sin(math.pi*t)); tip=(x+side*ln,yy-r.uniform(4,15))
        leaf(d,(x,yy+2),tip,side*r.uniform(2,8),5 if st>=2 else 3.2,K["l"] if i%3==0 else K["g"])
    if st>=3:
        for a in (-12,-6,0,6,12):
            e=(top[0]+a*.65,top[1]-18-r.uniform(0,8)); d.line((P((top[0],top[1]+3)),P(e)),fill=K["gold"],width=q(1.2)); d.ellipse((q(e[0]-1.2),q(e[1]-1.2),q(e[0]+1.2),q(e[1]+1.2)),fill=K["gl"])
    if st==4:
        for side,yy in ((-1,y-58),(1,y-76)):
            d.ellipse((q(x+side*5-5),q(yy-11),q(x+side*5+6),q(yy+13)),fill=K["gold"],outline=K["o"],width=q(1.1)); leaf(d,(x+side*2,yy+7),(x+side*30,yy+18),side*3,4,K["d"])
    return finish(im)

def carrot(st,r):
    im=base(); d=ImageDraw.Draw(im,"RGBA"); hs=(7,25,52,82,96); ns=(1,3,6,9,11); sh(d,(10,25,42,54,60)[st]); x,y=A
    if st>=3:
        rh=16 if st==3 else 28; rw=11 if st==3 else 17; poly=[(x-rw,y-6),(x+rw,y-6),(x+rw*.55,y+rh*.4),(x,y+rh),(x-rw*.55,y+rh*.4)]
        d.polygon([P(p) for p in poly],fill=K["or"] if st==3 else K["ol"],outline=K["o"],width=q(1.2)); d.line((P((x-4,y)),P((x+4,y+rh*.55))),fill=(242,164,93,180),width=q(1))
    for i in range(ns[st]):
        a=(x+r.uniform(-5,5),y-4); ang=r.uniform(-.42,.42); h=hs[st]*(.72+.34*r.random()); tip=(a[0]+math.sin(ang)*h,a[1]-math.cos(ang)*h); stem(d,a,tip,1 if st<2 else 1.4)
        if st>=2:
            for j in range(2+st):
                t=(j+1)/(3+st); px=a[0]+(tip[0]-a[0])*t; py=a[1]+(tip[1]-a[1])*t; side=-1 if (j+i)%2==0 else 1; ln=7+st*2
                leaf(d,(px,py),(px+side*ln,py-r.uniform(2,8)),side*2,1.7,K["l"] if j%3==0 else K["g"])
    return finish(im)

def save(im,p): p.parent.mkdir(parents=True,exist_ok=True); im.save(p,"PNG",optimize=True)
def main():
    ap=argparse.ArgumentParser(); ap.add_argument("--root",type=Path,default=Path(".")); root=ap.parse_args().root.resolve(); imgs={}; made=[]; draw={"rice":rice,"corn":corn,"carrot":carrot}
    for crop in CROPS:
        for i,stage in enumerate(STAGES):
            im=draw[crop](i,random.Random(f"mayhoa-phase2-{crop}-{i}")); p=root/"masters"/"farm"/"crops"/crop/f"{crop}_{stage}_v01.png"; save(im,p); made.append(p); imgs[crop,i]=im
    atlas=Image.new("RGBA",(C*5,C*3),(0,0,0,0)); frames={}
    for row,crop in enumerate(CROPS):
        for col,stage in enumerate(STAGES):
            atlas.alpha_composite(imgs[crop,col].resize((C,C),Image.Resampling.LANCZOS),(col*C,row*C)); frames[f"{crop}_{stage}"]={"x":col*C,"y":row*C,"w":C,"h":C,"anchor":{"x":.5,"y":.684}}
    p=root/"runtime"/"1x"/"farm"/"crops"/"core_crops_v01.png"; save(atlas,p); made.append(p)
    manifest={"format":"mayhoa-core-crops-atlas-v1","image":"1x/farm/crops/core_crops_v01.png","cellSize":{"w":C,"h":C},"masterCanvas":{"w":M,"h":M},"placementAnchor":{"x":.5,"y":.684},"crops":list(CROPS),"stageOrder":list(STAGES),"frames":frames}
    p=root/"runtime"/"core_crops_v01.json"; p.parent.mkdir(parents=True,exist_ok=True); p.write_text(json.dumps(manifest,indent=2)+"\n",encoding="utf-8"); made.append(p)
    if len(made)!=17: raise SystemExit("wrong file count")
    for p in made:
        if not p.exists() or not p.stat().st_size: raise SystemExit(f"missing {p}")
        if p.suffix==".png" and Image.open(p).convert("RGBA").getextrema()[3][0]!=0: raise SystemExit(f"no transparency {p}")
    print("generated and verified 17 Phase 2 files")
if __name__=="__main__": main()
