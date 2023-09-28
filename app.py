import dash
from dash import html
from dash import dcc
import plotly.graph_objects as go
from google.oauth2 import service_account
from google.cloud import storage
from google.cloud import bigquery
import numpy as np
import pandas as pd
from io import StringIO

# para inicializar la aplicacion
app = dash.Dash()

BUCKET_NAME = 'cloudthon-homework-bucket'
BLOB_NAME = 'regression_test2.csv'
CREDENTIALS_PATH = 'cloudthon-homework-e9095dd7ef2e.json'
credentials = service_account.Credentials.from_service_account_file(
    CREDENTIALS_PATH, scopes=["https://www.googleapis.com/auth/cloud-platform"]
)
storage_client = storage.Client(credentials= credentials, project= credentials.project_id)
bigquery_client = bigquery.Client(credentials=credentials, project=credentials.project_id)

#Function to fetch the CSV from GCP bucket
def fetch_file_from_gcp():
    bucket = storage_client.get_bucket(BUCKET_NAME)
    blob = bucket.blob(BLOB_NAME)
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
    app.run_server(host='0.0.0.0', debug=True, port=8080)
