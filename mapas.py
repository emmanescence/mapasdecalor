# Función para obtener datos
def get_data(tickers, period='1d', value_metric='Capitalización'):
    data = []
    for ticker in tickers:
        stock = yf.Ticker(ticker)
        hist = stock.history(period='1y')  # Obtener datos del último año
        if len(hist) > 1:
            # Determinar el periodo para el cálculo del rendimiento y el volumen
            if period == '1d':
                period_data = hist.tail(2)  # Últimos dos días
                volume_sum = hist['Volume'].iloc[-1]  # Volumen del último día
            elif period == '1wk':
                period_data = hist.resample('W').last().tail(2)  # Últimas dos semanas
                volume_sum = hist['Volume'].resample('W').sum().iloc[-1]  # Sumar volumen semanal
            elif period == '1mo':
                period_data = hist.resample('M').last().tail(2)  # Últimos dos meses
                volume_sum = hist['Volume'].resample('M').sum().iloc[-1]  # Sumar volumen mensual
            elif period == '1y':
                period_data = hist.resample('A').last().tail(2)  # Últimos dos años
                volume_sum = hist['Volume'].resample('A').sum().iloc[-1]  # Sumar volumen anual
            else:
                raise ValueError("Periodo no soportado")

            if len(period_data) >= 2:
                # Obtener precios de cierre
                last_close = period_data['Close'].iloc[-1]
                previous_close = period_data['Close'].iloc[-2]

                # Calcular el rendimiento
                performance = (last_close - previous_close) / previous_close * 100

                # Calcular la capitalización
                capi = volume_sum * last_close

                # Determinar el valor a mostrar según la métrica seleccionada
                value = capi if value_metric == 'Capitalización' else volume_sum

                # Agregar panel como 'Panel Líder' o 'Panel General'
                panel_type = 'Panel Líder' if ticker in tickers_panel_lider else 'Panel General'

                data.append({
                    'Ticker': ticker,
                    'Panel': panel_type,
                    'Volumen': volume_sum,
                    'Rendimiento': performance,
                    'Capitalización': capi,
                    'Value': value
                })
            else:
                continue  # Omitir si no hay suficientes datos para calcular el rendimiento
        else:
            continue  # Omitir si no hay suficientes datos históricos
    return pd.DataFrame(data)

