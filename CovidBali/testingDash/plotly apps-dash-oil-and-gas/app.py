# Import required libraries
import pickle
import copy
import pathlib
import urllib.request
import dash
import math
import datetime as dt
import pandas as pd
import json

import plotly.express as px
import plotly.graph_objects as go

from dash.dependencies import Input, Output, State, ClientsideFunction
import dash_core_components as dcc
import dash_html_components as html

# Multi-dropdown options
from controls import REGENCIES, COUNTIES, WELL_STATUSES, WELL_TYPES, WELL_COLORS
import controls


# get relative data folder
PATH = pathlib.Path(__file__).parent
DATA_PATH = PATH.joinpath("data").resolve()

# Data paths
#-----------------------------

data_covid_bali = r'C:\Users\ansve\Coding\Projects-WebScraping\CovidBali\testingDash\plotly apps-dash-oil-and-gas\data\data_process\bali_regency_data.csv'
data_covid_indo = r'C:\Users\ansve\Coding\Projects-WebScraping\CovidBali\testingDash\plotly apps-dash-oil-and-gas\data\data_process\indo_province_data.csv'
data_covid_germany = r'C:\Users\ansve\Coding\Projects-WebScraping\CovidBali\testingDash\plotly apps-dash-oil-and-gas\data\county_covid_BW.csv'
geojson_bali = r'C:\Users\ansve\Coding\Projects-WebScraping\CovidBali\testingDash\plotly apps-dash-oil-and-gas\data\bali_geojson_id.geojson'
geojson_indo = r'C:\Users\ansve\Coding\Projects-WebScraping\CovidBali\testingDash\plotly apps-dash-oil-and-gas\data\indo_level1_id.geojson'
geojson_germany = r'C:\Users\ansve\Coding\Projects-WebScraping\CovidBali\testingDash\plotly apps-dash-oil-and-gas\data\geojson_ger.json'


# Initialize App
#-----------------------------

app = dash.Dash(
    __name__, meta_tags=[{"name": "viewport", "content": "width=device-width"}]
)
server = app.server

# Create controls
#---------------------

# own controls for Bali_Covid Dash-App
regency_options = [
    {'label': str(REGENCIES[x]), 'value': str(REGENCIES[x])} for x in REGENCIES
]
# from template (old)
county_options = [
    {"label": str(COUNTIES[county]), "value": str(county)} for county in COUNTIES
]
well_status_options = [
    {"label": str(WELL_STATUSES[well_status]), "value": str(well_status)}
    for well_status in WELL_STATUSES
]
well_type_options = [
    {"label": str(WELL_TYPES[well_type]), "value": str(well_type)}
    for well_type in WELL_TYPES
]

# Create global chart template
#-----------------------------
mapbox_access_token = "pk.eyJ1IjoicGxvdGx5bWFwYm94IiwiYSI6ImNrOWJqb2F4djBnMjEzbG50amg0dnJieG4ifQ.Zme1-Uzoi75IaFbieBDl3A"

