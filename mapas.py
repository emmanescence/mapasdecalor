import yfinance as yf
import pandas as pd
import plotly.express as px
import streamlit as st

# Función para obtener datos
def get_last_data(tickers, period='5d', panel_name=''):
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
                'Rendimiento Diario': daily_return,
                'Panel': panel_name
            })
        else:
            data.append({
                'Ticker': ticker,
                'Volumen': None,
                'Rendimiento Diario': None,
                'Panel': panel_name
            })
    return pd.DataFrame(data)

# Selección de tickers y otras opciones
tickers_panel_general = [
    'ALUA.BA', 'BBAR.BA', 'BMA.BA', 'BYMA.BA', 'CEPU.BA', 'COME.BA',
    # Añadir todos los tickers restantes aquí
]

tickers_panel_lider = [
    'AGRO.BA', 'AUSO.BA', 'BHIP.BA', 'BOLT.BA', 'BPAT.BA', 'CADO.BA', 
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
    panel_name = 'Panel General'
    resultados = get_last_data(tickers, '5d', panel_name)
elif panel_option == 'Panel Líder':
    tickers = tickers_panel_lider
    panel_name = 'Panel Líder'
    resultados = get_last_data(tickers, '5d', panel_name)
else:
    # Obtener datos para ambos paneles
    data_general = get_last_data(tickers_panel_general, '5d', 'Panel General')
    data_lider = get_last_data(tickers_panel_lider, '5d', 'Panel Líder')

    # Filtrar datos válidos después de la combinación
    data_general = data_general.dropna(subset=['Volumen', 'Rendimiento Diario'])
    data_general = data_general[data_general['Volumen'] > 0]
    
    data_lider = data_lider.dropna(subset=['Volumen', 'Rendimiento Diario'])
    data_lider = data_lider[data_lider['Volumen'] > 0]

    # Mostrar los DataFrames finales antes de graficar para depuración
    st.write("Datos Panel General:", data_general)
    st.write("Datos Panel Líder:", data_lider)

    # Crear el gráfico para el panel general
    fig_general = px.treemap(data_general,
                            path=['Ticker'],
                            values='Volumen',
                            color='Rendimiento Diario',
                            color_continuous_scale='RdYlGn',
                            color_continuous_midpoint=0,
                            range_color=[-10, 10],
                            title="Panel General: Volumen Operado y Rendimiento Diario",
                            labels={'Rendimiento Diario': 'Rendimiento'})
    
    etiquetas_general = data_general.apply(lambda row: f"{row['Ticker']}: {row['Rendimiento Diario']:.2f}%", axis=1)
    fig_general.update_traces(
        text=etiquetas_general,
        textinfo="label+text"
    )
    fig_general.update_layout(width=1000, height=500)
    
    # Crear el gráfico para el panel líder
    fig_lider = px.treemap(data_lider,
                          path=['Ticker'],
                          values='Volumen',
                          color='Rendimiento Diario',
                          color_continuous_scale='RdYlGn',
                          color_continuous_midpoint=0,
                          range_color=[-10, 10],
                          title="Panel Líder: Volumen Operado y Rendimiento Diario",
                          labels={'Rendimiento Diario': 'Rendimiento'})
    
    etiquetas_lider = data_lider.apply(lambda row: f"{row['Ticker']}: {row['Rendimiento Diario']:.2f}%", axis=1)
    fig_lider.update_traces(
        text=etiquetas_lider,
        textinfo="label+text"
    )
    fig_lider.update_layout(width=1000, height=500)

    # Mostrar ambos gráficos
    st.plotly_chart(fig_general)
    st.plotly_chart(fig_lider)
    
# Mostrar el DataFrame final si se selecciona "Panel General" o "Panel Líder"
if panel_option in ['Panel General', 'Panel Líder']:
    st.write("Datos finales:", resultados)

