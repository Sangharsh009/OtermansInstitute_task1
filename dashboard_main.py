# First, let's import the necessary libraries
from dash import Dash, html, dcc, Input, Output
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# Now, laoding the required datasets
purchase_details = pd.read_csv('user_purchase_details.csv')
user_information = pd.read_csv('user_information.csv')
user_time_spent_details = pd.read_csv('user_time_spent_details.csv')
session_details = pd.read_csv('overall_session_details.csv')


# To create the dash app by instantiating
app = Dash()

# Developing the layout for the app
app.layout = html.Div(children=[
    html.Div(children=[
        html.H1(children='Purchase Details for the Users', style={'background-color': '#2c3e50', 'textAlign': 'center', 'color': '#ffffff', 'fontFamily': 'Times New Roman, Georgia', 'fontSize': '32px', 'marginBottom': '20px'}),
        html.Div([
            html.Label('Select User:', style={'fontSize': 16, 'marginRight': '10px'}),
            dcc.Dropdown(
                id='user-dropdown',
                options=[{'label': user, 'value': user} for user in user_information['User_Name'].unique()],
                value=user_information['User_Name'].iloc[0], 
                multi=True 
            )
        ], style={'width': '20%', 'margin': '10px'}),
        
        html.Div([
            dcc.Graph(id='price-bar-chart'),
            dcc.Graph(id='item-pie-chart')
        ], style={'display': 'flex', 'flexDirection': 'row', 'justifyContent': 'center'}),
        
        html.Div(children=[
            html.H1(children='User Attributes Relationships', style={'background-color': '#2c3e50', 'textAlign': 'center', 'color': '#ffffff', 'fontFamily': 'Times New Roman, Georgia', 'fontSize': '32px', 'marginBottom': '20px'}),
            
            html.Div([
                html.H2(children='User Skill Level', style={'textAlign': 'center', 'marginBottom': '5px'}),
                dcc.Graph(id='user-skill-level-bar', style={'marginBottom': '20px'})
            ], style={'backgroundColor': 'rgba(255, 255, 255, 0.6)', 'padding': '10px', 'marginBottom': '10px'}),
            
            html.Div([
                html.H2(children='User Total Coins', style={'textAlign': 'center', 'marginBottom': '5px'}),
                dcc.Graph(id='user-total-coins-bar', style={'marginBottom': '20px'})
            ], style={'backgroundColor': 'rgba(255, 255, 255, 0.6)', 'padding': '10px', 'marginBottom': '10px'}),
            
            html.Div([
                html.H2(children='User Age', style={'textAlign': 'center', 'marginBottom': '5px'}),
                dcc.Graph(id='user-age-bar', style={'marginBottom': '20px'})
            ], style={'backgroundColor': 'rgba(255, 255, 255, 0.6)', 'padding': '10px', 'marginBottom': '10px'})
        ], style={'width': '100%', 'margin': 'auto'}),
        
        html.Div([
            html.H1("Time Spent Details of Users", style={'background-color': '#2c3e50', 'textAlign': 'center', 'color': '#ffffff', 'fontFamily': 'Times New Roman, Georgia', 'fontSize': '32px', 'marginBottom': '20px'}),
            dcc.Graph(id='time-spent-bar')
        ], style={'width': '100%', 'margin': 'auto'}),
    ]),
    html.Div([
        html.H1("User Performance Analysis (Session)", style={'background-color': '#2c3e50', 'textAlign': 'center', 'color': '#ffffff', 'fontFamily': 'Times New Roman, Georgia', 'fontSize': '32px', 'marginBottom': '20px'})
    ]),
    html.Div([
        dcc.Graph(id='performance-graph', config={'displayModeBar': False}),
        dcc.Graph(id='time-graph', config={'displayModeBar': False})
    ], style={'display': 'flex', 'flex-direction': 'row', 'justifyContent': 'center', 'margin-top': '20px'})
], style={'width': '90%', 'margin': 'auto'})


