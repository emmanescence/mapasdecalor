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
    # Retornar el DataFrame solo si contiene datos
    if data:
        return pd.DataFrame(data)
    else:
        return pd.DataFrame()  # Si no hay datos, retornar un DataFrame vacío

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

# Comprobar si el DataFrame tiene datos antes de graficar
if resultados.empty:
    st.error("No se encontraron datos para los tickers seleccionados.")
else:
    st.write("DataFrame Resultante:")
    st.write(resultados)  # Para ver las columnas y valores del DataFrame

    # Definir el campo de valores a visualizar
    if visualizacion == 'Volumen':
        valor = 'Volumen'
    else:
        valor = 'Volumen por Precio'

    # Asegurarse de que el valor exista como columna en el DataFrame
    if valor in resultados.columns:
        # Crear el gráfico de treemap con etiquetas de rendimiento
        fig = px.treemap(resultados,
                         path=['Ticker'],
                         values=valor,  # Asegúrate de que esta columna existe
                         color='Rendimiento',
                         hover_data={'Rendimiento': True},  # Mostrar rendimiento en el hover
                         color_continuous_scale=[(0, 'red'), (0.5, 'white'), (1, 'green')],
                         color_continuous_midpoint=0,
                         range_color=rango_color,  # Usar el rango de color seleccionado
                         title=f"Panel {panel}: {valor} y Rendimiento {periodo}"
        )

        # Ajustar etiquetas de rendimiento en el gráfico
        fig.update_traces(
            textinfo='label+value',  # Mostrar nombre del ticker y el valor del campo seleccionado
            texttemplate='<b>%{label}</b><br><b>%{customdata[0]:.2f}%</b>',  # Mostrar ticker y rendimiento
            customdata=resultados[['Rendimiento']]  # Añadir la columna de rendimiento a customdata
        )

        # Mostrar el gráfico en la app
        st.plotly_chart(fig)
    else:
        st.error(f"La columna '{valor}' no existe en los datos.")

    # Mostrar el DataFrame resultante para depuración
    st.dataframe(resultados)


