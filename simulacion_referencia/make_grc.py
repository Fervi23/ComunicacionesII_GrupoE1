import yaml, sys
blocks=[]; conns=[]
def B(name, bid, params, xy, state='enabled'):
    p={k:str(v) for k,v in params.items()}
    p.setdefault('comment','')
    blocks.append({'name':name,'id':bid,'parameters':p,
      'states':{'bus_sink':False,'bus_source':False,'bus_structure':None,
                'coordinate':[xy[0],xy[1]],'rotation':0,'state':state}})
def C(a,pa,b,pb): conns.append([a,str(pa),b,str(pb)])
def var(name,value,xy,comment=''): B(name,'variable',{'value':value,'comment':comment},xy)
def rng(name,label,start,stop,step,value,xy):
    B(name,'variable_qtgui_range',{'gui_hint':'','label':label,'min_len':200,
      'orient':'QtCore.Qt.Horizontal','rangeType':'float','start':start,'step':step,
      'stop':stop,'value':value,'widget':'counter_slider'},xy)
def tsink(name,title,typ,n,srate,labels,ymin,ymax,hint,size=4096,ylabel='Amplitud'):
    p={'type':typ,'name':f'"{title}"','nconnections':n,'size':size,'srate':srate,
       'autoscale':'False','grid':'True','legend':'True','ymin':ymin,'ymax':ymax,
       'ylabel':ylabel,'yunit':'""','update_time':'0.10','gui_hint':hint,'entags':'True',
       'axislabels':'True','ctrlpanel':'False','stemplot':'False',
       'tr_mode':'qtgui.TRIG_MODE_FREE','tr_slope':'qtgui.TRIG_SLOPE_POS',
       'tr_chan':0,'tr_delay':0,'tr_level':'0.0','tr_tag':'""'}
    for i in range(10):
        p[f'label{i+1}']=labels[i] if i<len(labels) else ''
        p[f'color{i+1}']=['blue','red','green','black','cyan','magenta','yellow','dark red','dark green','dark blue'][i]
        p[f'width{i+1}']=1; p[f'style{i+1}']=1; p[f'marker{i+1}']=-1; p[f'alpha{i+1}']='1.0'
    return p

# ---------------- opciones ----------------
options={'parameters':{'author':'Grupo E1','catch_exceptions':'True','category':'[GRC Hier Blocks]',
  'cmake_opt':'','comment':'','copyright':'',
  'description':'S5 Telemetria binaria BFSK: Tx CPFSK, canal AWGN y receptor no coherente '
                '(filtro de canal, discriminador, integrador, muestreo, slicer y BER).',
  'gen_cmake':'On','gen_linking':'dynamic','generate_options':'qt_gui','hier_block_src_path':'.:',
  'id':'S5_BFSK_TxCanalRx_GrupoE1','max_nouts':'0','output_language':'python','placement':'(0,0)',
  'qt_qss_theme':'','realtime_scheduling':'','run':'True','run_command':'{python} -u {filename}',
  'run_options':'prompt','sizing_mode':'fixed','thread_safe_setters':'',
  'title':'S5 - Telemetria binaria BFSK: Tx - canal AWGN - Rx','window_size':'(1500,950)'},
  'states':{'bus_sink':False,'bus_source':False,'bus_structure':None,'coordinate':[8,8],'rotation':0,'state':'enabled'}}

