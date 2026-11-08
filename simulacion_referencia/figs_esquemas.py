import numpy as np, matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, Rectangle, Circle, Polygon, Arc
import os
R=os.path.join(os.path.dirname(os.path.abspath(__file__)),'..','figures')+os.sep
plt.rcParams.update({'font.family':'DejaVu Sans','font.size':9,'savefig.dpi':200,'savefig.bbox':'tight'})
C1='#1f5fbf'; C2='#d1495b'; C3='#2a9d8f'; GR='#555555'; WALL='#8d8d8d'

# ===================== Fig 1: escenario contextual =====================
fig,ax=plt.subplots(figsize=(11,7)); ax.set_xlim(0,110); ax.set_ylim(-7,66); ax.set_aspect('equal'); ax.axis('off')
ax.add_patch(Rectangle((1,1),108,62,fill=False,lw=2.5,ec=WALL))
ax.text(3,60,'Planta de tratamiento de agua: vista en planta (esquema, no a escala)',fontsize=11,weight='bold')
def zona(x,y,w,h,txt,fc='#f3f3f3'):
    ax.add_patch(FancyBboxPatch((x,y),w,h,boxstyle='round,pad=0.3,rounding_size=1',fc=fc,ec=WALL,lw=1.2))
    ax.text(x+w/2,y+h-2,txt,ha='center',fontsize=8.5,color='#333')
zona(4,30,27,25,'Tanques de sedimentación')
for cx,cy in [(11.5,39.5),(23.5,39.5)]:
    ax.add_patch(Circle((cx,cy),5.2,fc='#d8e8f6',ec='#6a8fb5',lw=1.5)); ax.add_patch(Circle((cx,cy),3.4,fc='none',ec='#6a8fb5',lw=0.8,ls='--'))
zona(4,4,27,22,'Estación de bombeo')
for cx in [10,17.5,25]:
    ax.add_patch(Circle((cx,10.5),2.6,fc='#e9e9e9',ec='#666',lw=1.2)); ax.text(cx,10,'M',ha='center',fontsize=8,weight='bold')
ax.add_patch(Rectangle((7,15.5),21,1.2,fc='#9fb3c8',ec='none')); ax.text(17.5,17.6,'tubería metálica',ha='center',fontsize=7,color='#456')
zona(42,4,24,20,'Filtros y válvulas')
for cx in [48,54,60]: ax.add_patch(Rectangle((cx-2.3,7),4.6,8.5,fc='#ececec',ec='#777'))
zona(80,30,26,25,'Sala de control',fc='#eef5ff')
ax.add_patch(Rectangle((86,33.5),14,5,fc='#cfd8e3',ec='#667')); ax.text(93,35.5,'SCADA / PC',ha='center',fontsize=7.5)
ax.add_patch(Rectangle((87,41),6,4,fc='#ddd',ec='#667')); ax.text(90,42.5,'Rx',ha='center',fontsize=8,weight='bold')
ax.add_patch(Rectangle((71,8),1.6,38,fc='#bdbdbd',ec='#888')); ax.text(69.4,27,'muro de concreto',rotation=90,fontsize=7.5,color='#555',va='center')
def antena(x,y,c):
    ax.plot([x,x],[y,y+4],color=c,lw=1.8); ax.add_patch(Polygon([[x-1.2,y+4],[x+1.2,y+4],[x,y+6]],closed=True,fc=c,ec=c))
RX=(96,45)
antena(RX[0],RX[1],C3); ax.text(RX[0]+1.6,48.5,'Antena Rx',fontsize=7.5,color=C3)
ax.plot([93,96],[43,45],color='#667',lw=1)
nodos=[(36.5,44,'Tx1','nivel de tanque'),(36.5,14,'Tx2','estado de bombas'),(59.5,17.8,'Tx3','posición de válvulas')]
for x,y,l,sub in nodos:
    ax.add_patch(FancyBboxPatch((x-2.5,y-1.5),5,3,boxstyle='round,pad=0.2',fc='white',ec=C1,lw=1.6))
    ax.text(x,y-0.5,l,ha='center',fontsize=8,weight='bold',color=C1); antena(x+1.4,y+1.5,C1)
    ax.text(x,y-4,sub,ha='center',fontsize=7,color='#222',bbox=dict(fc='white',ec='none',pad=0.5,alpha=0.9))
    sx,sy=x+1.4,y+7.5; tx_,ty_=RX[0],RX[1]+6
    ax.annotate('',xy=(tx_,ty_),xytext=(sx,sy),arrowprops=dict(arrowstyle='->',color=C1,lw=1.1,ls=(0,(5,3))))
    ang=np.degrees(np.arctan2(ty_-sy,tx_-sx))
    for r in (2,3.1,4.2): ax.add_patch(Arc((sx,sy),2*r,2*r,theta1=ang-25,theta2=ang+25,color=C1,lw=1))
