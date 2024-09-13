import yfinance as yf
import pandas as pd
import plotly.express as px
import streamlit as st

# Listas de tickers
tickers_panel_general = [ 
    'ALUA.BA', 'BBAR.BA', 'BMA.BA', 'BYMA.BA', 'CEPU.BA', 'COME.BA',
    'CRES.BA', 'CVH.BA', 'EDN.BA', 'GGAL.BA', 'HARG.BA', 'LOMA.BA',
    'MIRG.BA', 'PAMP.BA', 'SUPV.BA', 'TECO2.BA', 'TGNO4.BA', 'TGSU2.BA',
    'TRAN.BA', 'TXAR.BA', 'VALO.BA', 'YPFD.BA',
    'AGRO.BA', 'AUSO.BA', 'BHIP.BA', 'BOLT.BA', 'BPAT.BA', 'CADO.BA', 'CAPX.BA', 'CARC.BA', 'CECO2.BA',
    'CELU.BA', 'CGPA2.BA', 'CTIO.BA', 'DGCE.BA', 'DGCU2.BA', 'DOME.BA', 'DYCA.BA', 'FERR.BA', 'FIPL.BA',
    'GARO.BA', 'GBAN.BA', 'GCDI.BA', 'GCLA.BA', 'GRIM.BA', 'HAVA.BA', 'INTR.BA', 'INVJ.BA', 'IRSA.BA',
    'LEDE.BA', 'LONG.BA', 'METR.BA', 'MOLA.BA', 'MOLI.BA', 'MORI.BA', 'OEST.BA', 'PATA.BA', 'RIGO.BA',
    'ROSE.BA', 'SAMI.BA', 'SEMI.BA'
]

tickers_panel_lider = [
    'AGRO.BA', 'AUSO.BA', 'BHIP.BA', 'BOLT.BA', 'BPAT.BA', 'CADO.BA', 'CAPX.BA', 'CARC.BA', 'CECO2.BA',
    'CELU.BA', 'CGPA2.BA', 'CTIO.BA', 'DGCE.BA', 'DGCU2.BA', 'DOME.BA', 'DYCA.BA', 'FERR.BA', 'FIPL.BA',
    'GARO.BA', 'GBAN.BA', 'GCDI.BA', 'GCLA.BA', 'GRIM.BA', 'HAVA.BA', 'INTR.BA', 'INVJ.BA', 'IRSA.BA',
    'LEDE.BA', 'LONG.BA', 'METR.BA', 'MOLA.BA', 'MOLI.BA', 'MORI.BA', 'OEST.BA', 'PATA.BA', 'RIGO.BA',
    'ROSE.BA', 'SAMI.BA', 'SEMI.BA'
]

# Función para obtener datos
def get_last_data(tickers, period='5d'):
    data = []
    for ticker in tickers:
        stock = yf.Ticker(ticker)
        hist = stock.history(period=period)
        if len(hist) >= 2:
            last_close = hist['Close'].iloc[-1]
            last_volume = hist['Volume'].iloc[-1]
            previous_close = hist['Close'].iloc[-2]
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

# Streamlit UI
st.title('Análisis Financiero')
option = st.selectbox('Seleccione el panel', ['Panel General', 'Panel Líder', 'Todos'])

if option == 'Panel General':
    tickers = tickers_panel_general
elif option == 'Panel Líder':
    tickers = tickers_panel_lider
else:
    tickers = tickers_panel_general + tickers_panel_lider

value_option = st.selectbox('Seleccione el tipo de valor', ['Volumen', 'Volumen por Precio'])
performance_option = st.selectbox('Seleccione el tipo de rendimiento', ['Diario', 'Semanal', 'Mensual', 'Anual'])

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

# Procesar datos según el valor seleccionado
if value_option == 'Volumen':
    resultados['Valor'] = resultados['Volumen']
else:
    resultados['Valor'] = resultados['Volumen'] * (resultados['Rendimiento Diario'] / 100 + 1)

# Crear el gráfico de treemap
fig = px.treemap(resultados,
                 path=['Ticker'],
                 values='Valor',
                 color='Rendimiento Diario',
                 color_continuous_scale=px.colors.sequential.Viridis,
                 color_continuous_midpoint=0,
                 range_color=[-10, 10],
                 title="Panel General: Valor y Rendimiento Diario")

# Añadir la columna 'Rendimiento Diario' a customdata
fig.update_traces(customdata=resultados[['Rendimiento Diario']],
                  texttemplate="<b>%{label}</b><br><b>%{customdata[0]:.2f}%</b>",
                  textinfo="label+text")

# Ajustar el tamaño del gráfico
fig.update_layout(width=2000, height=800)

# Mostrar el gráfico en Streamlit
st.plotly_chart(fig)

# Mostrar el DataFrame al final
st.write(resultados)
