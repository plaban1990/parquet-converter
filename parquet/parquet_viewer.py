import os
import pandas as pd
from dash import Dash, dcc, html, dash_table, callback, Output, Input

# Target folder containing the Parquet files
target_folder = './target/'

# Function to list all Parquet files in the target folder
def list_parquet_files():
    return [f for f in os.listdir(target_folder) if f.endswith('.parquet')]

# Function to read a Parquet file and return a DataFrame
def read_parquet_file(file_name):
    file_path = os.path.join(target_folder, file_name)
    return pd.read_parquet(file_path, engine='pyarrow')

# Initialize Dash app
app = Dash(__name__)

app.layout = html.Div([
    html.H1("Parquet File Viewer", style={'text-align': 'center'}),
    
    # Dropdown to select a Parquet file
    dcc.Dropdown(
        id='parquet-dropdown',
        options=[{'label': file, 'value': file} for file in list_parquet_files()],
        placeholder="Select a Parquet file"
    ),
    
    # Display the table
    html.Div(id='table-container')
])

# Callback to update the table when a file is selected
@callback(
    Output('table-container', 'children'),
    Input('parquet-dropdown', 'value')
)
def update_table(selected_file):
    if selected_file:
        df = read_parquet_file(selected_file)
        return dash_table.DataTable(
            data=df.to_dict('records'),
            columns=[{'name': col, 'id': col} for col in df.columns],
            page_size=10,  # Show 10 rows per page
            style_table={'overflowX': 'auto'},
            style_cell={
                'textAlign': 'left',
                'padding': '10px',
                'whiteSpace': 'normal',
                'height': 'auto',
            }
        )
    else:
        return html.Div("Select a Parquet file to view its content.")

if __name__ == '__main__':
    app.run_server(debug=True)
