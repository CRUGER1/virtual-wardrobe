import sys
from PIL import Image, ImageDraw, ImageFont
OUT=sys.argv[1]
F="/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"; FB="/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
f=lambda s,b=False: ImageFont.truetype(FB if b else F,s)
INK=(40,40,40); RED=(200,30,30); COAT=(196,110,40); STEEL=(90,95,105)

def arrow(d,p0,p1,col=INK,w=3):
    d.line([p0,p1],fill=col,width=w)
    import math
    a=math.atan2(p1[1]-p0[1],p1[0]-p0[0]); L=16
    for s in (2.6,-2.6):
        d.line([p1,(p1[0]-L*math.cos(a+s*0.17),p1[1]-L*math.sin(a+s*0.17))],fill=col,width=w)
def dim_h(d,x0,x1,y,txt,fs=26):
    d.line([(x0,y),(x1,y)],fill=INK,width=2)
    for x in (x0,x1): d.line([(x,y-12),(x,y+12)],fill=INK,width=2)
    tw=d.textlength(txt,font=f(fs)); d.text(((x0+x1-tw)/2,y+8),txt,font=f(fs),fill=INK)
def dim_v(d,x,y0,y1,txt,fs=24):
    d.line([(x,y0),(x,y1)],fill=INK,width=2)
    for y in (y0,y1): d.line([(x-10,y),(x+10,y)],fill=INK,width=2)
    d.text((x+12,(y0+y1)/2-14),txt,font=f(fs),fill=INK)

