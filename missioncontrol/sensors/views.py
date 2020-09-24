from django.shortcuts import render
import plotly.graph_objs as go
from influxdb_client import InfluxDBClient
import os


def home(request):

    database = 'lifesupport'
    retention_policy = 'autogen'
    bucket = f'{database}/{retention_policy}'

    # Connect to influxdb
    token = os.environ.get('INFLUXDB_TOKEN')
    client = InfluxDBClient(url="http://localhost:8086", token=token, org='-')

    influx = client.query_api()

    # Query pm2.5 sensor data
    table = influx.query(f'from(bucket:"{bucket}") '
                      '|> range(start: -5m)'
                      '|> filter(fn: (r) => r._measurement == "pm25standard")'
                      '|> keep(columns: ["_time", "_value"])')[0]

    figure = go.Figure()

    figure.add_trace(go.Scatter(x=[record.get_value() for record in table],
                                y=[record.get_time() for record in table],
                                marker={'color': 'red',
                                        'symbol': 104,
                                        'size': 10
                                        },
                                mode="lines", name='pm25standard'))

    figure.update_layout(title="PM2.5 Particle Count", xaxis={'title': 'time'}, yaxis={'title': 'x2'})

    return render(request, 'sensors/home.html', {'graph': figure.to_html()})
