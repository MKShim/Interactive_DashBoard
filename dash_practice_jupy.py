# ---
# jupyter:
#   jupytext:
#     formats: ipynb,py:light
#     text_representation:
#       extension: .py
#       format_name: light
#       format_version: '1.5'
#       jupytext_version: 1.14.5
#   kernelspec:
#     display_name: Python 3 (ipykernel)
#     language: python
#     name: python3
# ---

# +
#pip install duckdb
# -

import pandas as pd
import numpy as np
import duckdb
import pymysql
import plotly.express as px
import plotly.graph_objects as go
#import plotly.io as pio
#pio.renderers.default = "browser"

dash_db = pymysql.connect(
    user='root', 
    passwd='0000', 
    host='127.0.0.1', 
    db='dash', 
    charset='utf8'
)

cursor_dash = dash_db.cursor(pymysql.cursors.DictCursor)
cursor_dash.execute("select * from dash.saledata")
saledata_dic = cursor_dash.fetchall()

saledata = pd.DataFrame(saledata_dic)
saledata

saledata.info()

# +
#saledata = pd.read_csv('/Users/minkyoung/Documents/Dev/DashBoard_basic/practice_data/Salesdata/Data.csv')

#saledata['year'] = saledata['OrderDate'].str.slice(start = 0, stop = 4)
#saledata['month'] = saledata['OrderDate'].str.slice(start = 5, stop = 7)
# -

saledata['year'] = pd.DatetimeIndex(saledata['OrderDate']).year
saledata['month'] = pd.DatetimeIndex(saledata['OrderDate']).month

# +
df_g1=duckdb.query("select Country, sum(Revenue) as Revenue, sum(Revenue)-sum(Cost) as Margin from saledata where year=2020 group by Country order by Revenue desc limit 10").df()

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
# -

# Scatter Chart
df_scatter = duckdb.query("Select year, month, sum(Revenue) as Revenue from (select substr(OrderDate,1,4) as year, substr(OrderDate,6,2) as month, Revenue from saledata) group by year, month order by year, month").df()
year=list(df_scatter['year'].unique())

traces=[]
for years in year :
  tmp = df_scatter[df_scatter['year']==years]
  traces.append(go.Scatter(x=tmp['month'],
                           y=tmp['Revenue'],
                           #mode='Lines + Markers',
                           marker = dict(size=10),name=years))

scatter_layout=go.Layout(title='Scatter & Line Charts',
                         xaxis=dict(title='Month'),
                         yaxis=dict(title='Revenue'))

scatter_fig=go.Figure(traces,scatter_layout)
scatter_fig.show()

# Pie Chart
pie_df=duckdb.query("select AgeGroup, round(sum(Revenue),2) as Revenue from saledata group by agegroup order by agegroup").df()

pie_trace = go.Pie(labels=pie_df['AgeGroup'],values=pie_df['Revenue'],
               pull = [0,0,0.3,0,0],
               textinfo='label+percent',
               hole=0.3)
pie_layout=go.Layout(title = 'Pie Chart')
pie_fig = go.Figure(pie_trace,pie_layout)
pie_fig.show()

# Sankey Diagram : Flow diagram
sankey_df1 = duckdb.query('select Region, Channel, sum(Revenue) as Revenue from saledata where year=2020 group by Region, Channel, order by Region, Channel').df() # label, target, value
sankey_df2 = duckdb.query('select Channel, Category, sum(Revenue) as Revenue from saledata where year=2020 group by Channel, Category order by Channel, Category').df()

# +
sankey_labels = list(sankey_df1['Region'].unique())+list(sankey_df1['Channel'].unique())+list(sankey_df2['Category'].unique())
#sankey_sources = [0,0,1,1,2,2,3,3,4,4] +[5,5,5,5,5,6,6,6,6,6]
#sankey_targets=[5,6,5,6,5,6,5,6,5,6]+[7,8,9,10,11,7,8,9,10,11]
#sankey_values=list(sankey_df1['Revenue'])+list(sankey_df2['Revenue'])

l_c1=list(sankey_df1['Region'].unique())
l_c2=list(sankey_df1['Channel'].unique())
l_c3=list(sankey_df2['Category'].unique())
sankey_labels = l_c1+l_c2+l_c3
sankey_values=list(sankey_df1['Revenue'])+list(sankey_df2['Revenue'])

sankey_source1=list(np.repeat(range(0,len(l_c1)),len(l_c2)))
sankey_source2=list(np.repeat(range(len(l_c1),len(l_c1)+len(l_c2)),len(l_c3)))
sankey_sources=sankey_source1+sankey_source2

sankey_target1=list(range(len(l_c1),len(l_c1)+len(l_c2)))*len(l_c1)
sankey_target2=list(range(len(l_c1)+len(l_c2),len(l_c1)+len(l_c2)+len(l_c3)))*len(l_c2)
sankey_targets=sankey_target1+sankey_target2
# -

sankey_trace = go.Sankey(node=dict(label=sankey_labels),
                  link=dict(source=sankey_sources,
                            target=sankey_targets,
                            value=sankey_values))
sankey_layout=go.Layout(title='Sankey Diagram', font_size=15)
sankey_fig=go.Figure(sankey_trace,sankey_layout)
sankey_fig.show()





# +
#pip install mysql-connector-python
# -

import mysql.connector

mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    passwd="0000",
    database="Lpay")

cur = mydb.cursor()

cur.execute("select * from health.infor2020")

myresult = cur.fetchall()

pip install PyMySQL

import pymysql

mia_db = pymysql.connect(
    user='root', 
    passwd='0000', 
    host='127.0.0.1', 
    db='health', 
    charset='utf8'
)

cursor = mia_db.cursor(pymysql.cursors.DictCursor)

cursor.execute("select * from health.infor2020")
result = cursor.fetchall()

health_infor20 = pd.DataFrame(result)
health_infor20

# +
#pip install jupytext
#import jupytext