ax.text(62,56,'camino directo, d ≈ 80–300 m: la potencia recibida cae con la distancia',fontsize=7.5,color=C1,ha='center',
        bbox=dict(fc='white',ec='none',alpha=0.9))
ax.text(93,27.2,'BFSK ±10 kHz · 10 kbit/s · ISM sub-GHz',fontsize=7,ha='center',color='#333')
ax.add_patch(FancyBboxPatch((77,8),29,10,boxstyle='round,pad=0.3',fc='#fdecee',ec=C2,lw=1.2))
ax.text(91.5,15.2,'Perturbación modelada: AWGN',ha='center',fontsize=8,weight='bold',color=C2)
ax.text(91.5,12.5,'ruido térmico del Rx + ruido de fondo',ha='center',fontsize=7.2)
ax.text(91.5,10,'noise_voltage = 0 / 0.3 / 0.6 / 0.8',ha='center',fontsize=7.2,family='DejaVu Sans Mono')
ax.annotate('',xy=(90,40.6),xytext=(90,18.4),arrowprops=dict(arrowstyle='->',color=C2,lw=1.2))
items=[(C1,'Nodo Tx con antena'),(C3,'Receptor (Rx)'),(C1,'Trayectoria directa (línea discontinua)'),(C2,'Perturbación (AWGN)'),(WALL,'Muros y obstáculos')]
pos=[3,26,45,77,98]
for (c,t),x0 in zip(items,pos):
    ax.add_patch(Rectangle((x0,-4),1.6,1.6,fc=c,ec='none')); ax.text(x0+2.3,-3.7,t,fontsize=7)
fig.savefig(R+'escenario/fig01_escenario_contextual.png'); plt.close(fig); print('fig01')

# ===================== Fig 2: diagrama tecnico =====================
fig,ax=plt.subplots(figsize=(13,5.4)); ax.set_xlim(0,130); ax.set_ylim(0,54); ax.axis('off')
def caja(x,y,w,h,t1,t2,c='#333',fc='white',lw=1.2):
    ax.add_patch(FancyBboxPatch((x,y),w,h,boxstyle='round,pad=0.2,rounding_size=1',fc=fc,ec=c,lw=lw))
    ax.text(x+w/2,y+h*0.64,t1,ha='center',va='center',fontsize=7.8,weight='bold')
    ax.text(x+w/2,y+h*0.28,t2,ha='center',va='center',fontsize=6.8,color='#444')
def fl(x1,y1,x2,y2,c=GR): ax.annotate('',xy=(x2,y2),xytext=(x1,y1),arrowprops=dict(arrowstyle='->',color=c,lw=1.1))
ax.text(1,51.5,'S5: sistema Tx–canal–Rx (S5_BFSK_TxCanalRx_GrupoE1.grc)',fontsize=11,weight='bold')
w,h,g=17,7.5,3.5; y1=38
ax.text(1,47,'TRANSMISOR',fontsize=8,color=C1,weight='bold'); ax.text(5*(w+g)+1,47,'CANAL',fontsize=8,color=C2,weight='bold')
tx=[('Vector Source','16 bits, se repite'),('Chunks to Symbols','0 → −1, 1 → +1'),('Repeat','×100 (sps)'),('Frequency Mod','k = 2πΔf / fs'),('Throttle','fs = 1 MS/s'),('Channel Model','noise_voltage, taps = 1')]
for i,(a,b) in enumerate(tx):
    x=1+i*(w+g); caja(x,y1,w,h,a,b,c=C2 if i==5 else C1,fc='#fdecee' if i==5 else 'white')
    if i: fl(x-g,y1+h/2,x,y1+h/2)
ax.text(1,31,'RECEPTOR',fontsize=8,color=C3,weight='bold')
y2=17; w2,g2=14.5,2.6
caja(1,y2+5,w2,h,'LPF canal (R2)','fc 20 kHz, 241 taps',c=C3,fc='#e6f4f2',lw=2)
caja(1,y2-5,w2,h,'Delay (R1)','lpf_delay = 120',c=GR)
chx=5*(w+g)+1+w/2
ax.plot([chx,chx],[y1,33],color=GR,lw=1.1); ax.plot([chx,-0.5+0.5],[33,33],color=GR,lw=1.1)
ax.plot([0.5,0.5],[33,y2-5+h/2],color=GR,lw=1.1); fl(0.5,y2+5+h/2,1,y2+5+h/2); fl(0.5,y2-5+h/2,1,y2-5+h/2)
rxb=[('Mezcla R1/R2','Multiply Const + Add'),('Quad. Demod','G = fs / (2πΔf)'),('Moving Average','L = sps, escala 1/sps'),('Skip Head','skip = 20 muestras'),('Keep One in N','N = sps = 100'),('Binary Slicer','umbral 0')]
xs=1+w2+g2+2
for i,(a,b) in enumerate(rxb):
    x=xs+i*(w2+g2); caja(x,y2,w2,h,a,b,c=C3)
    if i: fl(x-g2,y2+h/2,x,y2+h/2)
