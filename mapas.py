import yfinance as yf
import pandas as pd
import plotly.express as px
import streamlit as st

# Función para obtener datos
def get_last_data(tickers, period='5d'):
    data = []
    for ticker in tickers:
        stock = yf.Ticker(ticker)
        hist = stock.history(period=period)
        if len(hist) >= 2:
            # Obtener el precio de cierre y volumen del último día
            last_close = hist['Close'].iloc[-1]
            last_volume = hist['Volume'].iloc[-1]
            # Obtener el precio de cierre del día anterior
            previous_close = hist['Close'].iloc[-2]
            # Calcular el rendimiento diario
            daily_return = (last_close - previous_close) / previous_close * 100
            data.append({
                'Ticker': ticker,
                'Volumen': last_volume,
                'Rendimiento Diario': daily_return
            })
        else:
            data.append({
                'Ticker': ticker,
                'Volumen': None,
                'Rendimiento Diario': None
            })
    return pd.DataFrame(data)

# Función para depurar los datos
def debug_data(df):
    st.write("DataFrame:")
    st.write(df.head())
    st.write("DataFrame Info:")
    st.write(df.info())
    st.write("Valores Nulos:")
    st.write(df.isnull().sum())

# Selección de tickers y otras opciones
tickers_panel_general = [
    'ALUA.BA', 'BBAR.BA', 'BMA.BA', 'BYMA.BA', 'CEPU.BA', 'COME.BA',
    'CRES.BA', 'CVH.BA', 'EDN.BA', 'GGAL.BA', 'HARG.BA', 'LOMA.BA',
    'MIRG.BA', 'PAMP.BA', 'SUPV.BA', 'TECO2.BA', 'TGNO4.BA', 'TGSU2.BA',
    'TRAN.BA', 'TXAR.BA', 'VALO.BA', 'YPFD.BA'
    # Añadir todos los tickers restantes aquí
]

tickers_panel_lider = [
    'AGRO.BA', 'AUSO.BA', 'BHIP.BA', 'BOLT.BA', 'BPAT.BA', 'CADO.BA', 'CAPX.BA', 'CARC.BA', 'CECO2.BA',
    'CELU.BA', 'CGPA2.BA', 'CTIO.BA', 'DGCE.BA', 'DGCU2.BA', 'DOME.BA', 'DYCA.BA', 'FERR.BA', 'FIPL.BA',
    'GARO.BA', 'GBAN.BA', 'GCDI.BA', 'GCLA.BA', 'GRIM.BA', 'HAVA.BA', 'INTR.BA', 'INVJ.BA', 'IRSA.BA',
    'LEDE.BA', 'LONG.BA', 'METR.BA', 'MOLA.BA', 'MOLI.BA', 'MORI.BA', 'OEST.BA', 'PATA.BA', 'RIGO.BA',
    'ROSE.BA', 'SAMI.BA', 'SEMI.BA'
    # Añadir todos los tickers restantes aquí
]

# Streamlit UI
st.title("Análisis de Acciones")

panel_option = st.selectbox('Seleccione el panel', ['Panel General', 'Panel Líder', 'Todos'])
metric_option = st.selectbox('Seleccione la métrica', ['Volumen', 'Volumen por Precio'])
performance_option = st.selectbox('Seleccione el rendimiento', ['Diario', 'Semanal', 'Mensual', 'Anual'])

# Determinar tickers y periodo
if panel_option == 'Panel General':
    tickers = tickers_panel_general
elif panel_option == 'Panel Líder':
    tickers = tickers_panel_lider
else:
    tickers = tickers_panel_general + tickers_panel_lider

# Obtener datos
if performance_option == 'Diario':
    period = '5d'
elif performance_option == 'Semanal':
    period = '1wk'
elif performance_option == 'Mensual':
    period = '1mo'
else:
    period = '1y'

resultados = get_last_data(tickers, period)

# Verificar si hay datos faltantes
debug_data(resultados)

# Calcular 'Volumen por Precio' si se selecciona
if metric_option == 'Volumen por Precio':
    resultados['Volumen'] = resultados['Volumen'] * resultados['Rendimiento Diario'].fillna(0)

# Crear el gráfico de treemap
fig = px.treemap(resultados,
                 path=['Ticker'],
                 values='Volumen',
                 color='Rendimiento Diario',
                 color_continuous_scale='RdYlGn',
                 color_continuous_midpoint=0,
                 range_color=[-10, 10],
                 title="Panel general: Volumen Operado y Rendimiento Diario")

# Actualizar las etiquetas para que coincidan con el DataFrame
fig.update_traces(textinfo="label+text+value",
                  texttemplate="<b>%{label}</b><br><b>%{customdata[0]:.2f}%</b>")

# Añadir la columna 'Rendimiento Diario' a customdata
fig.update_traces(customdata=resultados[['Rendimiento Diario']])

# Ajustar el tamaño del gráfico
fig.update_layout(width=2000, height=800)

# Mostrar el gráfico
st.plotly_chart(fig)

# Mostrar el DataFrame final
st.write(resultados)

