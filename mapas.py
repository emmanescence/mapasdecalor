import yfinance as yf
import pandas as pd
import plotly.express as px
import streamlit as st

# Título de la aplicación en Streamlit
st.title("Panel General: Volumen Operado y Rendimiento Diario")

# Lista de tickers
tickers_panel_lider = [
    'ALUA.BA', 'BBAR.BA', 'BMA.BA', 'BYMA.BA', 'CEPU.BA', 'COME.BA',
    'CRES.BA', 'CVH.BA', 'EDN.BA', 'GGAL.BA', 'HARG.BA', 'LOMA.BA',
    'MIRG.BA', 'PAMP.BA', 'SUPV.BA', 'TECO2.BA', 'TGNO4.BA', 'TGSU2.BA',
    'TRAN.BA', 'TXAR.BA', 'VALO.BA', 'YPFD.BA'
]

# Función para obtener datos
def get_last_data(tickers):
    data = []
    for ticker in tickers:
        stock = yf.Ticker(ticker)
        hist = stock.history(period='5d')  # Obtener datos de los últimos 5 días
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

# Obtener datos
resultados = get_last_data(tickers_panel_lider)

# Crear el gráfico de treemap con etiquetas personalizadas y escala de colores ajustada
fig = px.treemap(resultados,
                 path=['Ticker'],
                 values='Volumen',
                 color='Rendimiento Diario',
                 color_continuous_scale=[(0, 'red'), (0.5, 'white'), (1, 'darkgreen')],
                 color_continuous_midpoint=0,  # Punto medio de la escala en 0%
                 range_color=[-3, 3],  # Rango de colores desde -3% a +3%
                 title="Panel general: Volumen Operado y Rendimiento Diario")

# Personalizar la información en las etiquetas con negrita
fig.update_traces(textinfo="label+text+value",
                  texttemplate="<b>%{label}</b><br><b>%{customdata[0]:.2f}%</b>")

# Añadir la columna 'Rendimiento Diario' a customdata
fig.update_traces(customdata=resultados[['Rendimiento Diario']])

# Mostrar el gráfico en Streamlit
st.plotly_chart(fig)
