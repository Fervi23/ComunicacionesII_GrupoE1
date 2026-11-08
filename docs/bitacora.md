# Bitácora del proyecto (S5, BFSK)

Registrar fecha, responsable y commit asociado en cada entrada.

| Fecha | Etapa | Decisión o resultado | Evidencia |
| --- | --- | --- | --- |
| _(completar)_ | Guía 1 | Se observaron envolvente compleja, PSD y frecuencia instantánea de FSK, ideal y con AWGN. Aparecen espigas en la frecuencia instantánea con ruido. | Capturas de la Guía 1 |
| _(completar)_ | Selección | Escenario S5 (telemetría binaria FSK) en una planta de tratamiento de agua. BFSK frente a BPSK: se descarta BPSK por la recuperación de portadora. | Ficha de Decisión Técnica Ciega |
| _(completar)_ | Parámetros | Rs = Rb = 10 kbit/s, SPS = 100, fs = 1 MS/s. Δf baja de 20 a 10 kHz (h = 2, B ≈ 40 kHz). | Tabla de parámetros |
| _(completar)_ | Receptor v1 | Discriminador → Moving Average → Keep One in N → Binary Slicer. Funciona en A y B; en C la BER ≈ 2 % pese a Eb/N0 = 24 dB. | fig08, fig09 (fila R1) |
| _(completar)_ | Diagnóstico | La SNR a la entrada del discriminador es 4.4 dB (ruido en 1 MHz), por debajo del umbral de FM (~10 dB): clicks. | Referencia [4] |
| _(completar)_ | Receptor v2 | Se agrega un filtro FIR de canal (corte 20 kHz, 241 taps). Sin errores en A–D. | fig09 (fila R2), fig11 |
| _(completar)_ | Alineación | El filtro introduce 120 muestras de retardo. Skip Head = 120 mod 100 = 20; referencia Tx retardada 1 bit; Delay de 120 muestras en R1 para comparar con igual latencia. | Prueba A con BER = 0 |
| _(completar)_ | Barridos | BER vs noise_voltage (R2 falla desde σ ≈ 1.5) y BER vs Δf con R1. | data/tablas_de_pruebas |
| 7 nov 2026 | Verificación GNU Radio | GRC ejecutado en GNU Radio 3.10.12 (radioconda). Con un bloque Selector, cambiar de R2 a R1 en ejecución daba BER ≈ 0.62 (flujos desalineados). Se reemplazó por una mezcla ponderada (Multiply Const 1−receptor / receptor + Add). Resultados: A y B sin errores; C: R1 0.022–0.033, R2 0; D: R1 0.155–0.169, R2 0. | Capturas del GRC |
| _(completar)_ | Entrega | Informe IEEE, blog, README y video. | docs/, blog/ |

## Pruebas fallidas relevantes

- Comparar sin retardar la referencia Tx (D_b = 0) dio una BER aparente de ≈ 0.6 en la prueba A, aunque los bits recuperados eran correctos: estaban desplazados un bit por el retardo del filtro.
- Con h = 1 (Δf = 5 kHz) y sin filtro de canal, la BER en la prueba C sube a 4 %.

## Pendientes antes de entregar

- [x] GRC ejecutado en GNU Radio y pruebas A–D verificadas.
- [x] Capturas de GNU Radio de las pruebas A–D con R1 y R2 (58 imágenes) en `figures/pantallazos_GNU_radio/`; BER medidas: A 0/0, B 0/0, C 0.024/0, D 0.151/0.
- [x] `ajuste_muestreo = 0` confirmado: BER = 0 en la prueba A.
- [x] Integrantes y grupo (E1) agregados en informe, blog, README, guion y ficha.
- [ ] Grabar y enlazar el video.
