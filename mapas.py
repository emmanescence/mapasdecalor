import yfinance as yf
import pandas as pd
import plotly.express as px
import streamlit as st

# Definición de tickers
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
def get_data(tickers, period):
    data = []
    for ticker in tickers:
        try:
            stock = yf.Ticker(ticker)
            hist = stock.history(period='1y')  # Obtener datos de un año para cálculos

            if period == '1d':
                # Para el día actual, usa el último cierre disponible
                hist = hist.tail(2)  # Usa las últimas dos fechas para calcular el rendimiento diario

            if len(hist) >= 2:
                last_close = hist['Close'].iloc[-1]
                last_volume = hist['Volume'].iloc[-1]
                previous_close = hist['Close'].iloc[-2]
                daily_return = (last_close - previous_close) / previous_close * 100

                data.append({
                    'Ticker': ticker,
                    'Volumen': last_volume,
                    'Volumen por Precio': last_volume * last_close,
                    'Rendimiento': round(daily_return, 2)
                })
            else:
                print(f"No hay suficientes datos para el ticker: {ticker}")

        except Exception as e:
            print(f"Error al obtener datos para el ticker {ticker}: {e}")

    if data:
        return pd.DataFrame(data)
    else:
        return pd.DataFrame()

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

# Selección de la escala de colores para rendimiento
escala_rendimiento = st.selectbox(
    "Seleccione el rango de escala de colores para el rendimiento:",
    ['-10% a +10%', '-6% a +6%', '-3% a +3%', '-1% a +1%']
)

# Obtener el rango seleccionado
rangos = {
    '-10% a +10%': [-10, 10],
    '-6% a +6%': [-6, 6],
    '-3% a +3%': [-3, 3],
    '-1% a +1%': [-1, 1]
}
rango_color = rangos[escala_rendimiento]

# Obtener los datos
resultados = get_data(tickers, periodo)

if resultados.empty:
    st.error("No se encontraron datos para los tickers seleccionados.")
    st.write("Verifica los tickers y el periodo seleccionado.")
else:
    st.write("DataFrame Resultante:")
    st.write(resultados)  # Para ver las columnas y valores del DataFrame

    if visualizacion == 'Volumen':
        valor = 'Volumen'
    else:
        valor = 'Volumen por Precio'

    if valor in resultados.columns:
        fig = px.treemap(resultados,
                         path=['Ticker'],
                         values=valor,
                         color='Rendimiento',
                         hover_data={'Rendimiento': True},
                         color_continuous_scale=px.colors.sequential.Viridis,
                         color_continuous_midpoint=0,
                         range_color=rango_color,
                         title=f"Panel {panel}: {valor} y Rendimiento {periodo}"
        )

        fig.update_traces(
            textinfo='label+text+value',
            texttemplate='<b>%{label}</b><br><b>%{customdata[0]:.2f}%</b>',
            customdata=resultados[['Rendimiento']]
        )

        st.plotly_chart(fig)
    else:
        st.error(f"La columna '{valor}' no existe en los datos.")

    st.dataframe(resultados)
