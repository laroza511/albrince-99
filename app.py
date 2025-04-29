import dash
from dash import dcc, html
import pandas as pd
import plotly.graph_objs as go
import yfinance as yf
from datetime import datetime, timedelta

# تحميل البيانات
def load_data():
    today = datetime.today()
    start = today - timedelta(days=365)  # مددنا الفترة سنة

    sp500 = yf.download(tickers='^GSPC', start=start, end=today, auto_adjust=False, progress=False)
    dax = yf.download(tickers='^GDAXI', start=start, end=today, auto_adjust=False, progress=False)
    ftse = yf.download(tickers='^FTSE', start=start, end=today, auto_adjust=False, progress=False)

    return sp500, dax, ftse

sp500, dax, ftse = load_data()

# إنشاء التطبيق
app = dash.Dash(__name__)
server = app.server

app.layout = html.Div([
    html.H1('لوحة التخصصات العالمية', style={'textAlign': 'center'}),

    dcc.Graph(
        id='sp500',
        figure={
            'data': [go.Scatter(x=sp500.index, y=sp500['Close'], mode='lines', name='S&P 500')],
            'layout': go.Layout(title='S&P 500', xaxis={'title': 'تاريخ'}, yaxis={'title': 'السعر'})
        }
    ),
    dcc.Graph(
        id='dax',
        figure={
            'data': [go.Scatter(x=dax.index, y=dax['Close'], mode='lines', name='DAX')],
            'layout': go.Layout(title='الألماني DAX', xaxis={'title': 'تاريخ'}, yaxis={'title': 'السعر'})
        }
    ),
    dcc.Graph(
        id='ftse',
        figure={
            'data': [go.Scatter(x=ftse.index, y=ftse['Close'], mode='lines', name='FTSE')],
            'layout': go.Layout(title='البريطاني FTSE', xaxis={'title': 'تاريخ'}, yaxis={'title': 'السعر'})
        }
    )
])

if __name__ == '__main__':
    app.run_server(debug=True)
