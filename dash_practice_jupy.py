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
bar_layout = go.Layout(title = 'Bar Chart', barmode = 'group', yaxis = dict(autorange='reversed'))
bar_fig = go.Figure(graph_obj, bar_layout)
bar_fig.show()
# -

# Scatter Chart
df_scatter = duckdb.query("Select year, month, sum(Revenue) as Revenue from (select substr(OrderDate,1,4) as year, substr(OrderDate,6,2) as month, Revenue from saledata) group by year, month order by year, month").df()
year=list(df_scatter['year'].unique())

scatter_traces=[]
for years in year :
  tmp = df_scatter[df_scatter['year']==years]
  scatter_traces.append(go.Scatter(x=tmp['month'],
                           y=tmp['Revenue'],
                           #mode='Lines + Markers',
                           marker = dict(size=10),name=years))

scatter_layout=go.Layout(title='Scatter & Line Charts',
                         xaxis=dict(title='Month'),
                         yaxis=dict(title='Revenue'))

scatter_fig=go.Figure(scatter_traces,scatter_layout)
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
# Box Plots
# -

box_df = duckdb.query('select Region, Revenue from saledata where year=2020 order by Region').df()

box_df

box_traces = []
regions = list(box_df['Region'].unique())

regions

# Creating Graph objects 
for region in regions:
    tmp = box_df[box_df['Region']== region]
    box_traces.append(go.Box(y =tmp['Revenue'],name = region))

box_traces

box_layout = go.Layout(title='Box plot')
box_fig = go.Figure(box_traces,box_layout)

box_fig.show()

saledata.head()

# +
# Histogram
# -

hist_df = duckdb.query('select AgeGroup, Quantity from saledata where year=2020').df()

hist_df.head()

ages=list(hist_df['AgeGroup'].unique())

ages.sort()

ages

# +
# Create graph objects, for Multi Histograms Group by Ages
# -

from plotly.subplots import make_subplots

hist_fig = make_subplots(rows = 2, cols = 3, shared_yaxes = 'all') 

hist_traces= []
for age in ages:
    hist_traces.append(go.Histogram(x = hist_df[hist_df['AgeGroup']== age]['Quantity'], name= age))

hist_traces

# +
hist_fig.append_trace(hist_traces[0],1,1) # mat(1,1) 
hist_fig.append_trace(hist_traces[1],1,2) # mat(1,2)
hist_fig.append_trace(hist_traces[2],1,3) # mat(1,3) 
hist_fig.append_trace(hist_traces[3],2,1) # mat(2,1)
hist_fig.append_trace(hist_traces[4],2,2) # mat(2,2)
hist_fig.update_layout(title = 'Histogram')

hist_fig.show()
# -

saledata.head()

# +
# Scatter & Error(+/- std) Bar : shows data deviation, ranges
# -

err_df = duckdb.query("select channel, year, round(mean(revenue),2) as mean, round(stddev(revenue),2) as sd, count(revenue) as n from saledata where Region='Asia' and category='Foods' group by channel, year order by channel, year").df()

err_df

err_df_off = err_df[err_df['Channel'] == 'Offline'].copy()

# +
scerr_trace=go.Scatter(x=err_df_off['year'], 
                 y = err_df_off['mean'],
                 error_y = dict(type= 'data',array = err_df_off['sd']),
                 name = 'Offline')
                               
err1_data = [scerr_trace]
# -

err1_layout = go. Layout(title = 'Scatter &Error Bar (Offline)', 
                    xaxis = dict(title = 'Year'),
                    yaxis = dict(title = 'Revenue (Mean)')) 
err1_fig = go.Figure(err1_data, err1_layout)
err1_fig.show()

# +
# Bar & Error Bar 
# -

import math

err_df['lower'] = err_df['mean']- err_df['sd'] 
err_df['upper'] = err_df['mean']+ err_df['sd'] 

ymax = math.ceil(err_df['upper'].max()*1.05) 
ymin = math.ceil(err_df['lower'].min()*0.95)



