import yfinance as yf
import pandas as pd
import plotly.express as px
import streamlit as st

# Tickers
tickers_panel_lider = [
    'ALUA.BA', 'BBAR.BA', 'BMA.BA', 'BYMA.BA', 'CEPU.BA', 'COME.BA',
    'CRES.BA', 'CVH.BA', 'EDN.BA', 'GGAL.BA', 'HARG.BA', 'LOMA.BA',
    'MIRG.BA', 'METR.BA', 'PAMP.BA', 'SUPV.BA', 'TECO2.BA', 'TGNO4.BA', 'TGSU2.BA',
    'TRAN.BA', 'TXAR.BA', 'VALO.BA', 'YPFD.BA'
]

tickers_panel_general = [
    'AGRO.BA', 'AUSO.BA', 'BHIP.BA', 'BOLT.BA', 'BPAT.BA', 'CADO.BA', 'CAPX.BA', 'CARC.BA', 'CECO2.BA',
    'CELU.BA', 'CGPA2.BA', 'CTIO.BA', 'DGCE.BA', 'DGCU2.BA', 'DOME.BA', 'DYCA.BA', 'FERR.BA', 'FIPL.BA',
    'GARO.BA', 'GBAN.BA', 'GCDI.BA', 'GCLA.BA', 'GRIM.BA', 'HAVA.BA', 'INTR.BA', 'INVJ.BA', 'IRSA.BA',
    'LEDE.BA', 'LONG.BA', 'MOLA.BA', 'MOLI.BA', 'MORI.BA', 'OEST.BA', 'PATA.BA', 'RIGO.BA',
    'ROSE.BA', 'SAMI.BA', 'SEMI.BA'
]

# Función para obtener datos (sin cambios)
def get_data(tickers, period='1d', value_metric='Capitalización'):
    # Tu código para obtener datos aquí...

# Configuración de la aplicación Streamlit (sin cambios)
st.title('Análisis de Mercado Bursátil Argentino - https://x.com/iterAR_eco')
st.sidebar.header('Parámetros de Selección')

# Parámetros de selección en la barra lateral (sin cambios)
panel = st.sidebar.selectbox('Seleccionar Panel', ('todos', 'panel_lider', 'panel_general'))
period = st.sidebar.selectbox('Seleccionar Periodo', ('diario', 'semana en curso', 'mes en curso', 'año en curso'))
value_metric = st.sidebar.selectbox('Métrica de Valor', ('Capitalización', 'Volumen'))
range_colors = st.sidebar.slider('Rango de Colores para Rendimiento', min_value=1, max_value=10, value=3)

# Mapear períodos a códigos (sin cambios)
period_mapping = {
    'diario': '1d',
    'semana en curso': '1wk',
    'mes en curso': '1mo',
    'año en curso': '1y'
}

# Seleccionar tickers según el panel (sin cambios)
if panel == 'panel_lider':
    tickers = tickers_panel_lider
elif panel == 'panel_general':
    tickers = tickers_panel_general
elif panel == 'todos':
    tickers = tickers_panel_lider + tickers_panel_general
else:
    st.error("Panel no soportado")

# Obtener datos
resultados = get_data(tickers, period_mapping.get(period, '1d'), value_metric)

# Filtrar datos válidos (remover NaNs)
resultados = resultados.dropna(subset=['Value', 'Rendimiento'])
resultados = resultados[resultados['Value'] > 0]

# Verificar si hay datos para mostrar
if not resultados.empty:
    # Crear el gráfico de treemap con etiquetas personalizadas y colores brillantes
    fig = px.treemap(resultados,
                     path=['Panel', 'Ticker'],
                     values='Value',
                     color='Rendimiento',
                     color_continuous_scale=px.colors.sequential.Viridis,  # Escala de colores brillante
                     color_continuous_midpoint=0,
                     range_color=[-range_colors, range_colors],
                     title=f"Panel general: {value_metric} y Rendimiento ({period})")

    # Ajustar el tamaño del gráfico
    fig.update_layout(width=2500, height=800)

    # Personalizar la información en las etiquetas
    fig.update_traces(textinfo="label+text+value",
                      texttemplate="<b>%{label}</b><br><b>%{customdata[0]:.2f}%</b>",
                      textfont=dict(size=14, family="Arial Black"))  # Texto más grueso

    # Mostrar el gráfico en Streamlit
    st.plotly_chart(fig)
else:
    st.warning("No hay datos válidos para mostrar.")
