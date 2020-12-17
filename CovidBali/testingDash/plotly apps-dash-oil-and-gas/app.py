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

app = dash.Dash(
    __name__, meta_tags=[{"name": "viewport", "content": "width=device-width"}]
)
server = app.server

# Create controls
## own controls for Bali_Covid Dash-App
regency_options = [
    {'label': str(REGENCIES[x]), 'value': str(REGENCIES[x])} for x in REGENCIES
]

## from template (old)
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
                                "height": "100px",
                                "width": "auto",
                                "margin-bottom": "25px",
                            },
                        )
                    ],
                    className="one-third column",
                ),
                html.Div(
                    [
                        html.Div(
                            [
                                html.H3(
                                    "Covid Cases",
                                    style={"margin-bottom": "0px"},
                                ),
                                html.H5(
                                    "Cases in Bali per Regency", style={"margin-top": "0px"}
                                ),
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
            style={"margin-bottom": "25px"},
        ),

        
        html.Div(
            [
                # Controls Panel Component
                # ------------------------------
                html.Div(
                    [
                        html.P(
                            " Which Region:",
                            className='control_label'
                        ),
                        dcc.RadioItems(
                            id='region_selector',
                            options=[
                                {'label': 'Bali', 'value': 'bali'},
                                {'label': 'Indonesia', 'value': 'indo'},
                                {'label': 'Germany', 'value': 'ger'}
                            ],
                            labelStyle={"display": "inline-block"},
                            value="bali",
                            className="dcc_control",
                        ),
                        html.P(
                            "Filter by date (or select range in histogram):",
                            className="control_label",
                        ),
                        dcc.RangeSlider(
                            id="year_slider",
                            min=1960,
                            max=2017,
                            value=[1990, 2010],
                            className="dcc_control",
                        ),
                        dcc.Checklist(
                            id="lock_selector",
                            options=[{"label": "Lock camera", "value": "locked"}],
                            className="dcc_control",
                            value=[],
                        ),

                        html.P("Filter by Cases:", className="control_label"),
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

                        html.P("Filter by Regency:",
                               className="control_label"),
                        dcc.RadioItems(
                            id="well_type_selector",
                            options=[
                                {"label": "All ", "value": "all"},
                                {"label": "Jembrana", "value": "productive"},
                                {"label": "Denpasar ", "value": "custom"},
                            ],
                            value="productive",
                            labelStyle={"display": "inline-block"},
                            className="dcc_control",
                        ),
                        dcc.Dropdown(
                            id="well_types",
                            options= regency_options,       #well_type_options,
                            multi=True,
                            value= list(REGENCIES.values()),          #list(WELL_TYPES.keys()),
                            className="dcc_control",
                        ),
                    ],
                    className="pretty_container four columns",
                    id="cross-filter-options",
                ),

                # Data & Graphs Components
                # ------------------------------
                html.Div(
                    [
                        html.Div(
                            [
                                html.Div(
                                    [html.H6(id="well_text"),
                                     html.P("Mortality Rate")],
                                    id="wells",
                                    className="mini_container",
                                ),
                                html.Div(
                                    [html.H6(id="gasText"), html.P("Gas")],
                                    id="gas",
                                    className="mini_container",
                                ),
                                html.Div(
                                    [html.H6(id="oilText"), html.P("Oil")],
                                    id="oil",
                                    className="mini_container",
                                ),
                                html.Div(
                                    [html.H6(id="waterText"), html.P("Water")],
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
                            style={"minHeight": "60vh"},
                            className="pretty_container",
                        ),
                    ],
                    id="right-column",
                    className="eight columns",
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
                                style={'max-width': '100%',
                                       'max-height': '100%',
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


def filter_dataframe(df, well_statuses, well_types, year_slider):
    dff = df[
        df["Well_Status"].isin(well_statuses)
        & df["Well_Type"].isin(well_types)
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

# @app.callback(
#     Output("aggregate_data", "data"),
#     [Input("year_slider", "value"),],
# )
# def update_production_text(year_slider):
#     dff = filter_dataframe(df, well_statuses, well_types, year_slider)
#     selected = dff["API_WellNo"].values
#     index, gas, oil, water = produce_aggregate(selected, year_slider)
#     return [human_format(sum(gas)), human_format(sum(oil)), human_format(sum(water))]


# # Radio -> multi
# @app.callback(
#     Output("well_statuses", "value"), [Input("well_status_selector", "value")]
# )
# def display_status(selector):
#     if selector == "all":
#         return list(WELL_STATUSES.keys())
#     elif selector == "active":
#         return ["AC"]
#     return []


# # Radio -> multi
# @app.callback(Output("well_types", "value"), [Input("well_type_selector", "value")])
# def display_type(selector):
#     if selector == "all":
#         return list(WELL_TYPES.keys())
#     elif selector == "productive":
#         return ["GD", "GE", "GW", "IG", "IW", "OD", "OE", "OW"]
#     return []


# Slider -> count graph
# @app.callback(Output("year_slider", "value"), [Input("count_graph", "selectedData")])
# def update_year_slider(count_graph_selected):

#     if count_graph_selected is None:
#         return [1990, 2010]

#     nums = [int(point["pointNumber"]) for point in count_graph_selected["points"]]
#     return [min(nums) + 1960, max(nums) + 1961]


## Selectors -> well text
@app.callback(
    Output("well_text", "children"),
    [
        Input('well_types', 'value'),
        Input('region_selector', 'value'),

    ],
)
def update_well_text(regency, region):
    print(regency)
    print(region)

    if region =='bali':
        df = pd.read_excel(r'C:\Users\ansve\Coding\Projects-WebScraping\CovidBali\testingDash\plotly apps-dash-oil-and-gas\data\regencyCasesBali.xlsx')
         
    elif region == 'indo':
        df = pd.read_csv(r'C:\Users\ansve\Coding\Projects-WebScraping\CovidBali\testingDash\plotly apps-dash-oil-and-gas\data\indo_province_cases.csv')
        
    else:
        df = pd.read_csv(PATH.joinpath(r'C:\Users\ansve\Coding\Projects-WebScraping\CovidBali\testingDash\plotly apps-dash-oil-and-gas\data\county_covid_BW.csv'))
        
    df_1 = df[df['Regency'].str.match(regency)]
    return df['mortality_rate'][0]


# @app.callback(
#     [
#         Output("gasText", "children"),
#         Output("oilText", "children"),
#         Output("waterText", "children"),],
#     [Input("aggregate_data", "data")],
# )
# def update_text(data):
#     return data[0] + " mcf", data[1] + " bbl", data[2] + " bbl"


# Selectors -> main graph
@app.callback(
    Output("main_graph", "figure"),
    [
        Input("year_slider", "value"),
        Input('region_selector', 'value')
    ],
    [
        State("lock_selector", "value"),
        State("main_graph", "relayoutData")],
)
def make_main_figure(year_value, region, selector,  main_graph_layout):  
    print(region)
    print(year_value)
    print(main_graph_layout)    
    
    PATH = pathlib.Path(__file__).parent
    # zoom, center = controls.zoom_center(lons=[5, 10, 25, 30, 35, 40, 45, 50, 100, 115], lats=[0, 15, 20, 35, 45, 50])
    
    if region =='bali':
        df = pd.read_excel(r'C:\Users\ansve\Coding\Projects-WebScraping\CovidBali\testingDash\plotly apps-dash-oil-and-gas\data\regencyCasesBali.xlsx')
        geojson = json.load(open(r'C:\Users\ansve\Coding\Projects-WebScraping\CovidBali\testingDash\plotly apps-dash-oil-and-gas\data\bali_geojson_id.geojson', 'r'))
        center = {"lat": -8.5002, "lon": 115.0129}
        zoom=7
    
    elif region == 'indo':
        df = pd.read_csv(r'C:\Users\ansve\Coding\Projects-WebScraping\CovidBali\testingDash\plotly apps-dash-oil-and-gas\data\indo_province_cases.csv')
        geojson = json.load(open(r'C:\Users\ansve\Coding\Projects-WebScraping\CovidBali\testingDash\plotly apps-dash-oil-and-gas\data\indo_level1_id.geojson', 'r'))
        center = {'lat': 0, 'lon': 105}
        zoom = 2
    
    else:
        df = pd.read_csv(PATH.joinpath(r'C:\Users\ansve\Coding\Projects-WebScraping\CovidBali\testingDash\plotly apps-dash-oil-and-gas\data\county_covid_BW.csv'))
        geojson = json.load(open(r'C:\Users\ansve\Coding\Projects-WebScraping\CovidBali\testingDash\plotly apps-dash-oil-and-gas\data\geojson_ger.json', 'r'))
        center = {"lat": 48.5002, "lon": 9.0129}
        zoom = 6

    fig = px.choropleth_mapbox(
        df,
        geojson=geojson,
        locations='id',
        color='cases_per_100k',
        mapbox_style='carto-positron',
        # hover_name='Regency',
        # hover_data=['new cases total', 'total cases'],
        # animation_frame="Date",
        color_continuous_scale='blues',
        zoom= zoom,
        center= center,
        opacity=0.5,
    )

    fig.update_geos(fitbounds="locations", visible=False)
    fig.update_layout(margin={"r": 0, "t": 0, "l": 0, "b": 0})
    display_fig = go.Figure(fig)

    # Original Figure
    # dff = filter_dataframe(df, well_statuses, well_types, year_slider)

    # traces = []
    # for well_type, dfff in dff.groupby("Well_Type"):
    #     trace = dict(
    #         type="scattermapbox",
    #         lon=dfff["Surface_Longitude"],
    #         lat=dfff["Surface_latitude"],
    #         text=dfff["Well_Name"],
    #         customdata=dfff["API_WellNo"],
    #         name=WELL_TYPES[well_type],
    #         marker=dict(size=4, opacity=0.6),
    #     )
    #     traces.append(trace)

    # relayoutData is None by default, and {'autosize': True} without relayout action
    if main_graph_layout is not None and selector is not None and "locked" in selector:
        if "mapbox.center" in main_graph_layout.keys():
            lon = float(main_graph_layout["mapbox.center"]["lon"])
            lat = float(main_graph_layout["mapbox.center"]["lat"])
            zoom = float(main_graph_layout["mapbox.zoom"])
            layout["mapbox"]["center"]["lon"] = lon
            layout["mapbox"]["center"]["lat"] = lat
            layout["mapbox"]["zoom"] = zoom

    # figure = dict(data=traces, layout=layout)
    return display_fig


# # Main graph -> individual graph
# @app.callback(Output("individual_graph", "figure"), [Input("main_graph", "hoverData")])
# def make_individual_figure(main_graph_hover):

#     layout_individual = copy.deepcopy(layout)

#     if main_graph_hover is None:
#         main_graph_hover = {
#             "points": [
#                 {"curveNumber": 4, "pointNumber": 569, "customdata": 31101173130000}
#             ]
#         }

#     chosen = [point["customdata"] for point in main_graph_hover["points"]]
#     index, gas, oil, water = produce_individual(chosen[0])

#     if index is None:
#         annotation = dict(
#             text="No data available",
#             x=0.5,
#             y=0.5,
#             align="center",
#             showarrow=False,
#             xref="paper",
#             yref="paper",
#         )
#         layout_individual["annotations"] = [annotation]
#         data = []
#     else:
#         data = [
#             dict(
#                 type="scatter",
#                 mode="lines+markers",
#                 name="Gas Produced (mcf)",
#                 x=index,
#                 y=gas,
#                 line=dict(shape="spline", smoothing=2, width=1, color="#fac1b7"),
#                 marker=dict(symbol="diamond-open"),
#             ),
#             dict(
#                 type="scatter",
#                 mode="lines+markers",
#                 name="Oil Produced (bbl)",
#                 x=index,
#                 y=oil,
#                 line=dict(shape="spline", smoothing=2, width=1, color="#a9bb95"),
#                 marker=dict(symbol="diamond-open"),
#             ),
#             dict(
#                 type="scatter",
#                 mode="lines+markers",
#                 name="Water Produced (bbl)",
#                 x=index,
#                 y=water,
#                 line=dict(shape="spline", smoothing=2, width=1, color="#92d8d8"),
#                 marker=dict(symbol="diamond-open"),
#             ),
#         ]
#         layout_individual["title"] = dataset[chosen[0]]["Well_Name"]

#     figure = dict(data=data, layout=layout_individual)
#     return figure


# # Selectors, main graph -> aggregate graph
# @app.callback(
#     Output("aggregate_graph", "figure"),
#     [
#         Input("year_slider", "value"),
#         # Input("main_graph", "hoverData"),
#     ],
# )
# def make_aggregate_figure(year_slider): #, main_graph_hover , well_statuses, well_types,

#     layout_aggregate = copy.deepcopy(layout)

#     if main_graph_hover is None:
#         main_graph_hover = {
#             "points": [
#                 {"curveNumber": 4, "pointNumber": 569, "customdata": 31101173130000}
#             ]
#         }

#     chosen = [point["customdata"] for point in main_graph_hover["points"]]
#     well_type = dataset[chosen[0]]["Well_Type"]
#     dff = filter_dataframe(df, well_statuses, well_types, year_slider)

#     selected = dff[dff["Well_Type"] == well_type]["API_WellNo"].values
#     index, gas, oil, water = produce_aggregate(selected, year_slider)

#     data = [
#         dict(
#             type="scatter",
#             mode="lines",
#             name="Gas Produced (mcf)",
#             x=index,
#             y=gas,
#             line=dict(shape="spline", smoothing="2", color="#F9ADA0"),
#         ),
#         dict(
#             type="scatter",
#             mode="lines",
#             name="Oil Produced (bbl)",
#             x=index,
#             y=oil,
#             line=dict(shape="spline", smoothing="2", color="#849E68"),
#         ),
#         dict(
#             type="scatter",
#             mode="lines",
#             name="Water Produced (bbl)",
#             x=index,
#             y=water,
#             line=dict(shape="spline", smoothing="2", color="#59C3C3"),
#         ),
#     ]
#     layout_aggregate["title"] = "Aggregate: " + WELL_TYPES[well_type]

#     figure = dict(data=data, layout=layout_aggregate)
#     return figure


# # Selectors, main graph -> pie graph
# @app.callback(
#     Output("pie_graph", "figure"),
#     [
#         # Input("well_statuses", "value"),
#         # Input("well_types", "value"),
#         Input("year_slider", "value"),
#     ],
# )
# def make_pie_figure(well_statuses, well_types, year_slider):

#     layout_pie = copy.deepcopy(layout)

#     dff = filter_dataframe(df, well_statuses, well_types, year_slider)

#     selected = dff["API_WellNo"].values
#     index, gas, oil, water = produce_aggregate(selected, year_slider)

#     aggregate = dff.groupby(["Well_Type"]).count()

#     data = [
#         dict(
#             type="pie",
#             labels=["Gas", "Oil", "Water"],
#             values=[sum(gas), sum(oil), sum(water)],
#             name="Production Breakdown",
#             text=[
#                 "Total Gas Produced (mcf)",
#                 "Total Oil Produced (bbl)",
#                 "Total Water Produced (bbl)",
#             ],
#             hoverinfo="text+value+percent",
#             textinfo="label+percent+name",
#             hole=0.5,
#             marker=dict(colors=["#fac1b7", "#a9bb95", "#92d8d8"]),
#             domain={"x": [0, 0.45], "y": [0.2, 0.8]},
#         ),
#         dict(
#             type="pie",
#             labels=[WELL_TYPES[i] for i in aggregate.index],
#             values=aggregate["API_WellNo"],
#             name="Well Type Breakdown",
#             hoverinfo="label+text+value+percent",
#             textinfo="label+percent+name",
#             hole=0.5,
#             marker=dict(colors=[WELL_COLORS[i] for i in aggregate.index]),
#             domain={"x": [0.55, 1], "y": [0.2, 0.8]},
#         ),
#     ]
#     layout_pie["title"] = "Production Summary: {} to {}".format(
#         year_slider[0], year_slider[1]
#     )
#     layout_pie["font"] = dict(color="#777777")
#     layout_pie["legend"] = dict(
#         font=dict(color="#CCCCCC", size="10"), orientation="h", bgcolor="rgba(0,0,0,0)"
#     )

#     figure = dict(data=data, layout=layout_pie)
#     return figure


# Selectors -> count graph
@app.callback(
    Output("count_graph", "figure"),
    [
        Input("year_slider", "value"),
    ],
)
def make_count_figure(year_slider):

    data_path = r'C:\Users\ansve\Coding\Projects-WebScraping\CovidBali\testingDash\plotly apps-dash-oil-and-gas\data\covid_19_indonesia_time_series_all.csv'

    df_indo = pd.read_csv(data_path)
    df_bali = df_indo[df_indo['Location'].str.match('Bali')]
    df_test = df_bali.tail(20)
    days = df_test.Date.to_list()

    fig = go.Figure()

    selected_list = ['New Cases', 'New Deaths',
                     'New Recovered', 'New Active Cases', ]
    colors = px.colors.sequential.Blues
    count = 0

    for selected in selected_list:
        count += 2
        fig.add_traces(
            go.Bar(
                x=days,
                y=df_test[selected],
                name=selected,
                marker_color=colors[count]
            )
        )
    fig.update_layout(

        title='Daily Cases in Bali',
        xaxis_tickfont_size=14,
        yaxis=dict(
            title='oh',
            titlefont_size=16,
            tickfont_size=14,
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

    # layout_count = copy.deepcopy(layout)

    # dff = filter_dataframe(df, well_statuses, well_types, [1960, 2017])
    # g = dff[["API_WellNo", "Date_Well_Completed"]]
    # g.index = g["Date_Well_Completed"]
    # g = g.resample("A").count()

    # colors = []
    # for i in range(1960, 2018):
    #     if i >= int(year_slider[0]) and i < int(year_slider[1]):
    #         colors.append("rgb(123, 199, 255)")
    #     else:
    #         colors.append("rgba(123, 199, 255, 0.2)")

    # data = [
    #     dict(
    #         type="scatter",
    #         mode="markers",
    #         x=g.index,
    #         y=g["API_WellNo"] / 2,
    #         name="All Wells",
    #         opacity=0,
    #         hoverinfo="skip",
    #     ),
    #     dict(
    #         type="bar",
    #         x=g.index,
    #         y=g["API_WellNo"],
    #         name="All Wells",
    #         marker=dict(color=colors),
    #     ),
    # ]

    # layout_count["title"] = "Completed Wells/Year"
    # layout_count["dragmode"] = "select"
    # layout_count["showlegend"] = False
    # layout_count["autosize"] = True

    # figure = dict(data=data, layout=layout_count)
    # return figure


# Main
if __name__ == "__main__":
    app.run_server(debug=True)
