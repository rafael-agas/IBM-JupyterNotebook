#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import dash
from dash import dcc
from dash import html
from dash.dependencies import Input, Output
import pandas as pd
import plotly.graph_objs as go
import plotly.express as px

# Load the data using pandas
data = pd.read_csv('https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/IBMDeveloperSkillsNetwork-DV0101EN-SkillsNetwork/Data%20Files/historical_automobile_sales.csv')

# Initialize the Dash app
app = dash.Dash(__name__)

# Set the title of the dashboard
app.title = "Automobile Statistics Dashboard"

#---------------------------------------------------------------------------------
# Create the dropdown menu options
dropdown_options = [
    {'label': 'Yearly Statistics', 'value': 'Yearly Statistics'},
    {'label': 'Recession Period Statistics', 'value': 'Recession Period Statistics'}
]
# List of years 
year_list = [i for i in range(1980, 2024, 1)]
#---------------------------------------------------------------------------------------
# Create the layout of the app
app.layout = html.Div([
    #TASK 2.1 Add title to the dashboard
    html.H1("Automobile Statisitcs Dashboard",
            style ={'textAlign':'left','color':'#00000','font-size':24}),#May include style for title
    html.Div([#TASK 2.2: Add two dropdown menus
        dcc.Dropdown(
                        id='dropdown-statistics',
                        options=dropdown_options,
                        value=[option['value'] for option in dropdown_options],
                        placeholder="Select Statistics",
                        style={'padding': 3, 'font-size': 20, 'textAlignLast': 'center'}
                    )
    ]),
    html.Div(dcc.Dropdown(
            id='select-year',
            options=[{'label': i, 'value': i} for i in year_list],
            placeholder='Select Year',
            value=year_list[0]
        )),
    html.Div([#TASK 2.3: Add a division for output display
    html.Div(id='output-container', className='chart-grid', style={'display':'flex'}),])
])
#TASK 2.4: Creating Callbacks
# Define the callback function to update the input container based on the selected statistics
@app.callback(
    Output(component_id='select-year', component_property='disabled'),
    Input(component_id='dropdown-statistics',component_property='value'))

def update_input_container(selected_statistics):
    if selected_statistics =='Yearly Statistics': 
        return False
    else: 
        return True
#Callback for plotting
# Define the callback function to update the input container based on the selected statistics
@app.callback(
    Output(component_id='output-container', component_property='children'),
    [Input(component_id='dropdown-statistics', component_property='value'),
     Input(component_id='select-year', component_property='value')])
def update_output_container(selected_statistics, selected_year):
    if selected_statistics == 'Recession Period Statistics':
        # Filter the data for recession periods
        recession_data = data[data['Recession'] == 1]

        # Plot 1: Automobile sales fluctuate over Recession Period (year-wise)
        yearly_rec = recession_data.groupby('Year')['Automobile_Sales'].mean().reset_index()
        R_chart1 = dcc.Graph(
            figure=px.line(yearly_rec, x='Year', y='Automobile_Sales', title="Average Automobile Sales fluctuation over Recession Period")
        )

        # Plot 2: Calculate the average number of vehicles sold by vehicle type
        average_sales = recession_data.groupby('Vehicle_Type')['Automobile_Sales'].mean().reset_index()
        R_chart2 = dcc.Graph(
            figure=px.line(average_sales, x='Vehicle_Type', y='Automobile_Sales', title='Average Vehicle Type Sold during Recession Periods')
        )

        # Plot 3: Pie chart for total expenditure share by vehicle type during recessions
        exp_rec = recession_data.groupby('Vehicle_Type')['Advertising_Expenditure'].sum().reset_index()
        R_chart3 = dcc.Graph(
            figure=px.pie(exp_rec, values='Advertising_Expenditure', names='Vehicle_Type',
                          title='Advertising Expenditure based on Vehicle type during Recession Periods')
        )

        # Plot 4: Bar chart for the effect of unemployment rate on vehicle type and sales
        unemployment = recession_data.groupby(['unemployment_rate', 'Vehicle_Type'])['Automobile_Sales'].sum().reset_index()
        R_chart4 = dcc.Graph(
            figure=px.bar(unemployment, x='unemployment_rate', y='Automobile_Sales', color='Vehicle_Type',
                          title='Effect of Unemployment Rate on Vehicle Type and Sales')
        )

        return [
            html.Div(className='chart-item', children=[html.Div(children=R_chart1), html.Div(children=R_chart2)]),
            html.Div(className='chart-item', children=[html.Div(children=R_chart3), html.Div(children=R_chart4)])
        ]

    elif selected_statistics == 'Yearly Statistics' and selected_year:
        yearly_data = data[data['Year'] == selected_year]

        # Plot 1: Yearly Automobile sales using line chart for the whole period.
        yearly = yearly_data.groupby('Year')['Automobile_Sales'].mean().reset_index()
        Y_chart1 = dcc.Graph(figure=px.line(yearly, x='Year', y='Automobile_Sales', title='Yearly Average Automobile Sales'))

        # Plot 2: Total Monthly Automobile sales using line chart.
        Y_chart2 = dcc.Graph(figure=px.line(yearly_data, x='Month', y='Automobile_Sales', title='Monthly Average Automobile Sales'))

        # Plot 3: Bar chart for average number of vehicles sold during the given year
        avr_vdata = yearly_data.groupby('Vehicle_Type')['Automobile_Sales'].mean().reset_index()
        Y_chart3 = dcc.Graph(figure=px.bar(avr_vdata, x='Vehicle_Type', y='Automobile_Sales',
                                           title=f'Average Vehicles Sold by Vehicle Type in the year {selected_year}'))

        # Plot 4: Total Advertisement Expenditure for each vehicle using pie chart
        exp_data = yearly_data.groupby('Vehicle_Type')['Advertising_Expenditure'].sum().reset_index()
        Y_chart4 = dcc.Graph(figure=px.pie(exp_data, values='Advertising_Expenditure', names='Vehicle_Type',
                                           title=f'Total Advertising Expenditure based on Vehicle Type for the year {selected_year}'))

        return [
            html.Div(className='chart-item', children=[html.Div(Y_chart1), html.Div(Y_chart2)]),
            html.Div(className='chart-item', children=[html.Div(Y_chart3), html.Div(Y_chart4)])
        ]

    else:
        return None


# Run the Dash app
if __name__ == '__main__':
    app.run_server(debug=True)

