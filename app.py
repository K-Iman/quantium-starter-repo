from dash import Dash, html, dcc
import plotly.express as px
import pandas as pd

# 1. Load the data
df = pd.read_csv('formatted_morsel_data.csv')

# 2. Convert 'date' to datetime objects and sort chronologically
df['date'] = pd.to_datetime(df['date'])
df = df.sort_values(by='date')

# 3. Initialize the Dash app
app = Dash(__name__)

# 4. Create the line chart using Plotly Express
fig = px.line(
    df, 
    x='date', 
    y='sales-$', 
    title='Pink Morsel Sales Trend (2018 - 2022)'
)

# Add appropriate axis labels
fig.update_layout(
    xaxis_title='Date', 
    yaxis_title='Total Sales ($)'
)

# Add a vertical line to pinpoint the price increase
fig.add_vline(
    x=pd.Timestamp('2021-01-15').timestamp() * 1000,  # ✅ Fixed: numeric timestamp in ms
    line_dash="dash", 
    line_color="red", 
    annotation_text="Price Increase on Jan 15, 2021"
)

# 5. Define the layout of the app (Header + Chart)
app.layout = html.Div(children=[
    html.H1(
        children='Soul Foods: Pink Morsel Sales Visualizer', 
        style={'textAlign': 'center', 'fontFamily': 'Arial, sans-serif'}
    ),
    dcc.Graph(
        id='sales-line-chart',
        figure=fig
    )
])

# 6. Run the local development server
if __name__ == '__main__':
    app.run(debug=True)