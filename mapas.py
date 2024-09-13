import yfinance as yf
import pandas as pd
import streamlit as st
import plotly.express as px

# Definir los paneles de tickers
tickers_panel_general = [ 
    'ALUA.BA', 'BBAR.BA', 'BMA.BA', 'BYMA.BA', 'CEPU.BA', 'COME.BA',
    'CRES.BA', 'CVH.BA', 'EDN.BA', 'GGAL.BA', 'HARG.BA', 'LOMA.BA',
    'MIRG.BA', 'PAMP.BA', 'SUPV.BA', 'TECO2.BA', 'TGNO4.BA', 'TGSU2.BA',
    'TRAN.BA', 'TXAR.BA', 'VALO.BA', 'YPFD.BA'
]

tickers_panel_lider = [
    'AGRO.BA', 'AUSO.BA', 'BHIP.BA', 'BOLT.BA', 'BPAT.BA', 'CADO.BA', 'CAPX.BA', 'CARC.BA', 'CECO2.BA',
    'CELU.BA', 'CGPA2.BA', 'CTIO.BA', 'DGCE.BA', 'DGCU2.BA', 'DOME.BA', 'DYCA.BA', 'FERR.BA', 'FIPL.BA',
    'GARO.BA', 'GBAN.BA', 'GCDI.BA', 'GCLA.BA', 'GRIM.BA', 'HAVA.BA', 'INTR.BA', 'INVJ.BA', 'IRSA.BA',
    'LEDE.BA', 'LONG.BA', 'METR.BA', 'MOLA.BA', 'MOLI.BA', 'MORI.BA', 'OEST.BA', 'PATA.BA', 'RIGO.BA',
    'ROSE.BA', 'SAMI.BA', 'SEMI.BA'
]

# Función para obtener los datos de precios y volumen
def get_data(tickers, period):
    data = []
    for ticker in tickers:
        stock = yf.Ticker(ticker)
        hist = stock.history(period=period)  # Obtener datos según el periodo seleccionado
        if len(hist) >= 2:
            # Último día de cierre y volumen
            last_close = hist['Close'].iloc[-1]
            last_volume = hist['Volume'].iloc[-1]

            # Cierre del día anterior
            previous_close = hist['Close'].iloc[0] if period == '1d' else hist['Close'].iloc[-2]

            # Calcular el rendimiento
            daily_return = (last_close - previous_close) / previous_close * 100

            data.append({
                'Ticker': ticker,
                'Volumen': last_volume,
                'Volumen por Precio': last_volume * last_close,  # Volumen por precio
                'Rendimiento': round(daily_return, 2)  # Redondeo a 2 decimales
            })
    return pd.DataFrame(data)

# Crear la aplicación en Streamlit
st.title('Análisis de Tickers - Panel Líder y General')

# Selección de panel
panel = st.selectbox(
    "Seleccione el panel de tickers:",
    ['Panel General', 'Panel Líder', 'Todos los Tickers']
)

if panel == 'Panel General':
    tickers = tickers_panel_general
elif panel == 'Panel Líder':
    tickers = tickers_panel_lider
else:
    tickers = tickers_panel_general + tickers_panel_lider

# Selección de tipo de visualización
visualizacion = st.radio(
    "Seleccione el tipo de datos para visualizar:",
    ['Volumen', 'Volumen por Precio']
)

# Selección del periodo de rendimiento
periodo = st.selectbox(
    "Seleccione el periodo para calcular el rendimiento:",
    ['1d', '5d', '1mo', '1y'],
    format_func=lambda p: {'1d': 'Diario', '5d': 'Semanal', '1mo': 'Mensual', '1y': 'Anual'}[p]
)

# Obtener los datos
resultados = get_data(tickers, periodo)

# Mostrar los resultados para inspeccionar las columnas y sus valores
st.write(resultados)  # Verifica que las columnas existen y tienen los valores correctos

# Definir el campo de valores a visualizar
if visualizacion == 'Volumen':
    valor = 'Volumen'
else:
    valor = 'Volumen por Precio'

# Crear el gráfico de treemap
fig = px.treemap(resultados,
                 path=['Ticker'],
                 values=valor,  # Asegúrate de que esta columna existe
                 color='Rendimiento',
                 color_continuous_scale=[(0, 'red'), (0.5, 'white'), (1, 'green')],
                 color_continuous_midpoint=0,
                 range_color=[-3, 3],
                 title=f"Panel {panel}: {valor} y Rendimiento {periodo}"
)

# Mostrar el gráfico en la app
st.plotly_chart(fig)

# Mostrar el DataFrame resultante
st.dataframe(resultados)
