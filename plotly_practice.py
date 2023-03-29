import pandas as pd
import numpy as np
import duckdb
import plotly.express as px
import plotly.graph_objects as go
#import plotly.io as pio
#pio.renderers.default = "browser"

df = pd.read_csv('practice_data/Salesdata/Data.csv')

df['year'] = df['OrderDate'].str.slice(start = 0, stop = 4)
df['month'] = df['OrderDate'].str.slice(start = 5, stop = 7)

df_g1=duckdb.query("select Country, sum(Revenue) as Revenue, sum(Revenue)-sum(Cost) as Margin from df where year=2020 group by Country order by Revenue desc limit 10").df()

trace1 = go.Bar(
    y=df_g1['Country'],
    x=df_g1['Revenue'],
    name = 'Revenue',
    orientation = 'h')

trace2 = go.Bar(
    y=df_g1['Country'],
    x=df_g1['Revenue'],
    name = 'Margins',
    orientation = 'h')

graph_obj = [trace1,trace2]
layout = go.Layout(title = 'Chap2 - Bar Chart', barmode = 'group', yaxis = dict(autorange='reversed'))
fig = go.Figure(graph_obj, layout)
fig.show()