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
                'Rendimiento Diario': daily_return,
                'Panel': panel_name  # Agregar nombre del panel
            })
        else:
            data.append({
                'Ticker': ticker,
                'Volumen': None,
                'Rendimiento Diario': None,
                'Panel': panel_name  # Agregar nombre del panel
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
elif panel_option == 'Panel Líder':
    tickers = tickers_panel_lider
    panel_name = 'Panel Líder'
else:
    # Obtener datos para ambos paneles sin eliminar duplicados
    data_general = get_last_data(tickers_panel_general, '5d', 'Panel General').copy()
    data_lider = get_last_data(tickers_panel_lider, '5d', 'Panel Líder').copy()
    
    # Concatenar los DataFrames pero no eliminar duplicados
    resultados = pd.concat([data_general, data_lider], ignore_index=True)
    panel_name = 'Todos'

# Obtener datos si no estamos en 'Todos'
if panel_option != 'Todos':
    if performance_option == 'Diario':
        period = '5d'
    elif performance_option == 'Semanal':
        period = '1wk'
    elif performance_option == 'Mensual':
        period = '1mo'
    else:
        period = '1y'

    resultados = get_last_data(tickers, period, panel_name)

# Filtrar datos inválidos después de la combinación
resultados = resultados.dropna(subset=['Volumen', 'Rendimiento Diario'])
resultados = resultados[resultados['Volumen'] > 0]

# Crear una columna con las etiquetas que queremos mostrar en el gráfico
resultados['Etiqueta'] = resultados.apply(lambda row: f"{row['Ticker']}: {row['Rendimiento Diario']:.2f}%", axis=1)

# Verificar si hay datos para graficar
if resultados.empty:
    st.write("No hay datos suficientes para mostrar el gráfico.")
else:
    # Calcular 'Volumen por Precio' si se selecciona
    if metric_option == 'Volumen por Precio':
        resultados['Volumen'] = resultados['Volumen'] * resultados['Rendimiento Diario'].fillna(0)

    # Mostrar el DataFrame final antes de graficar para depuración
    st.write("Datos a graficar:", resultados)

    # Depuración: Mostrar valores de rendimiento diario para los tickers combinados
    for idx, row in resultados.iterrows():
        st.write(f"Ticker: {row['Ticker']}, Rendimiento Diario: {row['Rendimiento Diario']}")

    # Crear el gráfico de treemap
    fig = px.treemap(resultados,
                     path=['Panel', 'Ticker'],  # Agregar 'Panel' para mantener la unicidad
                     values='Volumen',
                     color='Rendimiento Diario',
                     color_continuous_scale='RdYlGn',
                     color_continuous_midpoint=0,
                     range_color=[-10, 10],
                     title="Panel general: Volumen Operado y Rendimiento Diario")

    # Actualizar las etiquetas para que coincidan con el DataFrame
    fig.update_traces(textinfo="label+text+value",
                      text=resultados['Etiqueta'])  # Usar la columna 'Etiqueta'

    # Ajustar el tamaño del gráfico
    fig.update_layout(width=2000, height=800)

    # Mostrar el gráfico
    st.plotly_chart(fig)

# Mostrar el DataFrame final al final
st.write("Datos finales:", resultados)