layout = dict(
    autosize=True,
    automargin=True,
    margin=dict(l=30, r=30, b=20, t=40),
    hovermode="closest",
    plot_bgcolor="#F9F9F9",
    paper_bgcolor="#F9F9F9",
    legend=dict(font=dict(size=10), orientation="h"),
    title="Satellite Overview",
    mapbox=dict(
        accesstoken=mapbox_access_token,
        style="light",
        center=dict(lon=114, lat=-8.54),
        zoom=7,
    ),
)
# Create app layout
#-----------------------------
app.layout = html.Div(
    [
        dcc.Store(id="aggregate_data"),
        # empty Div to trigger javascript file for graph resizing
        html.Div(id="output-clientside"),

        # Header Component
        # ------------------------------
        html.Div(
            [
                html.Div(
                    [
                        html.Img(
                            src=app.get_asset_url("Barong-Mask.png"),
                            id="plotly-image",
                            style={
                                "height": "80px",
                                "width": "auto",},
                        )
                    ],
                    className="one-third column",
                ),
                html.Div(
                    [
                        html.Div(
                            [
                                html.H3("Covid Cases", style={"margin-bottom": "0px"},),
                                html.H5("Cases in Bali per Regency", style={"margin-top": "0px"}),
                            ]
                        )
                    ],
                    className="one-half column",
                    id="title",
                ),
                html.Div(
                    [
                        html.A(
                            html.Button("About Me", id="learn-more-button"),
                            href="https://5cac0a0b7a48d9000a0e3c77--portfolio-gatsby-bali.netlify.app/",
                        )
                    ],
                    className="one-third column",
                    id="button",
                ),
            ],
            id="header",
            className="row flex-display",
            style={"margin-bottom": "10px"},
        ),
        html.Div(
            [
                # Controls Panel Component
                # ------------------------------
                html.Div(
                    [
                        html.P(
                            "Region:",
                            className='control_label'
                        ),
                        dcc.RadioItems(
                            id='region_selector',
                            options=[
                                {'label': 'Indonesia', 'value': 'indo'},
                                {'label': 'Bali', 'value': 'bali'},
                            ],
                            labelStyle={"display": "inline-block"},
                            value="bali",
                            className="dcc_control",
                        ),
                        html.P("Regency/County:",
                               className="control_label"),
                        dcc.Dropdown(
                            id="regency_selector",
                            options=regency_options,  # well_type_options,
                            multi=False,
                            value='',
                            className="dcc_control",
                        ),
                        html.P('NOT YET !!', className="control_label",),
                        html.P("Date or Timerange:",
                            className="control_label",
                        ),
                        dcc.RangeSlider(
                            id="year_slider",
                            min=1960,
                            max=2017,
                            value=[1990, 2010],
                            className="dcc_control",
                        ),
                        html.P("Cases:", className="control_label"),
                        dcc.RadioItems(
                            id="well_status_selector",
                            options=[
                                {"label": "All ", "value": "all"},
                                {"label": "Confirmed ", "value": "confirmed"},
                                {"label": "Deaths ", "value": "death"},
                                {"label": "Recovered ", "value": "Recovered"},
                                {"label": "Active ", "value": "active"},
                            ],
                            value="confirmed",
                            labelStyle={"display": "inline-block"},
                            className="dcc_control",
                        ),
                    ],
                    className="pretty_container three columns",
                    id="cross-filter-options",
                ),

                # Data & Graphs Components
                # ------------------------------
                html.Div(
                    [
                        html.Div(
                            [
                                html.Div(
                                    [html.H6(id="cases_mortality", style={'text-align': 'center'}), html.P("Cases per 100k"),
                                    ],
                                    id="wells",
                                    className="mini_container",
                                ),
                                html.Div(
                                    [html.H6(id="cases_per_100k"), html.P("Cases per 100k")],
                                    id="gas",
                                    className="mini_container",
                                ),
                                html.Div(
                                    [html.H6(id="deaths_per_100k"), html.P("Deaths per 100k")],
                                    id="oil",
                                    className="mini_container",
                                ),
                                html.Div(
                                    [html.H6(id="growth_rate"), html.P("growth-rate")],
                                    id="water",
                                    className="mini_container",
                                ),
                            ],
                            id="info-container",
                            className="row container-display",
                        ),
                        html.Div(
                            [dcc.Graph(id="count_graph")],
                            id="countGraphContainer",
                            style={"minHeight": "50vh"},
                            className="pretty_container",
                        ),
                    ],
                    id="right-column",
                    className="ten columns",
                ),
            ],
            className="row flex-display",
        ),
        html.Div(
            [
                html.Div(
                    [dcc.Graph(
                        id="main_graph",
                        style={'max-width': '100%',
                               'max-height': '100%'
                               },
                    )],
                    className="pretty_container seven columns",
                ),
                html.Div(
                    [
                        # dcc.Graph(id="individual_graph")
                        html.Div(
                            html.Img(
                                src=app.get_asset_url('pic1.jpg'),
                                style={
                                    'max-width': '100%',
                                    'max-height': '100%',
                                    #    'background-size': 'cover',
                                       }))
                    ],
                    className="pretty_container five columns",
                ),
            ],
            className="row flex-display",
        ),
        # html.Div(
        #     [
        #         html.Div(
        #             [dcc.Graph(id="pie_graph")],
        #             className="pretty_container seven columns",
        #         ),
        #         html.Div(
        #             [dcc.Graph(id="aggregate_graph")],
        #             className="pretty_container five columns",
        #         ),
        #     ],
        #     className="row flex-display",
        # ),
    ],
    id="mainContainer",
    style={"display": "flex", "flex-direction": "column"},
)