# Now, setting up the callback for all the plots to provide an interactive environment
@app.callback(
    Output(component_id='price-bar-chart', component_property='figure'),
    Output(component_id='item-pie-chart', component_property='figure'),
    Output(component_id='user-skill-level-bar', component_property='figure'),
    Output(component_id='user-total-coins-bar', component_property='figure'),
    Output(component_id='user-age-bar', component_property='figure'),
    Output(component_id='time-spent-bar', component_property='figure'),
    Output(component_id='performance-graph', component_property='figure'),
    Output(component_id='time-graph', component_property='figure'),
    Input(component_id='user-dropdown', component_property='value')
)
def update_plots(selected_users):
    if not selected_users:
         return {}, {}, {}, {}, {}, {}, {}, {}  # Default values when no user is selected
    
    if isinstance(selected_users, str):
        selected_users = [selected_users]  
    
    # Filter and transforming data based on the selected users and as required for the graphs
    filtered_user_purchase = purchase_details[purchase_details['User_Name'].isin(selected_users)]

    filtered_data = user_time_spent_details[user_time_spent_details['User_Name'].isin(selected_users)]
    time_spent = filtered_data.drop(columns=['User_Name', 'User_ID'])

    time_spent = time_spent.melt(var_name='Category', value_name='Time Spent')

    filtered_df_1 = session_details[session_details['User_Name'].isin(selected_users)]
    
    melted_df = pd.melt(filtered_df_1, id_vars=['User_Name'], value_vars=['Overall_Correct_Attempt', 'Overall_Error_Attempt', 'Overall_Question_Attempt'],
                        var_name='Metric', value_name='Value')
    

    sessions_fig_1 = px.bar(melted_df, x='Metric', y='Value', color='User_Name',
                labels={'Value': 'Value', 'Metric': 'Metric'},
                barmode='group')
    
    sessions_fig_1.update_layout(
        title={
            'text': 'Performance Analysis for Selected Users',
            'font': {
                'family': 'Times New Roman',
                'size': 24,
                'color': 'black',
            },
            'x': 0.5,  
            'y': 0.95   
        },
        font=dict(
            family="Times New Roman, Georgia",
            size=14,
            color="black"
        ),
        width=750,
        height=600
    )  
    

    usertime_fig = px.bar(time_spent, 
                 x='Category',  
                 y='Time Spent',  
                 color='Category',  
                 labels={'Category': 'Category', 'Time Spent': 'Time Spent (minutes)'},
                )
    usertime_fig.update_layout(
        title={
            'text': 'Time Spent by Category',
            'font': {
                'family': 'Times New Roman',
                'size': 24,
                'color': 'black',
            },
            'x': 0.5,  
            'y': 0.95   
        },
        font=dict(
            family="Times New Roman, Georgia",
            size=14,
            color="black"
        ),
        width=1200,
        height=600
    )

    filtered_df_2 = session_details[session_details['User_Name'].isin(selected_users)]
    
    time_df = filtered_df_2.groupby('User_Name')['Overall_Time_Taken'].sum().reset_index()
    sessions_fig_2 = px.bar(time_df, x='User_Name', y='Overall_Time_Taken', color='User_Name',
                 labels={'Overall_Time_Taken': 'Time Taken (seconds)', 'User_Name': 'User'})
    
    sessions_fig_2.update_layout(
        title={
            'text': 'Overall Time Taken by Selected Users',
            'font': {
                'family': 'Times New Roman',
                'size': 24,
                'color': 'black',
            },
            'x': 0.5,  
            'y': 0.95   
        },
        font=dict(
            family="Times New Roman, Georgia",
            size=14,
            color="black"
        ),
        width=750,
        height=600
    )  
   
    bar_fig = px.bar(filtered_user_purchase,
                     x='ItemName', y='ItemCost',
                     color='User_Name',  
                     )  
    bar_fig.update_layout(
        title={
            'text': 'Purchasing Info of Selected Users',
            'font': {
                'family': 'Times New Roman',
                'size': 24,
                'color': 'black',
            },
            'x': 0.5,  
            'y': 0.95  
        },
        font=dict(
            family="Times New Roman, Georgia",
            size=14,
            color="black"
        ),
        width=800,
        height=600
    )  
    
    
    total_values = purchase_details.groupby('ItemName')['ItemCost'].sum().reset_index()
    pie_fig = px.pie(total_values,
                     values='ItemCost',
                     names='ItemName',
                     title='Total Items Purchased Distribution')
    pie_fig.update_layout(
        title={
            'text': 'Total Items Purchased Distribution',
            'font': {
                'family': 'Times New Roman',
                'size': 24,
                'color': 'black',
            },
            'x': 0.5,  
            'y': 0.95   
        },
        font=dict(
            family="Times New Roman, Georgia",
            size=14,
            color="black",
        )
    )

    
    filtered_user_info = user_information[user_information['User_Name'].isin(selected_users)]
    
   
    skill_level_fig = go.Figure()
    for index, row in filtered_user_info.iterrows():
        skill_level_fig.add_trace(go.Bar(x=[row['User_Name']], y=[row['Skill_Level']], name=row['User_Name']))
    skill_level_fig.update_layout(xaxis_title='User', yaxis_title='Skill Level', font=dict(family="Times New Roman, Georgia", color="black", size=14), title_x=0.5, plot_bgcolor='rgba(255, 255, 255, 0.9)', xaxis=dict(showgrid=True, gridcolor='lightgray'), yaxis=dict(showgrid=True, gridcolor='lightgray'), showlegend=False)
    

    total_coins_fig = go.Figure()
    for index, row in filtered_user_info.iterrows():
        total_coins_fig.add_trace(go.Bar(x=[row['User_Name']], y=[row['Total_Coins']], name=row['User_Name']))
    total_coins_fig.update_layout(xaxis_title='User', yaxis_title='Total Coins', font=dict(family="Times New Roman, Georgia", color="black", size=14), title_x=0.5, plot_bgcolor='rgba(255, 255, 255, 0.9)', xaxis=dict(showgrid=True, gridcolor='lightgray'), yaxis=dict(showgrid=True, gridcolor='lightgray'), showlegend=False)
    
 
    user_age_fig = go.Figure()
    for index, row in filtered_user_info.iterrows():
        user_age_fig.add_trace(go.Bar(x=[row['User_Name']], y=[row['User_Age']], name=row['User_Name']))
    user_age_fig.update_layout(xaxis_title='User', yaxis_title='Age', font=dict(family="Times New Roman, Georgia", color="black", size=14), title_x=0.5, plot_bgcolor='rgba(255, 255, 255, 0.9)', xaxis=dict(showgrid=True, gridcolor='lightgray'), yaxis=dict(showgrid=True, gridcolor='lightgray'), showlegend=False)
    
    return bar_fig, pie_fig, skill_level_fig, total_coins_fig, user_age_fig, usertime_fig, sessions_fig_1, sessions_fig_2


# Runing in the local server(http://127.0.0.1:8050/)
if __name__ == '__main__':
    app.run_server(debug=True)