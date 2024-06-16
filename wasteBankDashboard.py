import requests
import pandas as pd
import plotly.express as px
import plotly.graph_objs as go
from dash import Dash, dcc, html

# Fetch data from the URL
privateKey = 'a8b3e6d4eaee404ba7b32cd80110a2eb'
url = "https://script.google.com/macros/s/AKfycbwqznIpOsEC_cPAe4pTy4pEQBN5MaksSaIy0IL8kganMDDeDYchgsebQb1yeEoSpxet/exec?api=sampah&apiKey=" + privateKey

response = requests.get(url)
data = response.json()
df = pd.DataFrame(data['data'])

# Initialize the Dash app
app = Dash(__name__)


"""
    Total Revenue and Total Waste
    Scorecard Text
"""
total_revenue = df['price'].sum()
total_waste = df['weight'].sum()


""" 
    Top 5 Waste Type
    Horizontal Bar Chart
"""
wasteType_sum = df.groupby('wasteType')['weight'].count().reset_index()
wasteType_sum_sort = wasteType_sum.sort_values(by='weight', ascending=False)
wasteType_sum = wasteType_sum_sort.sort_values(by='weight', ascending=False).head(5)
fig_wasteType = px.bar(wasteType_sum, x='weight', y='wasteType', orientation='h', title='Type of Waste')


""" 
    4 Newest Date
    Line Chart
"""
df['date'] = pd.to_datetime(df['date'], format='%d-%m-%Y')
waste_trend = df.groupby('date')['weight'].count().reset_index()
newest_waste_trend = waste_trend.sort_values(by='date', ascending=False)
newest_waste_trend = newest_waste_trend.sort_values(by='date', ascending=False)
fig_waste_trend = px.line(newest_waste_trend, x='date', y='weight', orientation='h', title='Waste Trend')


""" 
    Most Consistent Customers
    Heat Map
"""
consistent_customers = df['name'].value_counts().reset_index()
fig_consistent_customers = px.treemap(consistent_customers, path=[consistent_customers.name], values='count', title='Most Consistent Customers')


""" 
    Target Customer
    Gauge Chart
"""
target_customer_count = df['name'].nunique()
max_target_customer = 50  # Set the maximum target customer count here
fig_target_customer = go.Figure(go.Indicator(
    mode="gauge+number",
    value=target_customer_count,
    domain={'x': [0, 1], 'y': [0, 1]},
    title={'text': "Target Customer"},
    gauge={'axis': {'range': [None, max_target_customer]},
           'bar': {'color': "darkblue"},
           'steps': [
               {'range': [0, max_target_customer / 2], 'color': "lightgray"},
               {'range': [max_target_customer / 2, max_target_customer], 'color': "gray"}],
           'threshold': {'line': {'color': "red", 'width': 4}, 'thickness': 0.75, 'value': target_customer_count}}))
fig_target_customer.update_layout()


""" 
    Customer Development
    Vertical Bar Chart
"""
customer_development = df.groupby('date')['name'].nunique().reset_index()
customer_development_trend = customer_development.sort_values(by='date', ascending=False).head(4)
customer_development_trend = customer_development_trend.sort_values(by='date', ascending=False)
fig_customer_development = px.bar(customer_development_trend, x='date', y='name', title='Customer Development')


# Create the Dash app layout
app = Dash(__name__, external_stylesheets=['https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/css/bootstrap.min.css'])
app.layout = html.Div([
    html.Div([
        html.H1('Waste Bank Dashboard', className='text-center'),
        html.Div([
            html.Div([
                html.Div([
                    html.P('Total Revenue', className='h6'),
                    html.P(f'Rp {total_revenue}', className='h5'),
                ]),
                html.Div([
                    html.P('Total Waste', className='h6'),
                    html.P(f'{total_waste} kg', className='h5'),
                ]),
            ], className='col-lg-4 card'),
            html.Div([
                dcc.Graph(figure=fig_wasteType),
            ], className='col-lg-4 card'),
            html.Div([
                dcc.Graph(figure=fig_waste_trend),
            ], className='col-lg-4 card'),
        ], className='row align-items-center'),
        html.Div([
            html.Div([
                dcc.Graph(figure=fig_consistent_customers),
            ], className='col-lg-4 card'),
            html.Div([
                dcc.Graph(figure=fig_target_customer),
            ], className='col-lg-4 card'),
            html.Div([
                dcc.Graph(figure=fig_customer_development),
            ], className='col-lg-4 card'),
        ], className='row align-items-center'),
    ])
])

# Run the Dash app
if __name__ == '__main__':
    app.run_server(debug=True)