# ---------------- imports y variables ----------------
B('import_math','import',{'imports':'import math'},[1500,8])
B('import_firdes','import',{'imports':'from gnuradio.filter import firdes'},[1500,56])
B('import_window','import',{'imports':'from gnuradio.fft import window'},[1500,104])
var('samp_rate','1e6',[200,8])
var('sps','100',[300,8])
var('symbol_rate','samp_rate/sps',[400,8])
var('Rb','symbol_rate',[520,8],'BFSK binaria: Rb = Rs')
var('h_fsk','2*fsk_deviation/symbol_rate',[620,8],'Indice de modulacion')
rng('fsk_deviation','Desviacion FSK (Hz)',5000,100000,1000,10000,[740,8])
rng('noise_voltage','Noise voltage (A=0, B=0.3, C=0.6, D=0.8)',0.0,5.0,0.01,0.6,[940,8])
B('receptor','variable_qtgui_chooser',{'gui_hint':'','label':'Receptor','type':'int',
  'num_opts':2,'option0':0,'label0':'R1: discriminador directo (base)',
  'option1':1,'label1':'R2: filtro de canal + discriminador','value':1,
  'widget':'combo_box','orient':'Qt.QVBoxLayout','labels':'[]','options':'[0, 1, 2]'},[1180,8])
var('lpf_cutoff','20e3',[200,200],'= fsk_deviation + symbol_rate (recalcular si cambia el diseno)')
var('lpf_width','10e3',[320,200])
var('lpf_taps','firdes.low_pass(1.0, samp_rate, lpf_cutoff, lpf_width, window.WIN_HAMMING, 6.76)',[440,200])
var('lpf_delay','(len(lpf_taps)-1)//2',[700,200],'Retardo de grupo del filtro de canal (muestras)')
var('skip_muestreo','(lpf_delay + ajuste_muestreo) % sps',[840,200],'Fase de muestreo: ultima muestra de cada ventana')
var('ajuste_muestreo','0',[1010,200],'Ajuste fino (muestras), fijarlo en la Prueba A')
var('retardo_bits','(lpf_delay + ajuste_muestreo)//sps',[1150,200],'D_b: retardo de la referencia Tx en bits')
B('tabs','qtgui_tab_widget',{'gui_hint':'','num_tabs':4,'label0':'Tx y canal','label1':'Discriminador',
  'label2':'Ojo y decision','label3':'Validacion (BER)'},[1300,200])

# ---------------- transmisor (igual a la base) ----------------
B('bit_source','blocks_vector_source_x',{'type':'byte','vector':'[0,1,0,0,1,1,0,1,1,1,0,0,1,0,1,0]',
  'repeat':'True','tags':'[]','vlen':1},[24,380])
B('nrz_mapper','digital_chunks_to_symbols_xx',{'in_type':'byte','out_type':'float',
  'symbol_table':'[-1.0, 1.0]','dimension':1,'num_ports':1},[232,396])
B('symbol_repeat','blocks_repeat',{'type':'float','interp':'sps','vlen':1},[440,404])
B('fsk_modulator','analog_frequency_modulator_fc',{'sensitivity':'2*math.pi*fsk_deviation/samp_rate'},[616,404])
B('throttle','blocks_throttle2',{'type':'complex','samples_per_second':'samp_rate','vlen':1,
  'ignoretag':'True','limit':'auto','maximum':'0.1'},[824,396])
C('bit_source',0,'nrz_mapper',0); C('nrz_mapper',0,'symbol_repeat',0)
C('symbol_repeat',0,'fsk_modulator',0); C('fsk_modulator',0,'throttle',0)

# ---------------- canal ----------------
B('channel_awgn','channels_channel_model',{'noise_voltage':'noise_voltage','freq_offset':'0.0',
  'epsilon':'1.0','taps':'1.0 + 0.0j','seed':0,'block_tags':'True'},[1000,380])
C('throttle',0,'channel_awgn',0)

# ---------------- receptor ----------------
B('filtro_canal','fir_filter_xxx',{'type':'ccf','decim':1,'taps':'lpf_taps','samp_delay':0},[1240,540])
B('compensa_r1','blocks_delay',{'type':'complex','delay':'lpf_delay','num_ports':1,'vlen':1,
  'showports':'False'},[1240,628])
