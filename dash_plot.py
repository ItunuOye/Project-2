import dash
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
import plotly.graph_objs as go
from dash.dependencies import Input, Output
import requests, json

# df = pd.read_csv(
#     'wiki_fires_cleaned_2015-2018.csv')
year_data = requests.get("","json")
# print(type(year_data))
df = pd.read_json(year_data.content)

app = dash.Dash()

app.layout = html.Div([
    html.Div([
            dcc.Graph(id='graph-with-slider',
            hoverData={'points':[{'customdata':"San Bernardino"}] })
            ], style={'width': '49%', 'height': '550', 'display': 'inline-block', 'padding': '0.20'}),
   
    html.Div([
        dcc.Graph(id='x-time-series'),
        dcc.Graph(id='y-time-series'),
    ], style={'display': 'inline-block', 'width': '49%', 'height':'550'}),

    html.Div(
        dcc.Slider(
        id='year-slider',
        min=df['Fire Year'].min(),
        max=df['Fire Year'].max(),
        value=df['Fire Year'].min(),
        step=None,
        marks={str(Year): str(Year) for Year in df['Fire Year'].unique()}
    ), style={'width': '49%', 'padding':'0px 20px 20px 20px'})
])


@app.callback(
    dash.dependencies.Output('graph-with-slider', 'figure'),
    [dash.dependencies.Input('year-slider', 'value')])

def update_figure(selected_year):
    dff = df[df['Fire Year'] == selected_year]
    traces = []
    # create_time_series(filtered_df,title)
    for i in dff.County.unique():

        df_by_county = dff[dff['County'] == i]
        traces.append(go.Scatter(
            x=df_by_county['Number of Days'],
            y= df_by_county['Acres Burned'],
            customdata=df_by_county['County'],
            text= f"{i}, {selected_year}",
            mode='markers',
            opacity=0.7,
            marker={
                'size': 15,
                'line': {'width': 0.5, 'color': 'white'}
            },
            name=i
            ))
        
    
       
    return {
        'data': traces,
        'layout': go.Layout(
            xaxis={'type': 'linear', 'title': 'Number of Days'},
            yaxis={'title': 'Acres Burned', 'range': [0, 30000]},
            margin={'l': 40, 'b': 40, 't': 10, 'r': 10},
            hovermode='closest'
        )
    }



def create_time_series(tracesdf, title):
    return {
        'data': [go.Scatter(
            x=tracesdf['traces_year'],
            y=tracesdf['traces1'],
            mode='lines+markers'
            )],
        'layout': {
            'height': 225,
            'margin':{'l': 20, 'b':30, 'r':10, 't':10},
            'annotations': [{
                'x': 0, 'y':0.85, 'xanchor':'left', 'yanchor':'bottom', 
                'xref': 'paper', 'yref': 'paper', 'showarrow': False,
                'align': 'left', 'bgcolor': 'rgba(255, 255, 255, 0.5)',
                'text': title
            }],
            'yaxis': {'type': 'linear'},
            'xaxis': {'showgrid': False, 'title': 'Fire Year','range': [2014,2019]}
        }
         
    }
    
  
@app.callback(
    dash.dependencies.Output('x-time-series', 'figure'),
    [dash.dependencies.Input('graph-with-slider', 'hoverData'),
     dash.dependencies.Input('year-slider', 'value')]
    )
def update_y_timeseries(hoverData, selected_year):
    traces1 = []
    # print(hoverData)
    county_name = hoverData['points'][0]['customdata']
    # dff = df[df['Year'] == selected_year]
    dff = df[df['County'] == county_name]
    print(dff)
    # for i in dff.County.unique():
    
    for i in (dff["Fire Year"].unique()):
        df_by_year = dff[dff['Fire Year'] == i]
        max_acres = df_by_year['Acres Burned'].max()
        traces1.append(max_acres)
        # print(traces1)
    print(traces1)         
    title = '<b>{}</b><br>{}'.format(county_name, 'Acres')
    print(title)
    tracesyear = dff['Fire Year'].unique()
    d = {'traces_year': tracesyear, 'traces1': traces1}
    tracesdf = pd.DataFrame(d)
    print(tracesdf)
    return create_time_series(tracesdf, title)



@app.callback(
    dash.dependencies.Output('y-time-series', 'figure'),
    [dash.dependencies.Input('graph-with-slider', 'hoverData'),
     dash.dependencies.Input('year-slider', 'value')]
    )
def update_x_timeseries(hoverData, selected_year):
    traces1 = []
    county_name = hoverData['points'][0]['customdata']
    # dff = df[df['Year'] == selected_year]
    dff = df[df['County'] == county_name]
    for i in (dff['Fire Year'].unique()):
            df_by_year = dff[dff['Fire Year'] == i]
            number_days = df_by_year['Number of Days'].max()
            traces1.append(number_days)
            # print(traces1)
    print(traces1)  
    tracesyear = dff['Fire Year'].unique()
    d = {'traces_year': tracesyear, 'traces1': traces1}
    tracesdf = pd.DataFrame(d)
    print(tracesdf)   
    title = '<b>{}</b><br>{}'.format(county_name, 'Days')
    print(title)
    return create_time_series(tracesdf, title)


if __name__ == '__main__':
    app.run_server()