# Helper functions
def human_format(num):
    if num == 0:
        return "0"

    magnitude = int(math.log(num, 1000))
    mantissa = str(int(num / (1000 ** magnitude)))
    return mantissa + ["", "K", "M", "G", "T", "P"][magnitude]


def filter_dataframe(df, well_statuses, regency_selector, year_slider):
    dff = df[
        df["Well_Status"].isin(well_statuses)
        & df["Well_Type"].isin(regency_selector)
        & (df["Date_Well_Completed"] > dt.datetime(year_slider[0], 1, 1))
        & (df["Date_Well_Completed"] < dt.datetime(year_slider[1], 1, 1))
    ]
    return dff


def produce_individual(api_well_num):
    try:
        points[api_well_num]
    except:
        return None, None, None, None

    index = list(
        range(min(points[api_well_num].keys()),
              max(points[api_well_num].keys()) + 1)
    )
    gas = []
    oil = []
    water = []

    for year in index:
        try:
            gas.append(points[api_well_num][year]["Gas Produced, MCF"])
        except:
            gas.append(0)
        try:
            oil.append(points[api_well_num][year]["Oil Produced, bbl"])
        except:
            oil.append(0)
        try:
            water.append(points[api_well_num][year]["Water Produced, bbl"])
        except:
            water.append(0)

    return index, gas, oil, water


def produce_aggregate(selected, year_slider):

    index = list(range(max(year_slider[0], 1985), 2016))
    gas = []
    oil = []
    water = []

    for year in index:
        count_gas = 0
        count_oil = 0
        count_water = 0
        for api_well_num in selected:
            try:
                count_gas += points[api_well_num][year]["Gas Produced, MCF"]
            except:
                pass
            try:
                count_oil += points[api_well_num][year]["Oil Produced, bbl"]
            except:
                pass
            try:
                count_water += points[api_well_num][year]["Water Produced, bbl"]
            except:
                pass
        gas.append(count_gas)
        oil.append(count_oil)
        water.append(count_water)

    return index, gas, oil, water


# Create callbacks
app.clientside_callback(
    ClientsideFunction(namespace="clientside", function_name="resize"),
    Output("output-clientside", "children"),
    [Input("count_graph", "figure")],
)

# Slectore -> Mini-Container Numbers
@app.callback(
    [Output("cases_mortality", "children"),
    Output('cases_per_100k', 'children'),
    Output('deaths_per_100k', 'children'),
    Output('growth_rate', 'children')],

    [Input('regency_selector', 'value'),
    Input('region_selector', 'value')],
    )
    
def update_cases_mortality(regency, region):
    if region == 'indo':
        df = pd.read_csv(data_covid_indo)
        selected_region = df[df['Name_EN'].str.match('Indonesia')]
    elif region == 'bali' and regency is None:
        df = pd.read_csv(data_covid_indo)
        selected_region = df[df['Name_EN'].str.match('Bali')]
    else:
        df = pd.read_csv(data_covid_bali)
        selected_region = df[df['Name_EN'].str.match(regency)]
    
    cfr = selected_region['CFR'].iloc[-1].round(2)
    cp100k = selected_region['total_cases_per_100k'].iloc[-2]#.round(2)
    
    dp100k = selected_region['total_deaths_per_100k'].iloc[-2] #.round(2)
    return '{}'.format(cfr), '{}'.format(str(round(cp100k, 2))), '{}'.format(str(round(dp100k, 2))), 'not yet'