B('peso_r1','blocks_multiply_const_vxx',{'type':'complex','const':'1-receptor','vlen':1},[1460,620])
B('peso_r2','blocks_multiply_const_vxx',{'type':'complex','const':'receptor','vlen':1},[1460,540])
B('selector_receptor','blocks_add_xx',{'type':'complex','num_inputs':2,'vlen':1},[1660,576])
C('channel_awgn',0,'filtro_canal',0); C('channel_awgn',0,'compensa_r1',0)
C('compensa_r1',0,'peso_r1',0); C('filtro_canal',0,'peso_r2',0)
C('peso_r1',0,'selector_receptor',0); C('peso_r2',0,'selector_receptor',1)
B('discriminador_frecuencia_rx','analog_quadrature_demod_cf',
  {'gain':'samp_rate/(2*math.pi*fsk_deviation)'},[1840,580])
C('selector_receptor',0,'discriminador_frecuencia_rx',0)
B('integrador_simbolo','blocks_moving_average_xx',{'type':'float','length':'sps','scale':'1.0/sps',
  'max_iter':4000,'vlen':1},[2060,572])
C('discriminador_frecuencia_rx',0,'integrador_simbolo',0)
B('fase_muestreo','blocks_skiphead',{'type':'float','num_items':'skip_muestreo','vlen':1},[2280,580])
B('una_por_simbolo','blocks_keep_one_in_n',{'type':'float','n':'sps','vlen':1},[2470,580])
B('decision_binaria','digital_binary_slicer_fb',{},[2660,588])
C('integrador_simbolo',0,'fase_muestreo',0); C('fase_muestreo',0,'una_por_simbolo',0)
C('una_por_simbolo',0,'decision_binaria',0)

# ---------------- referencia Tx para observar ----------------
B('observador_frecuencia_tx','analog_quadrature_demod_cf',{'gain':'samp_rate/(2*math.pi*fsk_deviation)'},[1240,300])
B('alinea_ref_tx','blocks_delay',{'type':'float','delay':'lpf_delay','num_ports':1,'vlen':1,'showports':'False'},[1460,300])
C('throttle',0,'observador_frecuencia_tx',0); C('observador_frecuencia_tx',0,'alinea_ref_tx',0)

# ---------------- validacion BER ----------------
B('retardo_ref_bits','blocks_delay',{'type':'byte','delay':'retardo_bits','num_ports':1,'vlen':1,'showports':'False'},[240,820])
B('comparador_xor','blocks_xor_xx',{'type':'byte','num_inputs':2,'vlen':1},[2860,760])
B('errores_a_float','blocks_uchar_to_float',{},[3020,772])
B('ber_ventana','blocks_moving_average_xx',{'type':'float','length':1000,'scale':'1.0/1000',
  'max_iter':4000,'vlen':1},[3180,756])
C('bit_source',0,'retardo_ref_bits',0)
C('retardo_ref_bits',0,'comparador_xor',0); C('decision_binaria',0,'comparador_xor',1)
C('comparador_xor',0,'errores_a_float',0); C('errores_a_float',0,'ber_ventana',0)
B('bits_tx_float','blocks_uchar_to_float',{},[2860,880])
B('bits_rx_float','blocks_uchar_to_float',{},[2860,940])
C('retardo_ref_bits',0,'bits_tx_float',0); C('decision_binaria',0,'bits_rx_float',0)

# ---------------- visualizaciones ----------------
B('psd_tx_canal_rx','qtgui_freq_sink_x',{'type':'complex','name':'"PSD: Tx, salida del canal y entrada al discriminador"',
  'fftsize':2048,'wintype':'window.WIN_BLACKMAN_hARRIS','fc':0,'bw':'samp_rate','nconnections':3,
  'average':'1.0','autoscale':'False','grid':'True','legend':'True','ymin':-140,'ymax':10,
  'units':'dB','label':'Relative Gain','update_time':'0.10','freqhalf':'True','showports':'False',
  'axislabels':'True','ctrlpanel':'False','norm_window':'False','gui_hint':'tabs@0',
  'tr_mode':'qtgui.TRIG_MODE_FREE','tr_chan':0,'tr_level':'0.0','tr_tag':'""',
  'label1':'Tx ideal','label2':'Salida del canal','label3':'Entrada al discriminador',
  'color1':'"blue"','color2':'"red"','color3':'"green"'},[1840,760])
