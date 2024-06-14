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

# Generate figures
total_revenue = df['price'].sum()
total_waste = df['weight'].sum()

# print(df)

wasteType = df.groupby('wasteType')['weight'].sum().reset_index()
fig_wasteType = px.bar(wasteType, x='weight', y='wasteType', orientation='h', title='Type of Waste')

waste_trend = df.groupby('date')['weight'].sum().reset_index()
fig_waste_trend = px.line(waste_trend, x='date', y='weight', title='Waste Trend')

consistent_customers = df['name'].value_counts().reset_index()
fig_consistent_customers = px.treemap(consistent_customers, path=[consistent_customers.name], values='count', title='Most Consistent Customers')


target_customer_count = df['name'].nunique()

customer_development = df.groupby('date')['name'].nunique().reset_index()
fig_customer_development = px.bar(customer_development, x='date', y='name', title='Customer Development')


# Layout
app.layout = html.Div([
    html.Div([
        html.H1('Waste Bank Dashboard'),
        html.Div([
            html.Div([
                html.H2('Total Revenue'),
                html.P(f'{total_revenue}'),
            ], className='card'),
            html.Div([
                html.H2('Total Waste'),
                html.P(f'{total_waste}'),
            ], className='card'),
        ], className='row'),
        html.Div([
            html.Div([
                dcc.Graph(figure=fig_wasteType),
            ], className='six columns'),
            html.Div([
                dcc.Graph(figure=fig_waste_trend),
            ], className='six columns'),
        ], className='row'),
        html.Div([
            html.Div([
                dcc.Graph(figure=fig_consistent_customers),
            ], className='six columns'),
            html.Div([
                html.Div([
                    html.H2('Target Customer'),
                    html.P(f'Customers: {target_customer_count}'),
                ], className='card'),
            ], className='six columns'),
        ], className='row'),
        html.Div([
            html.Div([
                dcc.Graph(figure=fig_customer_development),
            ], className='six columns'),
        ], className='row'),
    ])
])

if __name__ == '__main__':
    app.run_server(debug=True)
