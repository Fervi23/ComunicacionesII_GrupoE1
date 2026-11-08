import numpy as np, csv, json, os, modelo as M
OUT=os.path.join(os.path.dirname(os.path.abspath(__file__)),'..','data','tablas_de_pruebas')
rng=np.random.default_rng(2026)
N=100000
def run(sigma,df,filt):
    b,m,x=M.tx(N,df); r=M.canal(x,sigma,rng); o=M.receptor(r,df,filt); return M.ber(b,o['bits'])
rows=[]
pruebas=[('A','Referencia',0.0),('B','Suave',0.3),('C','Media',0.6),('D','Fuerte',0.8)]
for pid,sev,s in pruebas:
    r1=run(s,10e3,False); r2=run(s,10e3,True)
    snr=np.inf if s==0 else -20*np.log10(s)
    ebn0=np.inf if s==0 else 20-20*np.log10(s)
    rows.append(dict(prueba=pid,severidad=sev,noise_voltage=s,fsk_deviation_Hz=10000,samp_rate=1e6,sps=100,
      Rs_baud=10000,SNR_1MHz_dB=round(snr,1) if s else 'inf',EbN0_dB=round(ebn0,1) if s else 'inf',
      BER_R1=r1[0],errores_R1=r1[1],BER_R2=r2[0],errores_R2=r2[1],bits=r1[2]))
    print(rows[-1])
with open(os.path.join(OUT,'pruebas.csv'),'w',newline='') as f:
    w=csv.DictWriter(f,fieldnames=rows[0].keys()); w.writeheader(); w.writerows(rows)
# barrido BER vs noise_voltage
sig=[0.2,0.3,0.4,0.5,0.6,0.7,0.8,1.0,1.25,1.5,2.0,2.5,3.0,3.5,4.0]
curva=[]
for s in sig:
    r1=run(s,10e3,False)[0]; r2=run(s,10e3,True)[0]
    curva.append(dict(noise_voltage=s,EbN0_dB=round(20-20*np.log10(s),2),BER_R1=r1,BER_R2=r2)); print(curva[-1])
with open(os.path.join(OUT,'barrido_ruido.csv'),'w',newline='') as f:
    w=csv.DictWriter(f,fieldnames=curva[0].keys()); w.writeheader(); w.writerows(curva)
# barrido delta f (R1, C)
dfr=[]
for df in [5e3,10e3,20e3]:
    dfr.append(dict(fsk_deviation_Hz=int(df),h=int(2*df/1e4),noise_voltage=0.6,BER_R1=run(0.6,df,False)[0],BER_R2=run(0.6,df,True)[0]))
    print(dfr[-1])
with open(os.path.join(OUT,'barrido_desviacion.csv'),'w',newline='') as f:
    w=csv.DictWriter(f,fieldnames=dfr[0].keys()); w.writeheader(); w.writerows(dfr)
