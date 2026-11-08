import numpy as np, matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt, csv
from matplotlib.patches import FancyBboxPatch, Rectangle, Circle, FancyArrowPatch, Wedge, Arc
import modelo as M
import os
R=os.path.join(os.path.dirname(os.path.abspath(__file__)),'..','figures')+os.sep
plt.rcParams.update({'font.family':'DejaVu Sans','font.size':10,'axes.grid':True,'grid.alpha':0.3,
 'axes.spines.top':False,'axes.spines.right':False,'savefig.dpi':200,'savefig.bbox':'tight'})
C1='#1f5fbf'; C2='#d1495b'; C3='#2a9d8f'; GR='#555555'
rng=np.random.default_rng(7)
DF=10e3
def save(fig,path): fig.savefig(R+path); plt.close(fig); print('ok',path)

# ---------- datos comunes ----------
b,m,x=M.tx(4000,DF)
sig={'A':0.0,'B':0.3,'C':0.6,'D':0.8}
rx={k:M.canal(x,s,np.random.default_rng(11)) for k,s in sig.items()}
out={(k,f):M.receptor(rx[k],DF,f) for k in sig for f in (False,True)}

# ---------- Fig 5: PSD de referencia ----------
f,p=M.psd(x)
fig,ax=plt.subplots(figsize=(7,3.4))
ax.plot(f/1e3,p,color=C1,lw=1.1,label='Tx ideal (Prueba A)')
for v in (-20,20): ax.axvline(v,color=GR,ls='--',lw=0.8)
for v in (-10,10): ax.axvline(v,color=C2,ls=':',lw=1)
ax.text(-19.5,-15,'B Carson ≈ 40 kHz',fontsize=8,color=GR)
ax.text(10.8,-5,'+Δf',color=C2,fontsize=9); ax.text(-15,-5,'−Δf',color=C2,fontsize=9)
ax.set_xlim(-100,100); ax.set_ylim(-110,5)
ax.set_xlabel('Frecuencia relativa a la portadora (kHz)'); ax.set_ylabel('PSD relativa (dB)')
ax.set_title('PSD de referencia: BFSK con Δf = 10 kHz, Rs = 10 kbaud (h = 2)'); ax.legend(loc='upper right',fontsize=8)
save(fig,'psd/fig05_psd_referencia_A.png')

# ---------- Fig 6: PSD bajo perturbacion ----------
fig,axs=plt.subplots(1,2,figsize=(10,3.4),sharey=True)
for ax,k in zip(axs,['C','D']):
    for v,lab,c in [(x,'Tx ideal',C1),(rx[k],'Salida del canal',C2),(out[(k,True)]['rin'],'Tras filtro de canal (R2)',C3)]:
        f,p=M.psd(v); ax.plot(f/1e3,p,lw=0.9,label=lab,color=c)
    ax.set_xlim(-200,200); ax.set_ylim(-110,5)
    ax.set_title(f'Prueba {k}: noise_voltage = {sig[k]}'); ax.set_xlabel('Frecuencia (kHz)')
axs[0].set_ylabel('PSD relativa (dB)'); axs[1].legend(fontsize=8,loc='upper right')
fig.suptitle('El ruido eleva un piso plano en toda la banda; el filtro de canal lo recorta fuera de ±20 kHz',fontsize=10.5,y=1.04)
save(fig,'psd/fig06_psd_perturbacion_C_D.png')

# ---------- Fig 12: PSD vs desviacion ----------
fig,ax=plt.subplots(figsize=(7,3.4))
for df,c in [(5e3,C3),(10e3,C1),(20e3,C2)]:
    _,_,xx=M.tx(4000,df); f,p=M.psd(xx)
    ax.plot(f/1e3,p,lw=1,color=c,label=f'Δf = {int(df/1e3)} kHz (h = {int(2*df/1e4)})')
