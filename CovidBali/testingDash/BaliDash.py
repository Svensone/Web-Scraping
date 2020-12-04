

### Working with bees

## not with Bali choropleth - maybe featureidkey not working
## working in scrapy env - updating dash ?


import pandas as pd
import plotly.express as px  

import json
import numpy as np

import dash  
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output

## initialise App

app = dash.Dash(__name__)

# ------------------------------------------------------------------------------
## 1. Data 
# ------------------------------------------------------------------------------
# Import and clean data (importing csv into pandas)

## 1.1. Get the data
# Import and clean data (importing csv into pandas)

##. 1 GeoJSON
path_geojson = r'C:\Users\ansve\Coding\Projects-WebScraping\CovidBali\testingPlotlyIndoStates\indo_level1_id.geojson'
indo_states = json.load(open(path_geojson, 'r'))

indo_states_map = {}

for state in indo_states['features']:
    indo_states_map[state['properties']['ADM1_EN']] = state['id']

## 2. get covid data on province level
path_csv = r'C:\Users\ansve\Coding\Projects-WebScraping\CovidBali\testingDash\OwnCode\indo-cases.csv'
df = pd.read_csv(path_csv)
df.head()

## adjust names in df to match names in indo_states_map
df = df.replace('Bangka Belitung', 'Kepulauan Bangka Belitung')
df = df.replace("DKI Jakarta", 'Dki Jakarta')

## drop row 'Indonesia' 
df = df.drop(index=34)
## add column id with 'ids' from indo-state-map list
df['id'] = df['Provinsi'].apply(lambda x: indo_states_map[x])

# ------------------------------------------------------------------------------
## 2. App Layout
# ------------------------------------------------------------------------------

app.layout = html.Div([
    html.H1('First Pimmel-Web Application with Dash and Plotly', style={'text-align': 'center'}),

    dcc.Dropdown(id= 'state',
    options = [
        {'label': "Tabanan", 'value': 'Tabanan'},
        {'label': "Jembrana", 'value': 'Jembrana'},
        {'label': "Badung", 'value': 'Badung'},
        {'label': "Buleleng", 'value': 'Buleleng'},
        {'label': "Denpasar", 'value': 'Denpasar'},
    ],
    multi=False,
    value='Jembrana',
    style={'width': '40%'}
    ),

    html.Div(id = 'output_containter', children=[]),
    html.Br(),

    dcc.Graph(id='indo_choropleth', figure={}),

])

# # ------------------------------------------------------------------------------
# ## 3. Connect Layout with Callback
# # ------------------------------------------------------------------------------

# use callback to connect to App Layout and get Inputs from Layout and define Output
@app.callback([
    Output(component_id = 'output_containter', component_property='children'),
    Output(component_id = 'indo_choropleth', component_property = 'figure')],
    [Input(component_id = 'state', component_property = 'value')]
)

def update_graph(option_selected):
    # good practice to print out args from Input
    print(option_selected)
    print(type(option_selected))

    # Output for the Info Div
    container = 'The regency that was chosen by user is {}'.format(option_selected)

    # px Choropleth figure with Input and px.choropleth
    ## Option 1 : using featureidkey

    fig = px.choropleth(df, geojson=indo_states, color="Kasus_Posi",
                    locations="id",
                    projection="mercator"
                   )
    fig.update_geos(fitbounds="locations", visible=False)
    fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0})

    return container, fig

# ------------------------------------------------------------------------------
## 4. Run App
# ------------------------------------------------------------------------------

if __name__=='__main__':
    app.run_server(debug=True)