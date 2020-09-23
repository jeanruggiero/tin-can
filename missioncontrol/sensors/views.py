from django.shortcuts import render
import plotly.graph_objs as go


def home(request):


    x = [1600819244822096000, 1600819245828558000, 1600819246836249000, 1600819247841971000, 1600819248848639000]
    y = [4, 4, 4, 3, 3]

    figure = go.Figure()

    figure.add_trace(go.Scatter(x=x, y=y, marker={'color': 'red', 'symbol': 104, 'size': 10},
                        mode="lines", name='1st Trace'))

    figure.update_layout(title="PM2.5 Particle Count", xaxis={'title': 'time'}, yaxis={'title': 'x2'})




    return render(request, 'sensors/home.html', {'graph': figure.to_html()})
