import dash
from dash import dcc, html
import pandas as pd
import plotly.graph_objs as go
import yfinance as yf
from datetime import datetime, timedelta

# تحميل البيانات
def load_data():
    today = datetime.today()
    start = today - timedelta(days=90)
    try:
        sp500 = yf.download('^GSPC', start=start, end=today, auto_adjust=True, progress=False).dropna()
        dax = yf.download('^GDAXI', start=start, end=today, auto_adjust=True, progress=False).dropna()
        ftse = yf.download('^FTSE', start=start, end=today, auto_adjust=True, progress=False).dropna()
    except:
        sp500 = dax = ftse = pd.DataFrame()
    return sp500, dax, ftse

sp500, dax, ftse = load_data()

app = dash.Dash(__name__)
server = app.server

def create_chart(df, title, label):
    if df.empty:
        return html.Div(f"❌ تعذر تحميل بيانات {label}", style={'color': 'red', 'textAlign': 'center', 'fontSize': 20})
    return dcc.Graph(
        figure={
            'data': [go.Scatter(x=df.index, y=df['Close'], mode='lines', name=label)],
            'layout': go.Layout(title=title, xaxis={'title': 'التاريخ'}, yaxis={'title': 'السعر'})
        }
    )

app.layout = html.Div([
    html.H1("لوحة متابعة الأسواق العالمية", style={'textAlign': 'center'}),
    create_chart(sp500, 'S&P 500', 'S&P 500'),
    create_chart(dax, 'DAX الألماني', 'DAX'),
    create_chart(ftse, 'FTSE البريطاني', 'FTSE 100')
])

if __name__ == "__main__":
    app.run_server(debug=True)
