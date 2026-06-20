import streamlit as st
import yfinance as yf
import pandas as pd
import plotly.express as px
from datetime import datetime, timedelta
import numpy as np
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error

st.set_page_config(page_title="Portfolio Dashboard", layout="wide")

st.title("Análisis de Portafolio")

st.sidebar.header("Configuración")

# Lista de tickers
tickers_options = [
    "AAPL", "MSFT", "GOOGL", "AMZN", "TSLA", "NVDA", "META", "AMD",
    "^GSPC", "^IXIC", "BTC-USD", "ETH-USD", "MELI", "JPM", "V", "MA",
    "KO", "PEP", "NFLX", "ADBE", "CRM", "PYPL"
]

selected_tickers = st.sidebar.multiselect(
    "Selecciona los activos",
    options=tickers_options,
    default=["AAPL", "MSFT", "GOOGL", "^GSPC"]
)

benchmark = st.sidebar.selectbox("Benchmark", ["^GSPC", "BTC-USD", "Ninguno"], index=0)

end_date = datetime.today()
start_date = st.sidebar.date_input("Fecha de inicio", value=end_date - timedelta(days=365))
end_date = st.sidebar.date_input("Fecha de fin", value=end_date)

# Pesos
st.sidebar.subheader("Pesos del portafolio (%)")
weights = {}
total = 0
for ticker in selected_tickers:
    w = st.sidebar.number_input(f"{ticker}", min_value=0.0, max_value=100.0, value=25.0, step=5.0)
    weights[ticker] = w / 100.0
    total += w

if abs(total - 100) > 2 and len(selected_tickers) > 0:
    st.sidebar.warning(f"Suma de pesos: {total:.1f}% (idealmente 100%)")

# Función con caché
@st.cache_data(ttl=3600)
def download_data(tickers, start, end):
    return yf.download(tickers, start=start, end=end, group_by="ticker", progress=False)

# Botón para cargar datos
if st.sidebar.button("Cargar Datos"):
    with st.spinner("Descargando datos..."):
        try:
            tickers_to_download = list(selected_tickers)
            if benchmark != "Ninguno" and benchmark not in tickers_to_download:
                tickers_to_download.append(benchmark)
            
            data = download_data(tuple(tickers_to_download), start_date, end_date)
            st.session_state.data = data
            st.session_state.weights = weights
            st.session_state.benchmark = benchmark
            st.success("Datos cargados correctamente")
        except Exception as e:
            st.error(f"Error al descargar datos: {e}")

# ====================== ANÁLISIS ======================
if "data" in st.session_state:
    data = st.session_state.data
    weights = st.session_state.weights
    benchmark = st.session_state.benchmark
    
    # Extraer precios de cierre
    closes = pd.DataFrame()
    for ticker in data.columns.levels[0]:
        if ticker in selected_tickers or ticker == benchmark:
            closes[ticker] = data[ticker]['Close']
    
    closes = closes.dropna()
    returns = closes.pct_change().dropna()
    
    # Portafolio
    portfolio_returns = returns[list(weights.keys())].dot(pd.Series(weights))
    cum_portfolio = (1 + portfolio_returns).cumprod() - 1

    # KPIs
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Retorno Total", f"{cum_portfolio.iloc[-1]:.2%}")
    with col2:
        vol = portfolio_returns.std() * (252 ** 0.5)
        st.metric("Volatilidad Anual", f"{vol:.2%}")
    with col3:
        sharpe = (portfolio_returns.mean() * 252) / vol if vol != 0 else 0
        st.metric("Sharpe Ratio", f"{sharpe:.2f}")
    with col4:
        cum_r = (1 + portfolio_returns).cumprod()
        dd = cum_r / cum_r.cummax() - 1
        st.metric("Max Drawdown", f"{dd.min():.2%}")

    # Tabs
    tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs([
        "Precios Normalizados", "Retornos", "Distribución", 
        "Correlaciones", "Detalles", "Predicción ML"
    ])

    with tab1:
        st.subheader("Precios Normalizados")
        normalized = closes / closes.iloc[0] * 100
        fig = px.line(normalized, title="Comparación de Rendimiento")
        st.plotly_chart(fig, use_container_width=True)

    with tab2:
        st.subheader("Retorno Acumulado del Portafolio")
        fig_cum = px.line(x=cum_portfolio.index, y=cum_portfolio * 100, 
                         title="Retorno Acumulado (%)")
        st.plotly_chart(fig_cum, use_container_width=True)

    with tab3:
        st.subheader("Distribución del Portafolio")
        fig_pie = px.pie(names=weights.keys(), values=weights.values())
        st.plotly_chart(fig_pie, use_container_width=True)

    with tab4:
        st.subheader("Matriz de Correlaciones")
        fig_corr = px.imshow(returns.corr(), text_auto=True, color_continuous_scale='RdBu_r')
        st.plotly_chart(fig_corr, use_container_width=True)

    with tab5:
        st.subheader("Rendimiento por Activo")
        perf = pd.DataFrame({
            "Retorno Total": closes.iloc[-1] / closes.iloc[0] - 1,
            "Volatilidad Anual": returns.std() * (252 ** 0.5)
        })
        st.dataframe(perf.style.format("{:.2%}"), use_container_width=True)
        
        st.subheader("Últimos datos")
        st.dataframe(closes.tail(10).style.format("${:.2f}"), use_container_width=True)

        csv = closes.to_csv().encode('utf-8')
        st.download_button("Descargar Datos CSV", csv, "portfolio_data.csv", "text/csv")

    with tab6:
        st.subheader("Predicción con Linear Regression")
        ticker_ml = st.selectbox("Selecciona activo para predecir", selected_tickers)
        
        if ticker_ml in closes.columns:
            price_series = closes[ticker_ml]
            X = np.arange(len(price_series)).reshape(-1, 1)
            y = price_series.values
            
            model = LinearRegression()
            model.fit(X, y)
            
            future_days = np.arange(len(price_series), len(price_series) + 30).reshape(-1, 1)
            pred = model.predict(future_days)
            
            fig_ml = px.line(x=price_series.index, y=price_series, title=f"Predicción de {ticker_ml}")
            future_index = pd.date_range(start=price_series.index[-1], periods=31, freq='B')[1:]
            fig_ml.add_scatter(x=future_index, y=pred, mode='lines', name='Predicción 30 días', line=dict(dash='dash'))
            st.plotly_chart(fig_ml, use_container_width=True)
            
            rmse = np.sqrt(mean_squared_error(y, model.predict(X)))
            st.metric("RMSE del modelo", f"${rmse:.2f}")

else:
    st.info("Selecciona los activos en la barra lateral y presiona 'Cargar Datos'")