fl(1+w2,y2+5+h/2,xs,y2+h*0.7,C3); fl(1+w2,y2-5+h/2,xs,y2+h*0.3,GR)
xl=xs+5*(w2+g2)
caja(xl,1,w2,h,'XOR + BER','Tx retardado 1 bit',c='#777'); fl(xl+w2/2,y2,xl+w2/2,1+h)
caja(xs+2*(w2+g2),1,w2,h,'Eye Sink','instante óptimo',c='#777'); fl(xs+2*(w2+g2)+w2/2,y2,xs+2*(w2+g2)+w2/2,1+h)
ax.add_patch(FancyBboxPatch((1,0.5),40,8,boxstyle='round,pad=0.3',fc='#f7f7f7',ec='#bbb'))
for i,t in enumerate(['M = 2, k = 1, Rs = Rb = 10 kbit/s','SPS = 100, fs = Rs·SPS = 1 MS/s','Δf = 10 kHz, h = 2Δf/Rs = 2, B ≈ 40 kHz']):
    ax.text(21,6.6-i*2.4,t,ha='center',fontsize=7.4)
fig.savefig(R+'diagramas_tecnicos/fig02_diagrama_tecnico_tx_canal_rx.png'); plt.close(fig); print('fig02')

# ===================== Fig 3: estados FSK =====================
fig,axs=plt.subplots(1,2,figsize=(11,3.4),gridspec_kw={'width_ratios':[1.4,1]})
bits=[0,1,0,0,1,1,0,1]; t=np.arange(0,8,0.002); m=np.array([2*bits[int(v)]-1 for v in t])
ax=axs[0]; ax.step(np.arange(9),[2*b-1 for b in bits]+[2*bits[-1]-1],where='post',color=C1,lw=1.5,label='m(t): nivel NRZ')
ph=np.cumsum(m)*0.002*2*np.pi*2.0   # ilustrativo: 2 ciclos por simbolo para h=... (dibujo)
ax.plot(t,0.6*np.cos(ph+2*np.pi*3*t)-0,color=GR,lw=0.6,alpha=0.8,label='Portadora FSK (ilustrativa)')
for i,b in enumerate(bits): ax.text(i+0.5,1.35,str(b),ha='center',fontsize=10,weight='bold')
ax.set_ylim(-1.6,1.7); ax.set_xlabel('Tiempo (símbolos, Ts = 100 µs)'); ax.set_yticks([-1,0,1]); ax.legend(fontsize=7,loc='lower right')
ax.set_title('Bits → niveles ±1 → frecuencia instantánea ±Δf',fontsize=10)
ax=axs[1]
for f0,c,lab in [(-10,C2,'bit 0: −Δf'),(10,C1,'bit 1: +Δf')]:
    ff=np.linspace(-40,40,800); ax.plot(ff,np.exp(-((ff-f0)/3)**2),color=c,lw=1.6); ax.text(f0,1.07,lab,ha='center',color=c,fontsize=8.5)
ax.annotate('',xy=(10,0.55),xytext=(-10,0.55),arrowprops=dict(arrowstyle='<->',color='k')); ax.text(0,0.6,'2Δf = 20 kHz',ha='center',fontsize=8)
ax.annotate('',xy=(20,0.15),xytext=(-20,0.15),arrowprops=dict(arrowstyle='<->',color=GR)); ax.text(0,0.22,'B ≈ 2(Δf + Rs) = 40 kHz',ha='center',fontsize=8,color=GR,bbox=dict(fc='white',ec='none',pad=0.5))
ax.set_xlim(-40,40); ax.set_ylim(0,1.25); ax.set_yticks([]); ax.set_xlabel('Frecuencia relativa (kHz)')
ax.set_title('Dos estados de frecuencia (esquema)',fontsize=10); ax.spines[['top','right','left']].set_visible(False)
fig.tight_layout(); fig.savefig(R+'diagramas_tecnicos/fig03_estados_fsk.png'); plt.close(fig); print('fig03')
