import dash
from dash import html
from dash import dcc
import plotly.graph_objects as go
from google.cloud import storage
import numpy as np
import pandas as pd
from io import StringIO

# para inicializar la aplicacion
app = dash.Dash()

bucket_name = 'cloudthon-homework-bucket'
blob_name = 'regression_test2.csv'
project_id = 'cloudthon-homework'
credentials_path = 'cloudthon-homework-e9095dd7ef2e.json'
storage_client = storage.Client.from_service_account_json(credentials_path)

def fetch_file_from_gcp():
    bucket = storage_client.get_bucket(bucket_name)
    blob = bucket.blob(blob_name)
    content = blob.download_as_text()
    data = pd.read_csv(StringIO(content))
    return data

def house_prices():
    df = fetch_file_from_gcp()
    x = np.arange(1, len(df['Rooms']) + 1)
    y = np.array(df['Price'])
    coeffs = np.polyfit(x, y, 1)
    y_fit = np.polyval(coeffs, x)

    # Function for creating line chart showing house's prices according to the number of rooms
    fig = go.Figure([go.Scatter(x = x,
                                y = y_fit,
                                mode='lines',
                                name = 'Regression'
                                ),
                                go.Scatter(x = x,
                                y = y,
                                mode='markers',
                                name = 'Prices'
                                )])
    fig.update_layout(title = 'Precios de Casas',
                      xaxis_title = 'Rooms',
                      yaxis_title = 'Price'
                      )
    return fig


app.layout = html.Div(id = 'parent',
                      children = [
                          html.H1(id = 'H1',
                                  children = 'Precios de acuerdo a numero de habitaciones',
                                  style = {'textAlign':'center', 'marginTop':40,'marginBottom':40}),
                          dcc.Graph(id = 'line_plot',
                                    figure = house_prices())
                      ])

if __name__ == '__main__':
    app.run_server(port=5003)