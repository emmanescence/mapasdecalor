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
            textinfo='label+value+text',
            texttemplate='<b>%{label}</b><br><b>%{customdata[0]:.2f}%</b>',
            customdata=resultados[['Rendimiento']]
        )

        st.plotly_chart(fig)
    else:
        st.error(f"La columna '{valor}' no existe en los datos.")

    st.dataframe(resultados)

