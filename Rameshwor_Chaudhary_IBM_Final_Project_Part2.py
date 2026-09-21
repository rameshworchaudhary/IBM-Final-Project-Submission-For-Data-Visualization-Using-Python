#!/usr/bin/env python
# coding: utf-8

# IBM Data Visualization with Python - Final Assignment Part 2
# Submitted by: Rameshwor Chaudhary
# Program: B.E. CSE (AI & ML), Chandigarh University

import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import pandas as pd
import plotly.express as px

# Load the automobile sales data
data = pd.read_csv(
    "https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/"
    "IBMDeveloperSkillsNetwork-DV0101EN-SkillsNetwork/Data%20Files/"
    "historical_automobile_sales.csv"
)

# Initialize Dash app
app = dash.Dash(__name__)
app.title = "Automobile Statistics Dashboard"

# Dropdown options
dropdown_options = [
    {"label": "Yearly Statistics Report", "value": "Yearly Statistics"},
    {"label": "Recession Period Statistics", "value": "Recession Period Statistics"}
]

year_list = [i for i in range(1980, 2024)]

# Dashboard layout
app.layout = html.Div([
    html.H1(
        "Automobile Sales Statistics Dashboard",
        style={
            "textAlign": "center",
            "color": "#503D36",
            "fontSize": 24
        }
    ),

    html.P(
        "Select a 'statistical report type' and 'Year' to create graphs",
        style={
            "textAlign": "center",
            "color": "#503D36",
            "fontSize": 18
        }
    ),

    html.Div([
        html.Label("Select Statistics:"),
        dcc.Dropdown(
            id="dropdown-statistics",
            options=dropdown_options,
            value="Recession Period Statistics",
            placeholder="Select a report type",
            style={"width": "80%", "padding": 3, "textAlign": "center",
                   "fontSize": 20}
        )
    ]),

    html.Div([
        html.Label("Select Year:"),
        dcc.Dropdown(
            id="select-year",
            options=[{"label": i, "value": i} for i in year_list],
            placeholder="Select a year",
            style={"width": "80%", "padding": 3, "textAlign": "center",
                   "fontSize": 20}
        )
    ]),

    html.Div([
        html.Div(
            id="output-container",
            className="chart-grid",
            style={"display": "flex", "flexDirection": "column"}
        )
    ])
])


# Callback to enable/disable year dropdown
@app.callback(
    Output("select-year", "disabled"),
    Input("dropdown-statistics", "value")
)
def update_input_container(selected_statistics):
    if selected_statistics == "Yearly Statistics":
        return False
    return True