#hover text : mean(lower, upper), using 'K' means kilo (1000)
err_df['text'] = (err_df['mean']/1000).round(2).apply(lambda x: str(x)) + 'K (' + (err_df['lower']/1000).round(2).apply(lambda x: str(x)) + 'K, ' + (err_df['upper']/1000).round(2).apply(lambda x: str(x)) + 'K)'

err_df

channels =list(err_df['Channel'].unique()) 

channels

barerr_traces = []

dat= err_df[err_df['Channel'] == channel] 
dat

for channel in channels:
    dat= err_df[err_df['Channel'] == channel] 
    barerr_traces.append(go.Bar(x = dat['year'],
                                 y = dat['mean'],
                                 error_y=dict(type ='data',array = dat['sd']),
                                 text = dat['text'],
                                 name = channel))

barerr_traces

barerr_layout = go.Layout(title ='Bar & Error Bar (Offline)', 
                           xaxis =dict(title= 'Year'),
                            yaxis = dict(title = 'Revenue(Mean)',
                                        range= [0, ymax]))

barerr_fig = go.Figure(barerr_traces, barerr_layout) 
barerr_fig.show()

# +
# Radar Chart
# -

rader_df = duckdb.query('select *, case when revenue>=70000000 then 5 when revenue>=50000000 then 4 when revenue>=30000000 then 3 when revenue>=10000000 then 2 else 1 end as rank from(select year, category, sum(revenue) as revenue from saledata group by year, category order by year)').df()

rader_df

# +
# 2020

# +
rader20=rader_df[rader_df['year']==2020].copy()

ranks=list(rader20['rank'])
ranks.append(ranks[0])

thetas = list(rader20['Category'])
thetas.append(thetas[0])
# -

rader_trace = go.Scatterpolar(r = ranks,
                            theta= thetas,
                            fill ='toself', 
                            name = '2020')
rader_data = [rader_trace]
rader_layout = go.Layout(title = 'Radar Chart') 
rader_fig = go.Figure(rader_data, rader_layout)
rader_fig.show()

# +
# All years
# -

years = list(rader_df['year'].unique())

years.sort()

raders_traces=[]

for year in years:
    data = rader_df[rader_df['year']==year]
    ranks = list(data['rank'])
    ranks.append(ranks[0])
    raders_thetas = list(data['Category'])
    raders_thetas.append(raders_thetas[0])
    raders_traces.append(go.Scatterpolar(r = ranks,
                                         theta = raders_thetas,
                                         name = str(year)))

raders_layout = go.Layout(title = 'Radar Chart, years',
                         legend_orientation = 'h',
                         legend = dict(x=0.3,y=-0.1),
                         polar={'radialaxis': {'visible': True}})

raders_fig=go.Figure(raders_traces, raders_layout)
raders_fig.show()

# +
# Indicator

# +
indi_trace1=go.Indicator(value= 200, # gauge type
                        delta = dict(reference = 160),
                        gauge =dict(axis =dict(visible= False)), # 눈금생략
                        domain = dict(row = 0, column = 0)) 

indi_trace2 =go.Indicator(value = 120,
                        gauge = dict(shape = 'bullet'), # 총알 모양
                        domain = dict(x = [0.05, 0.5], 
                                      y= [0.15, 0.35])) 

indi_trace3 =go.Indicator(mode= 'number+delta',
                        value =300,
                        domain = dict(row = 0, column = 1))
indi_trace4 =go.Indicator(mode= 'delta', 
                         value = 40,
                        domain= dict(row= 1, column= 1)) 

indi_data=[indi_trace1, indi_trace2, indi_trace3, indi_trace4]
# -

indi_layout = go.Layout(grid ={'rows': 2, 'columns' :2, 'pattern' :'independent'}, 
                        template ={'data': {'indicator':
                                            [{'title': {'text': 'Speed'},
                                              'mode':'number+delta+gauge', 
                                              'delta' : {'reference' : 90}}]}})

indi_fig =go.Figure(indi_data, indi_layout) 
indi_fig.show()

