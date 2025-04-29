import dash
from dash import dcc, html
import pandas as pd
import plotly.graph_objs as go
import yfinance as yf
from datetime import datetime, timedelta

# تحميل البيانات مع حماية ضد المشاكل
def load_data():
    today = datetime.today()
    start = today - timedelta(days=90)

    def safe_download(ticker):
        try:
            df = yf.download(tickers=ticker, start=start, end=today, auto_adjust=False, progress=False)
            if df is not None and not df.empty and len(df) > 1:
                return df
            else:
                print(f"[{ticker}] فشل التحميل أو البيانات غير كافية.")
                return pd.DataFrame()
        except Exception as e:
            print(f"خطأ في تحميل {ticker}: {e}")
            return pd.DataFrame()

    sp500 = safe_download('^GSPC')
    dax = safe_download('^GDAXI')
    ftse = safe_download('^FTSE')

    return sp500, dax, ftse

# تحميل البيانات
sp500, dax, ftse = load_data()

# إنشاء التطبيق
app = dash.Dash(__name__)
server = app.server

app.layout = html.Div([
    html.H1('لوحة متابعة الاقتصاد العالمي', style={'textAlign': 'center'}),

    dcc.Graph(
        id='sp500',
        figure={
            'data': [go.Scatter(x=sp500.index, y=sp500['Close'], mode='lines', name='S&P 500')] if not sp500.empty else [],
            'layout': go.Layout(title='مؤشر S&P 500', xaxis={'title': 'التاريخ'}, yaxis={'title': 'السعر'})
        }
    ),

    dcc.Graph(
        id='dax',
        figure={
            'data': [go.Scatter(x=dax.index, y=dax['Close'], mode='lines', name='DAX')] if not dax.empty else [],
            'layout': go.Layout(title='مؤشر DAX الألماني', xaxis={'title': 'التاريخ'}, yaxis={'title': 'السعر'})
        }
    ),

    dcc.Graph(
        id='ftse',
        figure={
            'data': [go.Scatter(x=ftse.index, y=ftse['Close'], mode='lines', name='FTSE 100')] if not ftse.empty else [],
            'layout': go.Layout(title='مؤشر FTSE البريطاني', xaxis={'title': 'التاريخ'}, yaxis={'title': 'السعر'})
        }
    )
])

if __name__ == "__main__":
    app.run_server(debug=True)