ax.set_xlim(-100,100); ax.set_ylim(-110,5); ax.legend(fontsize=8)
ax.set_xlabel('Frecuencia (kHz)'); ax.set_ylabel('PSD relativa (dB)')
ax.set_title('Mayor desviación separa los tonos y ensancha el espectro')
save(fig,'psd/fig12_psd_vs_desviacion.png')

# ---------- Fig 7: frecuencia instantanea referencia ----------
n0,n1=2000,2000+1600
t=np.arange(n1-n0)/M.FS*1e3
o=out[('A',True)]; ref=M.delay(m,M.LPF_DELAY)
fig,ax=plt.subplots(figsize=(7,3.2))
ax.plot(t,ref[n0:n1],color=GR,lw=2.2,alpha=0.5,label='Referencia Tx (alineada)')
ax.plot(t,o['y'][n0:n1],color=C1,lw=1,label='Salida del discriminador')
ax.set_ylim(-2,2); ax.set_xlabel('Tiempo (ms)'); ax.set_ylabel('Frecuencia normalizada (×Δf)')
ax.set_title('Prueba A: el discriminador reproduce los niveles ±1'); ax.legend(fontsize=8,loc='upper right')
save(fig,'constelacion_o_fsk/fig07_frecuencia_instantanea_A.png')

# ---------- Fig 8: frecuencia instantanea C, R1 vs R2 ----------
fig,axs=plt.subplots(2,1,figsize=(7,5),sharex=True)
for ax,fl,tit in [(axs[0],False,'R1: discriminador directo'),(axs[1],True,'R2: filtro de canal + discriminador')]:
    o=out[('C',fl)]
    ax.plot(t,o['y'][n0:n1],color=C2 if not fl else C3,lw=0.6,label='Discriminador')
    ax.plot(t,o['ma'][n0:n1],color='k',lw=1.4,label='Integrador')
    ax.plot(t,ref[n0:n1],color=GR,lw=1,ls='--',label='Referencia Tx')
    ax.set_ylim(-6,6); ax.set_title(f'Prueba C (noise_voltage = 0.6), {tit}',fontsize=10); ax.set_ylabel('×Δf')
axs[0].legend(fontsize=7,loc='upper right',ncol=3); axs[1].set_xlabel('Tiempo (ms)')
save(fig,'constelacion_o_fsk/fig08_frecuencia_instantanea_C_R1_R2.png')

# ---------- Fig 9: ojos ----------
fig,axs=plt.subplots(2,4,figsize=(12,5),sharex=True,sharey=True)
tt=np.arange(2*M.SPS)
for j,k in enumerate('ABCD'):
    for i,fl in enumerate((False,True)):
        ax=axs[i,j]; ma=out[(k,fl)]['ma']
        start=M.LPF_DELAY%M.SPS + M.SPS-1 + 3*M.SPS
        for s in range(start,start+200*M.SPS,M.SPS):
            seg=ma[s-M.SPS+1: s-M.SPS+1+2*M.SPS]
            if len(seg)==2*M.SPS: ax.plot(tt,seg,color=C1 if fl else C2,lw=0.4,alpha=0.35)
        ax.axvline(M.SPS-1,color='k',ls='--',lw=0.8); ax.axhline(0,color=GR,lw=0.6)
        ax.set_ylim(-1.8,1.8)
        if i==0: ax.set_title(f'Prueba {k} (σ = {sig[k]})',fontsize=10)
        if j==0: ax.set_ylabel(['R1 sin filtro','R2 con filtro'][i])
        if i==1: ax.set_xlabel('Muestras (2 símbolos)')
fig.suptitle('Diagramas de ojo a la salida del integrador; línea discontinua = instante de muestreo',fontsize=11)
save(fig,'constelacion_o_fsk/fig09_diagramas_de_ojo.png')

