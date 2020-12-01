import pandas as pd
import plotly.express as px  # (version 4.7.0)

import dash  # (version 1.12.0) pip install dash
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




# ------------------------------------------------------------------------------
## 2. App Layout
# ------------------------------------------------------------------------------

app.layout = html.Div([
    html.H1('First Web Application with Dash and Plotly', style={'text-align': 'center'}),

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
    Output(component_id = 'output_container', component_property='children'),
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
    fig = px.choropleth_mapbox(df, 
        geojson=indo_geojson, 
        color= 'Kasus_Meni', 
        locations='ADM1_PCODE', 
        featureidkey='properties.ADM1_PCODE',
        hover_name= 'Provinsi', 
        hover_data=['Kasus_Posi', 'Kasus_Meni'], 
        title='Covid Cases in Indonesia per Province',
        mapbox_style = 'carto-positron',
        zoom = 3,
        opacity=0.5,
    )

    return container, fig

# ------------------------------------------------------------------------------
## 4. Run App
# ------------------------------------------------------------------------------

if __name__=='__main__':
    app.run_server(debug=True)