C('throttle',0,'psd_tx_canal_rx',0); C('channel_awgn',0,'psd_tx_canal_rx',1); C('selector_receptor',0,'psd_tx_canal_rx',2)
B('envolvente_tx_canal','qtgui_time_sink_x',tsink('envolvente_tx_canal','Envolvente compleja: Tx vs salida del canal',
  'complex',2,'samp_rate',['Re Tx','Im Tx','Re canal','Im canal'],-2,2,'tabs@0',size=1024),[1660,640])
C('throttle',0,'envolvente_tx_canal',0); C('channel_awgn',0,'envolvente_tx_canal',1)
B('frecuencia_instantanea','qtgui_time_sink_x',tsink('frecuencia_instantanea',
  'Frecuencia instantanea normalizada: referencia Tx vs discriminador Rx','float',3,'samp_rate',
  ['Referencia Tx','Discriminador Rx','Integrador (Moving Average)'],-3,3,'tabs@1'),[2100,120])
C('alinea_ref_tx',0,'frecuencia_instantanea',0); C('discriminador_frecuencia_rx',0,'frecuencia_instantanea',1)
C('integrador_simbolo',0,'frecuencia_instantanea',2)
eye={'type':'float','name':'"Diagrama de ojo a la salida del integrador"','nconnections':1,'size':2000,
     'srate':'samp_rate','sps':'sps','ymin':-2,'ymax':2,'autoscale':'False','grid':'True','legend':'True',
     'update_time':'0.10','gui_hint':'tabs@2','entags':'True','axislabels':'True','ctrlpanel':'False',
     'ylabel':'Amplitud','yunit':'""','tr_mode':'qtgui.TRIG_MODE_FREE','tr_slope':'qtgui.TRIG_SLOPE_POS',
     'tr_chan':0,'tr_delay':0,'tr_level':'0.0','tr_tag':'""','label1':'Integrador','color1':'blue',
     'width1':1,'style1':1,'marker1':-1,'alpha1':'1.0'}
B('diagrama_ojo','qtgui_eye_sink_x',eye,[2100,40])
C('integrador_simbolo',0,'diagrama_ojo',0)
B('muestras_decision','qtgui_time_sink_x',tsink('muestras_decision','Muestras de decision (una por simbolo)',
  'float',1,'symbol_rate',['Muestra en el instante optimo'],-2,2,'tabs@2',size=256),[2460,120])
C('una_por_simbolo',0,'muestras_decision',0)
B('bits_tx_vs_rx','qtgui_time_sink_x',tsink('bits_tx_vs_rx','Bits Tx (retardados) vs bits Rx',
  'float',2,'symbol_rate',['Bits Tx','Bits Rx'],-0.5,1.5,'tabs@3',size=64),[2860,580])
C('bits_tx_float',0,'bits_tx_vs_rx',0); C('bits_rx_float',0,'bits_tx_vs_rx',1)
B('ber_estimada','qtgui_number_sink',{'type':'float','name':'"BER estimada (ventana de 1000 bits)"',
  'nconnections':1,'graph_type':'qtgui.NUM_GRAPH_HORIZ','min':0,'max':0.5,'avg':0,'autoscale':'False',
  'update_time':'0.20','gui_hint':'tabs@3','label1':'BER','unit1':'','factor1':1,'decimals1':4,
  'color1':'("black", "black")'},[2660,420])
C('ber_ventana',0,'ber_estimada',0)

doc={'options':options,'blocks':blocks,'connections':conns,
     'metadata':{'file_format':1,'grc_version':'3.10.12.0'}}
out=sys.argv[1]
with open(out,'w') as f: yaml.safe_dump(doc,f,sort_keys=False,allow_unicode=True,width=1000)
print(len(blocks),'blocks',len(conns),'connections')