# Callback to create dashboard graphs
@app.callback(
    Output("output-container", "children"),
    [
        Input("dropdown-statistics", "value"),
        Input("select-year", "value")
    ]
)
def update_output_container(selected_statistics, input_year):

    # ---------------------------------------------------------------
    # TASK 2.5: Recession Period Statistics
    # ---------------------------------------------------------------
    if selected_statistics == "Recession Period Statistics":

        recession_data = data[data["Recession"] == 1]

        # Plot 1: Average automobile sales by recession year
        yearly_rec = (
            recession_data.groupby("Year")["Automobile_Sales"]
            .mean()
            .reset_index()
        )

        R_chart1 = dcc.Graph(
            figure=px.line(
                yearly_rec,
                x="Year",
                y="Automobile_Sales",
                title="Average Automobile Sales Fluctuation over Recession Period"
            )
        )

        # Plot 2: Average automobile sales by vehicle type
        average_sales = (
            recession_data.groupby("Vehicle_Type")["Automobile_Sales"]
            .mean()
            .reset_index()
        )

        R_chart2 = dcc.Graph(
            figure=px.bar(
                average_sales,
                x="Vehicle_Type",
                y="Automobile_Sales",
                title="Average Automobile Sales by Vehicle Type during Recession Period"
            )
        )

        # Plot 3: Advertising expenditure by vehicle type
        exp_rec = (
            recession_data.groupby("Vehicle_Type")["Advertising_Expenditure"]
            .sum()
            .reset_index()
        )

        R_chart3 = dcc.Graph(
            figure=px.pie(
                exp_rec,
                values="Advertising_Expenditure",
                names="Vehicle_Type",
                title="Total Expenditures by Vehicle Type during Recession Period"
            )
        )

        # Plot 4: Automobile sales by vehicle type during recession
        unemp_rate = (
            recession_data.groupby("Vehicle_Type")["Automobile_Sales"]
            .mean()
            .reset_index()
        )

        R_chart4 = dcc.Graph(
            figure=px.bar(
                unemp_rate,
                x="Vehicle_Type",
                y="Automobile_Sales",
                title="Effects of Unemployment Rate on Automobile Sales by Vehicle Type during Recession Period"
            )
        )

        return [
            html.Div(
                className="chart-grid",
                style={"display": "flex"},
                children=[
                    html.Div(children=R_chart1, style={"width": "50%"}),
                    html.Div(children=R_chart2, style={"width": "50%"})
                ]
            ),
            html.Div(
                className="chart-grid",
                style={"display": "flex"},
                children=[
                    html.Div(children=R_chart3, style={"width": "50%"}),
                    html.Div(children=R_chart4, style={"width": "50%"})
                ]
            )
        ]

    # ---------------------------------------------------------------
    # TASK 2.6: Yearly Statistics
    # ---------------------------------------------------------------
    elif input_year and selected_statistics == "Yearly Statistics":

        yearly_data = data[data["Year"] == input_year]

        # Plot 1: Automobile sales over the complete period
        yas = (
            data.groupby("Year")["Automobile_Sales"]
            .sum()
            .reset_index()
        )

        Y_chart1 = dcc.Graph(
            figure=px.line(
                yas,
                x="Year",
                y="Automobile_Sales",
                title="Automobile Sales for the Year"
            )
        )

        # Plot 2: Monthly automobile sales
        mas = (
            yearly_data.groupby("Month")["Automobile_Sales"]
            .sum()
            .reset_index()
        )

        Y_chart2 = dcc.Graph(
            figure=px.line(
                mas,
                x="Month",
                y="Automobile_Sales",
                title="Total Automobile Sales by Month"
            )
        )

        # Plot 3: Average vehicles sold by vehicle type
        avr_vdata = (
            yearly_data.groupby("Vehicle_Type")["Automobile_Sales"]
            .mean()
            .reset_index()
        )

        Y_chart3 = dcc.Graph(
            figure=px.bar(
                avr_vdata,
                x="Vehicle_Type",
                y="Automobile_Sales",
                title=f"Average Vehicles Sold by Vehicle Type in the year {input_year}"
            )
        )

        # Plot 4: Advertising expenditure by vehicle type
        exp_data = (
            yearly_data.groupby("Vehicle_Type")["Advertising_Expenditure"]
            .sum()
            .reset_index()
        )

        Y_chart4 = dcc.Graph(
            figure=px.pie(
                exp_data,
                values="Advertising_Expenditure",
                names="Vehicle_Type",
                title="Total Advertising Expenditure by Vehicle Type"
            )
        )

        return [
            html.Div(
                className="chart-grid",
                style={"display": "flex"},
                children=[
                    html.Div(children=Y_chart1, style={"width": "50%"}),
                    html.Div(children=Y_chart2, style={"width": "50%"})
                ]
            ),
            html.Div(
                className="chart-grid",
                style={"display": "flex"},
                children=[
                    html.Div(children=Y_chart3, style={"width": "50%"}),
                    html.Div(children=Y_chart4, style={"width": "50%"})
                ]
            )
        ]

    return None


if __name__ == "__main__":
    # Compatible with current Dash versions.
    app.run(debug=True)