# Selectors -> main graph
@app.callback(
    Output("main_graph", "figure"),
    [
        Input("year_slider", "value"),
        Input('region_selector', 'value')
    ],
    [
        State("main_graph", "relayoutData")],
)
def make_main_figure(year_value, region, main_graph_layout):
    # print(region)
    # print(year_value)
    # print(main_graph_layout)
    PATH = pathlib.Path(__file__).parent

    # zoom, center = controls.zoom_center(lons=[5, 10, 25, 30, 35, 40, 45, 50, 100, 115], lats=[0, 15, 20, 35, 45, 50])
    if region == 'bali':
        df = pd.read_csv(data_covid_indo)
        geojson = json.load(open(geojson_indo))
        center = {"lat": -8.5002, "lon": 115.0129}
        zoom = 7
    elif region == 'indo':
        df = pd.read_csv(data_covid_indo)
        geojson = json.load(open(geojson_indo))
        center = {'lat': 0, 'lon': 107}
        zoom = 2

    else:
        df = pd.read_csv(data_covid_germany)
        geojson = json.load(open(geojson_germany))
        center = {"lat": 48.5002, "lon": 9.0129}
        zoom = 6

    fig = px.choropleth_mapbox(
        df,
        geojson=geojson,
        locations='id',
        color='total_cases_per_100k',
        mapbox_style='carto-positron',
        # hover_name='Regency',
        # hover_data=[],
        # animation_frame="Date",
        color_continuous_scale='blues',
        zoom=zoom,
        center=center,
        opacity=0.5,
    )

    fig.update_geos(fitbounds="locations", visible=False)
    fig.update_layout(margin={"r": 0, "t": 0, "l": 0, "b": 0})
    display_fig = go.Figure(fig)

    # relayoutData is None by default, and {'autosize': True} without relayout action
    if main_graph_layout is not None:
        if "mapbox.center" in main_graph_layout.keys():
            lon = float(main_graph_layout["mapbox.center"]["lon"])
            lat = float(main_graph_layout["mapbox.center"]["lat"])
            zoom = float(main_graph_layout["mapbox.zoom"])
            layout["mapbox"]["center"]["lon"] = lon
            layout["mapbox"]["center"]["lat"] = lat
            layout["mapbox"]["zoom"] = zoom

    # figure = dict(data=traces, layout=layout)
    return display_fig


# Selectors -> count graph
@app.callback(
    Output("count_graph", "figure"),
    [
        Input('region_selector', 'value'),
        Input('regency_selector', 'value'),
        Input("year_slider", "value"),
    ],
)
def make_count_figure(region, regency, year_slider):

    if region == 'indo':
        df = pd.read_csv(data_covid_indo)
        region_selected = 'indonesia'

    elif region == 'bali' and regency == '':
        df = pd.read_csv(data_covid_indo)
        region_selected = 'bali'

    else:
        df = pd.read_csv(data_covid_bali)
        region_selected = regency

    df = df[df['Name_EN'].str.match(region_selected)]

    df_test = df.tail(100)
    days = df_test.Date.to_list()

    fig = go.Figure()

    selected_cases = ['total_cases',
                     ]
    colors = px.colors.sequential.Blues
    count = 0

    for selected in selected_cases:
        count += 2
        fig.add_traces(
            go.Bar(
                x=days,
                y=df_test[selected],
                name=selected,
                marker_color=colors[count]
            )
        )
    # test plots for new cases and 
    selected_new = [
        'total_cases_per_100k'
    ]
    for selected in selected_new:
        fig.add_traces(
            go.Scatter(
                x=days, 
                y=df_test[selected],
                # mode='lines',
                name=selected,
                line=dict(color=colors[3], width=4)
                )
            )

    fig.update_layout(
        title='Daily Cases {}'.format(region_selected),
        xaxis_tickfont_size=14,
        yaxis=dict(
            title='oh',
            titlefont_size=16,
            tickfont_size=10,
        ),
        plot_bgcolor=colors[0],
        paper_bgcolor=colors[0],
        legend=dict(
            x=0,
            y=1.0,
            bgcolor=colors[0],
            bordercolor='white'
        ),
        barmode='group',
        bargap=0.15,  # gap between bars of adjacent location coordinates.
        bargroupgap=0.1  # gap between bars of the same location coordinate.
    )
    return fig

# Main
if __name__ == "__main__":
    app.run_server(debug=True)