# ---------- HOOK ----------
im=Image.new("RGB",(1600,1050),"white"); d=ImageDraw.Draw(im)
d.text((40,25),"HOOK (side view)  -  ILLUSTRATION ONLY, not to scale",font=f(38,True),fill=INK)
cm=45; xL=600; door_w=3.5*cm; xR=xL+door_w; top=330
d.rectangle([xL-140,170,xR+260,top-40],fill=(205,190,170),outline=INK,width=2)
d.text((xL-130,180),"door frame (top)",font=f(24),fill=INK)
d.rectangle([xL,top,xR,800],fill=(235,235,235),outline=INK,width=2)
d.text((xL+30,730),"DOOR",font=f(30,True),fill=(120,120,120))
t=9; open_w=4.5*cm; xB=xL+open_w
d.rectangle([xL-t,top-t,xB+t,top],fill=STEEL)                 # top bridge
d.rectangle([xL-t,top,xL,top+5*cm],fill=STEEL)                # front leg
d.rectangle([xB,top,xB+t,top+9*cm],fill=STEEL)                # back leg
yb=top+9*cm; d.arc([xB-10,yb-60,xB+110,yb+60],0,180,fill=STEEL,width=t)
d.rectangle([xB+100-t//2,yb-110,xB+100+t//2,yb],fill=STEEL)    # J tip
d.line([(xB,top+1.6*cm),(xR+2,top+3.3*cm),(xB-5,top+5.2*cm)],fill=STEEL,width=7)  # spring leaf
c0=top+2*cm
d.rectangle([xL,c0,xL+7,top+5*cm],fill=COAT)
d.rectangle([xB-7,c0,xB,top+9*cm],fill=COAT)
d.line([(xR+2,top+3.0*cm),(xR+2,top+3.6*cm)],fill=COAT,width=9)
d.ellipse([xB+40,yb-20,xB+160,yb+80],outline=(150,150,150),width=6)
d.text((xB+170,yb+10),"organizer loop",font=f(24),fill=INK)
# labels
d.text((930,95),"1) TOP PART: bare steel,",font=f(28,True),fill=INK)
d.text((930,130),"max 2 mm thick (incl. coating)",font=f(28,True),fill=INK)
arrow(d,(925,150),(xB-30,top-6))
d.text((1030,215),"gap above the door is only about 3 mm",font=f(24),fill=INK)
d.text((40,430),"2) PVC / rubber coating",font=f(28,True),fill=COAT)
d.text((40,465),"ONLY on the inner side",font=f(28,True),fill=COAT)
d.text((40,500),"of the legs, starting",font=f(28,True),fill=COAT)
d.text((40,535),"~2 cm below the top bend",font=f(28,True),fill=COAT)
arrow(d,(465,548),(xL+3,top+3.8*cm),COAT)
dim_v(d,xL-60,top,c0,"2 cm")
d.text((1000,430),"3) SPRING CLIP (MUST):",font=f(28,True),fill=RED)
d.text((1000,465),"presses the hook to the door.",font=f(26),fill=INK)
d.text((1000,500),"Hook sits tight on doors",font=f(26),fill=INK)
d.text((1000,535),"3.5 cm AND 4.4 cm thick:",font=f(26),fill=INK)
d.text((1000,570),"no side-to-side movement,",font=f(26),fill=INK)
d.text((1000,605),"no lifting at the top.",font=f(26),fill=INK)
arrow(d,(995,490),(xR+14,top+3.3*cm),RED)
dim_h(d,xL,xR,840,"door 3.5 - 4.4 cm")
dim_h(d,xL,xB,910,"hook inner opening >= 4.5 cm")
d.text((40,995),"3 hooks, all the same shape.  All 3 hanging loops the same length.",font=f(28,True),fill=INK)
im.save(OUT+"/illustration_hook_spring_coating.png")

# ---------- FRONT WINDOW ----------
im=Image.new("RGB",(1500,1050),"white"); d=ImageDraw.Draw(im)
d.text((40,25),"SHELF FRONT  -  ILLUSTRATION ONLY, not to scale",font=f(38,True),fill=INK)
d.text((40,90),"YES, we want this:",font=f(32,True),fill=(20,120,40))
s=26; X0,Y0=220,200; W,H=38*s,13*s
FAB=(220,207,191); MESH=(236,229,218); MESHL=(190,175,155)
d.rectangle([X0,Y0,X0+W,Y0+H],fill=FAB,outline=INK,width=3)
d.rectangle([X0,Y0,X0+W,Y0+0.8*s],fill=(200,186,168))
wx0,wy0,wx1,wy1=X0+3*s,Y0+2.5*s,X0+W-3*s,Y0+H-2*s
d.rectangle([wx0,wy0,wx1,wy1],fill=MESH,outline=MESHL,width=2)
for x in range(int(wx0)+6,int(wx1),9):
    for y in range(int(wy0)+6,int(wy1),9): d.ellipse([x-2,y-2,x+2,y+2],fill=MESHL)
d.text((X0+W+15,Y0-8),"fiberglass rod",font=f(22),fill=INK); d.text((X0+W+15,Y0+18),"in top edge",font=f(22),fill=INK)
d.text((wx0+40,(wy0+wy1)/2-36),"MESH WINDOW in the CENTER",font=f(32,True),fill=INK)
d.text((wx0+40,(wy0+wy1)/2+8),"mesh colour = fabric colour (beige)",font=f(26),fill=INK)
dim_h(d,X0,wx0,Y0+H+30,"~3 cm",22); dim_h(d,wx1,X0+W,Y0+H+30,"~3 cm",22)
dim_v(d,X0-70,Y0,wy0,"~2.5 cm",22); dim_v(d,X0-70,wy1,Y0+H,"~2 cm",22)
d.text((X0,Y0+H+75),"Fabric border on ALL 4 sides. Front width 38 cm.",font=f(26,True),fill=INK)
d.text((X0,Y0+H+112),"Same style on all 6 shelves (front heights 10 / 10 / 13 / 13 / 17 / 17 cm).",font=f(26),fill=INK)
d.text((40,720),"NOT this:",font=f(32,True),fill=RED)
s2=14; X1,Y1=220,790; W2,H2=38*s2,13*s2
d.rectangle([X1,Y1,X1+W2,Y1+H2],fill=FAB,outline=INK,width=3)
my=Y1+H2*0.55; d.rectangle([X1,my,X1+W2,Y1+H2],fill=MESH,outline=MESHL,width=2)
for x in range(X1+6,X1+W2,9):
    for y in range(int(my)+6,Y1+H2,9): d.ellipse([x-2,y-2,x+2,y+2],fill=MESHL)
d.line([(X1-10,Y1-10),(X1+W2+10,Y1+H2+10)],fill=RED,width=8); d.line([(X1-10,Y1+H2+10),(X1+W2+10,Y1-10)],fill=RED,width=8)
d.text((X1+W2+40,Y1+60),"mesh strip along the whole bottom",font=f(28),fill=INK)
im.save(OUT+"/illustration_front_window.png")
print("ok")