# Generating Margin
saledata['Margin'] = saledata['Revenue'] - saledata['Cost']


saledata.head(3)

saledata20 = saledata[saledata['year']==2020].copy()

saledata20.head(3)

indi_margin20 = round(saledata20.loc[:, ['Revenue', 'Margin']].sum()/1000000, 2)

indi_margin20

# +
indi_values =indi_margin20['Revenue'] 
indi_deltas=indi_margin20['Revenue'] - indi_margin20['Margin']

indi_trace = go.Indicator(mode ='number+delta', # 출력방식 
                          value = indi_values,        # 주요값 입력
                          number = dict(prefix = '$', # 주요값 앞 문자열
                                        suffix = 'M', # 주요값뒤문자열 
                                        valueformat = ',0f'),  # 값 형식
                          delta = dict(reference = indi_deltas, # 차이값입력
                                        valueformat = '.2f', # 값 형식
                                        relative = False,
                                        increasing =dict(color = 'blue'), 
                                        position = 'top'))


# -

indi_layout =go.Layout(title ='Indicator - Revenue & Margin',
                       paper_bgcolor ='white')
indi_fig = go.Figure(indi_trace, indi_layout) 
indi_fig.show()

# +
# Bubble Maps
# -

saledata20.head(3)

bubble_df = duckdb.query('select Country, sum(Revenue) as Revenue, Longitude, Latitude, Code3 from saledata20 group by Country,Longitude, Latitude, Code3').df()

# +
#bubble_df['Revenue']=bubble_df['Revenue'].astype(str) 
# -

bubble_df.head(8)

bubble_df['text'] = bubble_df['Country'] + ' - Total Revenue : ' + round(bubble_df['Revenue']/100000,1).astype(str) +'M'

bubble_df.head(7)

# +
bubble_trace = go.Scattergeo(lat = bubble_df['Latitude'],   # 위도
                             lon = bubble_df['Longitude'],  # 경도
                             mode = 'markers',              # 산점도
                             marker = dict(symbol='circle',  # 원형
                                            size = np.sqrt(bubble_df['Revenue']/10000)), 
                             text = bubble_df['text'], # hover text 활성화
                             hoverinfo ='text') # 입력한text만활성화

bubble_layout = go.Layout(title = 'Bubble Maps',
                          geo= dict(scope= 'world',
                          projection_type = 'equirectangular',
                          showcountries=True)) # 국가경계선

# -

bubble_fig = go.Figure(bubble_trace, bubble_layout) 
bubble_fig.show()

# +
# Choropleth Map, with color bar

# +
Choro_trace = go.Choropleth(locations = bubble_df['Code3'],  # 국가코드(영역)
                              z = bubble_df['Revenue'],        # 영역내표현값
                              colorscale = 'Blues',            # 영역 색상
                              reversescale = True,             # 컬러바 scale 반대
                              marker_line_color = 'darkgray',  # 영역테두리색상
                              marker_line_width = 0.5,         # 영역테두리두께 
                              colorbar_tickprefix = '$',       # 컬러바축문자열
                              colorbar_title = 'RevenueUS$')    # 컬러바 제목

Choro_layout = go.Layout(title = 'Choropleth Maps',
                        geo=dict(scope ='world',
                                 projection_type ='equirectangular',
                                 showframe = False, # 지도테두리
                                 showcoastlines = False))# 해안경계선
# -

Choro_fig = go.Figure(Choro_trace, Choro_layout) 
Choro_fig.show()

import jupyter_dash

import dash_html_components as html 
import dash_core_components as dec
from dash.dependencies import Input, Output

app = dash.Dash()

server = app.server                 # server 정의 

app.layout = html.Div(dcc.Graph())  # Layout 정의


# +
@app.callback(Output(id, property),     # Callback 정의
                Input( id, property )) 

def callbackfunction(input_value):      # Callback function 정의   
    go.Figure()                         # graph 
    return output_value


# -

if __name__ =='__main__':               # app launch
    app.run_server(debug = False)





# !pip install gunicorn





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
