import streamlit as st
import pandas as pd
from plotly.subplots import make_subplots
import plotly.graph_objects as go
import datetime
from data_loader import get_stock_data
from indicators import calc_sma, calc_rsi
st.set_page_config(
    page_title = "Stock Dashboard",
    page_icon = "📈",
    layout = "wide",
    initial_sidebar_state="collapsed"
)

st.title("Stocks Dashboard")


sb = st.sidebar

sb.header("Stock Settings")

ticker = sb.text_input(
    label="Stock Ticker",
    value="TATASTEEL.NS"
)

today = datetime.date.today()
defdate = today - datetime.timedelta(days = 365*2)

start_date= sb.date_input(
    label = "Start Date",
    value = defdate
)

end_date = sb.date_input(
    label = "End Date",
    value = today,
)

analyse_button = st.sidebar.button("Analyse")

if analyse_button:
    st.write("You Selected:")
    st.write("Ticker:", ticker)
    st.write("Start-Date", start_date)
    st.write("End-Date:", end_date)
    
    
    
    data = get_stock_data(ticker, start_date, end_date)
    
    if data is None:
        st.error("No data found. Please check ticker symbol.")
    else:
        data['SMA_20'] = calc_sma(data, 20)
        data['SMA_50'] = calc_sma(data, 50)
        
        data['RSI'] = calc_rsi(data)
        
        
        
        
        fig = make_subplots(
        rows=3,
        cols=1,
        shared_xaxes=True,
        vertical_spacing=0.02,
        row_heights=[0.6, 0.25, 0.15]
    )
        
    fig.add_trace(
        go.Candlestick(
            x=data['Date'],
            open=data['Open'],
            high=data['High'],
            low=data['Low'],
            close=data['Close'],
            name="Price"
        ),
        row=1,
        col=1
    )

    
    fig.add_trace(go.Scatter(
        x=data['Date'],
        y=data['SMA_20'],
        line=dict(color='orange', width=1),
        name ="SMA 20"
    ),
    row = 1,
    col = 1
    )
    
    fig.add_trace(go.Scatter(
        x=data['Date'],
        y=data['SMA_50'],
        line=dict(color='blue', width=1),
        name ="SMA 50"
    ),
    row = 1,
    col = 1
    )    

    fig.add_trace(
        go.Bar(
            x=data['Date'],
            y=data['Volume'],
            name="Volume"
        ),
        row=2,
        col=1
    )
    
    fig.add_trace(
        go.Scatter(
            x = data['Date'],
            y = data['RSI'],
            line = dict(color='cyan', width =1),
            name = "RSI"
        ),
        row=3,
        col=1
    )
    
    fig.add_hline(y=70, line_dash="dash", line_color="red", row=3, col=1)
    fig.add_hline(y=30, line_dash="dash", line_color="green", row=3, col=1)
    
    fig.update_layout(
        title=f"{ticker} Price and Volume",
        template="plotly_dark",
        xaxis_rangeslider_visible=False,
        hovermode="x unified",
        height=700
    )

    st.plotly_chart(fig, use_container_width=True)