# ---------- Fig 10: bits ----------
bt=M.delay(b,M.LPF_DELAY//M.SPS)
br1=out[('C',False)]['bits']; nn=min(len(bt),len(br1))
errs=(bt[:nn]!=br1[:nn]).astype(int); cs=np.convolve(errs[5:],np.ones(64),'valid'); W0=5+int(np.argmax((cs>=2)&(cs<=4))); W0=max(5,W0+30)
fig,axs=plt.subplots(2,1,figsize=(7,3.8),sharex=True)
for ax,fl,tit in [(axs[0],False,'R1'),(axs[1],True,'R2')]:
    br=out[('C',fl)]['bits']; idx=np.arange(W0,W0+64)
    ax.step(idx,bt[idx]+0.04,where='post',color=GR,lw=2,alpha=0.6,label='Bits Tx (retardados)')
    ax.step(idx,br[idx],where='post',color=C2 if not fl else C3,lw=1.2,label='Bits Rx')
    err=idx[bt[idx]!=br[idx]]
    ax.plot(err+0.5,np.full(len(err),1.25),'v',color=C2,ms=6,label='Error' if len(err) else None)
    ax.set_ylim(-0.3,1.45); ax.set_yticks([0,1]); ax.set_title(f'Prueba C, {tit}: {len(err)} errores en 64 bits',fontsize=10)
axs[0].legend(fontsize=7,ncol=3,loc='lower right'); axs[1].set_xlabel('Índice de bit')
save(fig,'constelacion_o_fsk/fig10_bits_tx_rx_C.png')

# ---------- Fig 13: envolvente ----------
fig,axs=plt.subplots(1,2,figsize=(10,3),sharey=True)
tt2=np.arange(400)/M.FS*1e3
for ax,k in zip(axs,['A','C']):
    ax.plot(tt2,rx[k][2000:2400].real,color=C1,lw=0.9,label='I')
    ax.plot(tt2,rx[k][2000:2400].imag,color=C2,lw=0.9,label='Q')
    ax.set_title(f'Envolvente compleja a la salida del canal, Prueba {k}',fontsize=10); ax.set_xlabel('Tiempo (ms)')
axs[0].set_ylabel('Amplitud'); axs[0].legend(fontsize=8); axs[0].set_ylim(-3,3)
save(fig,'constelacion_o_fsk/fig13_envolvente_A_C.png')

# ---------- Fig 11: BER vs ruido ----------
rows=list(csv.DictReader(open(os.path.join(R,'..','data','tablas_de_pruebas','barrido_ruido.csv'))))
s=np.array([float(r['noise_voltage']) for r in rows]); e=20-20*np.log10(s)
b1=np.array([float(r['BER_R1']) for r in rows]); b2=np.array([float(r['BER_R2']) for r in rows])
fl=1e-5
fig,ax=plt.subplots(figsize=(7,3.8))
ee=np.linspace(6,34,200); ax.semilogy(ee,0.5*np.exp(-10**(ee/10)/2),color=GR,ls='--',lw=1,label='Teoría BFSK no coherente óptima')
ax.semilogy(e,np.maximum(b1,fl),'o-',color=C2,label='R1: discriminador directo')
ax.semilogy(e,np.maximum(b2,fl),'s-',color=C3,label='R2: filtro de canal + discriminador')
for k,sv in sig.items():
    if sv: ax.axvline(20-20*np.log10(sv),color='k',lw=0.6,ls=':'); ax.text(20-20*np.log10(sv)+0.2,0.6,k,fontsize=9)
ax.set_ylim(fl,1); ax.set_xlim(6,35); ax.set_xlabel('Eb/N0 (dB)   [= 20 − 20·log10(noise_voltage)]')
ax.set_ylabel('BER'); ax.set_title('El filtro de canal desplaza la curva de BER unos 13 dB'); ax.legend(fontsize=8,loc='lower left')
ax.text(34.8,3e-5,'BER = 0 se grafica en 1e-5',fontsize=7,ha='right',color=GR)
save(fig,'constelacion_o_fsk/fig11_ber_vs_ruido.png')
