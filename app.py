import dash
from dash import dcc, html
import pandas as pd
import plotly.graph_objs as go
import yfinance as yf
from datetime import datetime, timedelta

# تحميل البيانات
def load_data():
    today = datetime.today()
    start = today - timedelta(days=365)
    try:
        sp500 = yf.download(tickers='^GSPC', start=start, end=today, auto_adjust=False, progress=False)
        dax = yf.download(tickers='^GDAXI', start=start, end=today, auto_adjust=False, progress=False)
        ftse = yf.download(tickers='^FTSE', start=start, end=today, auto_adjust=False, progress=False)
    except Exception as e:
        print(f"Download error: {e}")
        sp500, dax, ftse = pd.DataFrame(), pd.DataFrame(), pd.DataFrame()

    print("S&P 500 rows:", len(sp500))
    print("DAX rows:", len(dax))
    print("FTSE rows:", len(ftse))

    return sp500, dax, ftse

sp500, dax, ftse = load_data()

# إنشاء التطبيق
app = dash.Dash(__name__)
server = app.server

def generate_graph(df, title, name):
    if df.empty:
        return html.Div(f"لا توجد بيانات لعرض {title}")
    return dcc.Graph(
        figure={
            'data': [go.Scatter(x=df.index, y=df['Close'], mode='lines', name=name)],
            'layout': go.Layout(title=title, xaxis={'title': 'تاريخ'}, yaxis={'title': 'السعر'})
        }
    )

app.layout = html.Div([
    html.H1('لوحة التخصصات العالمية', style={'textAlign': 'center'}),
    generate_graph(sp500, "S&P 500", "S&P 500"),
    generate_graph(dax, "مؤشر DAX الألماني", "DAX"),
    generate_graph(ftse, "مؤشر FTSE البريطاني", "FTSE")
])

if __name__ == '__main__':
    app.run_server(debug=True)
