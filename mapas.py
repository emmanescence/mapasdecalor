import streamlit as st
import yfinance as yf
import pandas as pd
import plotly.express as px

# Lista de tickers
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
            if period == 'diario':
                period_data = hist.tail(2)
            elif period == 'semanal':
                period_data = hist.resample('W').last().tail(2)
            elif period == 'mensual':
                period_data = hist.resample('M').last().tail(2)
            elif period == 'anual':
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
                value = capi if value_metric == 'Volumen x precio' else last_volume

                data.append({
                    'Ticker': ticker,
                    'Volumen': last_volume,
                    'Rendimiento': performance,
                    'Capitalización': capi,
                    'Value': value
                })
            else:
                data.append({
                    'Ticker': ticker,
                    'Volumen': None,
                    'Rendimiento': None,
                    'Capitalización': None,
                    'Value': None
                })
        else:
            data.append({
                'Ticker': ticker,
                'Volumen': None,
                'Rendimiento': None,
                'Capitalización': None,
                'Value': None
            })
    return pd.DataFrame(data)

# Aplicación Streamlit
def main():
    st.title("Análisis Financiero con Streamlit")

    # Selección del panel
    panel = st.selectbox(
        "Selecciona el panel:",
        ['Panel General', 'Panel Líder', 'Todos']
    )

    # Selección del período
    period = st.selectbox(
        "Selecciona el período de rendimiento:",
        ['diario', 'semanal', 'mensual', 'anual']
    )

    # Selección de la métrica
    value_metric = st.selectbox(
        "Selecciona la métrica para el valor en el gráfico:",
        ['Volumen x precio', 'Volumen']
    )

    # Selección del rango de colores
    color_range = st.selectbox(
        "Selecciona el rango de colores para el rendimiento:",
        ['-10 a 10', '-5 a 5', '-3 a 3', '-1 a 1']
    )

    # Mapeo de los rangos de colores a valores
    color_ranges = {
        '-10 a 10': [-10, 10],
        '-5 a 5': [-5, 5],
        '-3 a 3': [-3, 3],
        '-1 a 1': [-1, 1]
    }
    
    selected_range = color_ranges[color_range]

    # Determinar los tickers a usar según el panel seleccionado
    if panel == 'Panel General':
        tickers = tickers_panel_general
    elif panel == 'Panel Líder':
        tickers = tickers_panel_lider
    else:
        tickers = tickers_panel_lider + tickers_panel_general  # Todos los tickers

    # Obtener datos
    resultados = get_data(tickers, period, value_metric)

    # Crear el gráfico de treemap con etiquetas personalizadas y escala de colores ajustada
    fig = px.treemap(resultados,
                     path=['Ticker'],
                     values='Value',
                     color='Rendimiento',
                     color_continuous_scale=[(0, 'red'), (0.5, 'white'), (1, 'darkgreen')],
                     color_continuous_midpoint=0,  # Punto medio de la escala en 0%
                     range_color=selected_range,  # Rango de colores según selección
                     title=f"Panel {panel}: {value_metric} y Rendimiento ({period})")

    # Ajustar el tamaño del gráfico
    fig.update_layout(width=1500, height=800)  # Puedes ajustar estos valores según sea necesario

    # Personalizar la información en las etiquetas con negrita
    fig.update_traces(textinfo="label+text+value",
                      texttemplate="<b>%{label}</b><br><b>%{customdata[0]:.2f}%</b>")

    # Añadir la columna 'Rendimiento Diario' a customdata
    fig.update_traces(customdata=resultados[['Rendimiento Diario']])

    # Mostrar el gráfico
    st.plotly_chart(fig)

if __name__ == "__main__":
    main()

