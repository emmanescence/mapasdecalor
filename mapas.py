import yfinance as yf
import pandas as pd
import plotly.express as px
import streamlit as st

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

color_ranges = {
    '-10% a +10%': [-10, 10],
    '-6% a +6%': [-6, 6],
    '-3% a +3%': [-3, 3],
    '-1% a +1%': [-1, 1]
}

st.title("Análisis de Acciones")

panel_option = st.selectbox('Seleccione el panel', ['Panel General', 'Panel Líder', 'Todos'])
color_scale_option = st.selectbox('Seleccione la escala de colores', ['-10% a +10%', '-6% a +6%', '-3% a +3%', '-1% a +1%'])

if panel_option == 'Panel General':
    tickers = tickers_panel_general
    panel_name = 'Panel General'
    resultados = get_last_data(tickers, '5d', panel_name)
elif panel_option == 'Panel Líder':
    tickers = tickers_panel_lider
    panel_name = 'Panel Líder'
    resultados = get_last_data(tickers, '5d', panel_name)
else:
    data_general = get_last_data(tickers_panel_general, '5d', 'Panel General')
    data_lider = get_last_data(tickers_panel_lider, '5d', 'Panel Líder')

    data_general = data_general.dropna(subset=['Volumen', 'Rendimiento Diario'])
    data_general = data_general[data_general['Volumen'] > 0]
    
    data_lider = data_lider.dropna(subset=['Volumen', 'Rendimiento Diario'])
    data_lider = data_lider[data_lider['Volumen'] > 0]

    st.write("Datos finales para ambos paneles combinados:")
    st.write(pd.concat([data_general, data_lider]))

    fig_general = px.treemap(data_general,
                            path=['Ticker'],
                            values='Volumen',
                            color='Rendimiento Diario',
                            color_continuous_scale='RdYlGn',
                            color_continuous_midpoint=0,
                            range_color=color_ranges[color_scale_option],
                            title="Panel General",
                            labels={'Rendimiento Diario': 'Rendimiento'})
    
    fig_lider = px.treemap(data_lider,
                          path=['Ticker'],
                          values='Volumen',
                          color='Rendimiento Diario',
                          color_continuous_scale='RdYlGn',
                          color_continuous_midpoint=0,
                          range_color=color_ranges[color_scale_option],
                          title="Panel Líder",
                          labels={'Rendimiento Diario': 'Rendimiento'})
    
    st.plotly_chart(fig_general)
    st.plotly_chart(fig_lider)

if panel_option != 'Todos':
    resultados = resultados.dropna(subset=['Volumen', 'Rendimiento Diario'])
    resultados = resultados[resultados['Volumen'] > 0]

    if resultados.empty:
        st.write("No hay datos válidos para graficar.")
    else:
        fig = px.treemap(resultados,
                         path=['Panel', 'Ticker'],
                         values='Volumen',
                         color='Rendimiento Diario',
                         color_continuous_scale='RdYlGn',
                         color_continuous_midpoint=0,
                         range_color=color_ranges[color_scale_option],
                         title="Análisis de Acciones",
                         labels={'Rendimiento Diario': 'Rendimiento'})
        st.plotly_chart(fig)

