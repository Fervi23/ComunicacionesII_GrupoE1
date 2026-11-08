"""Modelo numerico de referencia del GRC S5_BFSK_TxCanalRx (misma cadena y mismos retardos)."""
import numpy as np
from scipy import signal
FS=1e6; SPS=100; RS=FS/SPS
PAT=np.array([0,1,0,0,1,1,0,1,1,1,0,0,1,0,1,0],dtype=np.uint8)
LPF_CUT=20e3; LPF_W=10e3
def gr_lowpass(fs=FS,fc=LPF_CUT,tw=LPF_W):
    n=int(53*fs/(22.0*tw)); n+= (n%2==0)
    m=np.arange(n)-(n-1)/2
    h=np.sinc(2*fc/fs*m)*2*fc/fs*np.hamming(n)
    return h/h.sum()
TAPS=gr_lowpass(); LPF_DELAY=(len(TAPS)-1)//2
def tx(nbits,df):
    bits=np.tile(PAT,int(np.ceil(nbits/16)))[:nbits]
    m=np.repeat(2.0*bits-1,SPS)
    x=np.exp(1j*np.cumsum(2*np.pi*df/FS*m))
    return bits,m,x
def canal(x,sigma,rng):
    n=sigma*(rng.standard_normal(len(x))+1j*rng.standard_normal(len(x)))/np.sqrt(2)
    return x+n
def delay(v,d): return np.r_[np.zeros(d,dtype=v.dtype),v[:len(v)-d]]
def demod(r,df):
    prev=np.r_[0,r[:-1]]
    return FS/(2*np.pi*df)*np.angle(r*np.conj(prev))
def receptor(r,df,usar_filtro,ajuste=0):
    rin=np.convolve(r,TAPS)[:len(r)] if usar_filtro else delay(r,LPF_DELAY)
    y=demod(rin,df)
    ma=np.convolve(y,np.ones(SPS)/SPS)[:len(y)]
    skip=(LPF_DELAY+ajuste)%SPS
    s=ma[skip:]; n=len(s)//SPS
    muestras=s[SPS-1::SPS][:n]          # Keep One in N conserva la ultima de cada bloque
    bits=(muestras>=0).astype(np.uint8)
    return dict(rin=rin,y=y,ma=ma,muestras=muestras,bits=bits)
def ber(bits_tx,bits_rx,ajuste=0,descartar=3):
    D=(LPF_DELAY+ajuste)//SPS
    ref=delay(bits_tx,D)
    n=min(len(ref),len(bits_rx))
    e=(ref[descartar:n]^bits_rx[descartar:n])
    return e.mean(), int(e.sum()), len(e)
def psd(v,nfft=2048):
    f,p=signal.welch(v,FS,window='blackmanharris',nperseg=nfft,return_onesided=False,scaling='density')
    i=np.argsort(f); return f[i],10*np.log10(p[i]*FS/nfft+1e-20)
