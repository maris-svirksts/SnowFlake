import streamlit as st
import snowflake.connector
import pandas as pd
import plotly.graph_objects as go
from datetime import datetime

# Snowflake credentials are stored in Streamlit's secrets
def get_snowflake_connection():
    try:
        conn = snowflake.connector.connect(
            user=st.secrets["snowflake"]["user"],
            password=st.secrets["snowflake"]["password"],
            role=st.secrets["snowflake"]["role"],
            account=st.secrets["snowflake"]["account"],
            warehouse=st.secrets["snowflake"]["warehouse"],
            database=st.secrets["snowflake"]["database"],
            schema=st.secrets["snowflake"]["schema"],
            client_session_keep_alive=True  # Keep the session alive
        )
        return conn
    except Exception as e:
        st.error(f"Error connecting to Snowflake: {str(e)}")
        return None

# Fetch stock data from Snowflake based on symbol and date range
def fetch_stock_data_from_snowflake(symbol, start_date, end_date):
    conn = get_snowflake_connection()
    if not conn:
        return None

    try:
        cursor = conn.cursor()
        query = """
        SELECT SYMBOL, TRADE_DATE, OPEN_PRICE, HIGH_PRICE, LOW_PRICE, CLOSE_PRICE, VOLUME_TRADED
        FROM STOCK_PRICE_DATA
        WHERE SYMBOL = %s AND TRADE_DATE BETWEEN %s AND %s
        ORDER BY TRADE_DATE
        """
        cursor.execute(query, (symbol, start_date, end_date))
        result = cursor.fetchall()
        columns = [desc[0] for desc in cursor.description]

        df = pd.DataFrame(result, columns=columns)
        cursor.close()
        conn.close()  # Close the connection after the query
        return df
    except Exception as e:
        st.error(f"Error fetching data from Snowflake: {str(e)}")
        if conn:
            conn.close()  # Ensure the connection is closed in case of an error
        return None

# Streamlit UI to select stock symbol and visualize data
st.title("Stock Price Data Visualization")

# Dropdown to select stock symbol (AAPL, GOOGL)
symbol = st.selectbox("Select Stock Symbol", ["AAPL", "GOOGL"])

# Date range selection
start_date = st.date_input("Start Date", datetime(2020, 1, 1))
end_date = st.date_input("End Date", datetime.today())

if symbol:
    # Fetch data from Snowflake
    df = fetch_stock_data_from_snowflake(symbol, start_date, end_date)

    if df is not None and not df.empty:
        # Display data
        st.write(f"Showing stock data for {symbol}")
        st.dataframe(df)

        # Convert 'TRADE_DATE' to datetime
        df['TRADE_DATE'] = pd.to_datetime(df['TRADE_DATE'])

        # Add moving averages
        df['SMA_50'] = df['CLOSE_PRICE'].rolling(window=50).mean()
        df['SMA_200'] = df['CLOSE_PRICE'].rolling(window=200).mean()

        # Create the candlestick chart using Plotly
        fig = go.Figure(data=[go.Candlestick(
            x=df['TRADE_DATE'],
            open=df['OPEN_PRICE'],
            high=df['HIGH_PRICE'],
            low=df['LOW_PRICE'],
            close=df['CLOSE_PRICE'],
            name='Stock Prices'
        )])

        # Add 50-day and 200-day moving averages
        fig.add_trace(go.Scatter(
            x=df['TRADE_DATE'],
            y=df['SMA_50'],
            name='50-day SMA',
            line=dict(color='blue')
        ))

        fig.add_trace(go.Scatter(
            x=df['TRADE_DATE'],
            y=df['SMA_200'],
            name='200-day SMA',
            line=dict(color='red')
        ))

        # Add volume bar chart
        fig.add_trace(go.Bar(
            x=df['TRADE_DATE'],
            y=df['VOLUME_TRADED'],
            name='Volume',
            yaxis='y2',
            marker=dict(color='lightgray'),
            opacity=0.5
        ))

        # Update layout to add second y-axis for volume
        fig.update_layout(
            title=f"{symbol} Stock Price Candlestick Chart",
            xaxis_title="Date",
            yaxis_title="Price",
            xaxis_rangeslider_visible=False,
            yaxis2=dict(overlaying='y', side='right', title="Volume")
        )

        # Display the chart in Streamlit
        st.plotly_chart(fig)
    else:
        st.error("No data found for the specified stock symbol and date range.")
else:
    st.error("Please select a stock symbol.")
