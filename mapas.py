import yfinance as yf
import pandas as pd
import plotly.express as px
import streamlit as st

# Tickers
tickers_panel_lider = [
    'ALUA.BA', 'BBAR.BA', 'BMA.BA', 'BYMA.BA', 'CEPU.BA', 'COME.BA',
    'CRES.BA', 'CVH.BA', 'EDN.BA', 'GGAL.BA', 'HARG.BA', 'LOMA.BA',
    'MIRG.BA', 'PAMP.BA', 'SUPV.BA', 'TECO2.BA', 'TGNO4.BA', 'TGSU2.BA',
    'TRAN.BA', 'TXAR.BA', 'VALO.BA', 'YPFD.BA'
]

tickers_panel_general = [
    'AGRO.BA', 'AUSO.BA', 'BHIP.BA', 'BOLT.BA', 'BPAT.BA', 'CADO.BA', 'CAPX.BA', 'CARC.BA', 'CECO2.BA',
    'CELU.BA', 'CGPA2.BA', 'CTIO.BA', 'DGCE.BA', 'DGCU2.BA', 'DOME.BA', 'DYCA.BA', 'FERR.BA', 'FIPL.BA',
    'GARO.BA', 'GBAN.BA', 'GCDI.BA', 'GCLA.BA', 'GRIM.BA', 'HAVA.BA', 'INTR.BA', 'INVJ.BA', 'IRSA.BA',
    'LEDE.BA', 'LONG.BA', 'METR.BA', 'MOLA.BA', 'MOLI.BA', 'MORI.BA', 'OEST.BA', 'PATA.BA', 'RIGO.BA',
    'ROSE.BA', 'SAMI.BA', 'SEMI.BA'
]

# Función para obtener datos
def get_data(tickers, period='1d', value_metric='Capitalización'):
    data = []
    for ticker in tickers:
        stock = yf.Ticker(ticker)
        hist = stock.history(period='1y')  # Obtener datos del último año
        if len(hist) > 1:
            # Determinar el periodo para el cálculo del rendimiento
            if period == '1d':
                period_data = hist.tail(2)
            elif period == '1wk':
                period_data = hist.resample('W').last().tail(2)
            elif period == '1mo':
                period_data = hist.resample('M').last().tail(2)
            elif period == '1y':
                period_data = hist.resample('A').last().tail(2)
            else:
                raise ValueError("Periodo no soportado")

            if len(period_data) >= 2:
                # Obtener precios de cierre
                last_close = period_data['Close'].iloc[-1]
                previous_close = period_data['Close'].iloc[-2]

                # Calcular el rendimiento
                performance = (last_close - previous_close) / previous_close * 100

                # Obtener el volumen
                last_volume = period_data['Volume'].iloc[-1]

                # Calcular la capitalización
                capi = last_volume * last_close

                # Determinar el valor a mostrar según la métrica seleccionada
                value = capi if value_metric == 'Capitalización' else last_volume

                # Agregar panel como 'Panel Líder' o 'Panel General'
                panel_type = 'Panel Líder' if ticker in tickers_panel_lider else 'Panel General'

                data.append({
                    'Ticker': ticker,
                    'Panel': panel_type,
                    'Volumen': last_volume,
                    'Rendimiento': performance,
                    'Capitalización': capi,
                    'Value': value
                })
            else:
                continue  # Omitir si no hay suficientes datos para calcular el rendimiento
        else:
            continue  # Omitir si no hay suficientes datos históricos
    return pd.DataFrame(data)

# Configuración de la aplicación Streamlit
st.title('Análisis de Mercado Bursátil Argentino')
st.sidebar.header('Parámetros de Selección')

# Parámetros de selección en la barra lateral
panel = st.sidebar.selectbox('Seleccionar Panel', ('todos', 'panel_lider', 'panel_general'))
period = st.sidebar.selectbox('Seleccionar Periodo', ('1d', '1wk', '1mo', '1y'))
value_metric = st.sidebar.selectbox('Métrica de Valor', ('Capitalización', 'Volumen'))
range_colors = st.sidebar.slider('Rango de Colores para Rendimiento', min_value=1, max_value=10, value=3)

# Seleccionar tickers según el panel
if panel == 'panel_lider':
    tickers = tickers_panel_lider
elif panel == 'panel_general':
    tickers = tickers_panel_general
elif panel == 'todos':
    tickers = tickers_panel_lider + tickers_panel_general
else:
    st.error("Panel no soportado")

# Obtener datos
resultados = get_data(tickers, period, value_metric)

# Filtrar datos válidos (remover NaNs)
resultados = resultados.dropna(subset=['Value', 'Rendimiento'])
resultados = resultados[resultados['Value'] > 0]

# Verificar si hay datos para mostrar
if not resultados.empty:
    # Crear el gráfico de treemap con etiquetas personalizadas y escala de colores ajustada
    fig = px.treemap(resultados,
                     path=['Panel', 'Ticker'],  # Incluir el nivel 'Panel' para el agrupamiento
                     values='Value',
                     color='Rendimiento',
                     color_continuous_scale=[(0, 'red'), (0.5, 'white'), (1, 'darkgreen')],
                     color_continuous_midpoint=0,  # Punto medio de la escala en 0%
                     range_color=[-range_colors, range_colors],  # Ajusta según el rango de rendimiento esperado
                     title=f"Panel general: {value_metric} y Rendimiento ({'diario' if period == '1d' else 'semanal' if period == '1wk' else 'mensual' if period == '1mo' else 'anual'})")

    # Ajustar el tamaño del gráfico
    fig.update_layout(width=1500, height=800)  # Puedes ajustar estos valores según sea necesario

    # Mostrar el gráfico en Streamlit
    st.plotly_chart(fig)
else:
    st.warning("No hay datos válidos para mostrar.")

