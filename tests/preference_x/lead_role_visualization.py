# lead_role_visualization.py

import plotly.express as px
import plotly.graph_objects as go
import numpy as np
import pandas as pd

def create_lead_ratio_bar(metrics_df):
    """Create lead role ratio bar chart"""
    fig = px.bar(metrics_df, x='Zodiac', y='Lead_Ratio',
                 title='Lead Role Ratio by Zodiac Sign',
                 error_y=metrics_df['Lead_Ratio'] * 0.1)  # Assume 10% error range
    
    fig.update_layout(
        xaxis_title='Zodiac Sign',
        yaxis_title='Lead Role Ratio',
        showlegend=False
    )
    return fig

def create_genre_heatmap(interaction_data):
    """Create genre interaction heatmap"""
    # Create pivot table
    pivot_data = pd.pivot_table(
        interaction_data,
        values='relative_effect',
        index='Zodiac',
        columns='Genre',
        fill_value=0
    )
    
    # Ensure data is numeric type
    z_values = pivot_data.values.astype(float)
    
    fig = go.Figure(data=go.Heatmap(
        z=z_values,
        x=pivot_data.columns,
        y=pivot_data.index,
        colorscale='RdBu',
        zmid=0,
        text=np.array([[f'{val:.3f}' for val in row] for row in z_values]),
        texttemplate='%{text}',
        textfont={"size":10},
        colorbar=dict(title='Relative Effect')
    ))
    
    fig.update_layout(
        title='Zodiac-Genre Interaction Effect on Lead Roles',
        xaxis_title='Movie Genre',
        yaxis_title='Zodiac Sign',
        width=1000,
        height=600
    )
    return fig

def create_genre_lead_ratio_plot(genre_metrics):
    """Create genre lead role ratio plot"""
    summary = (genre_metrics.groupby(['Genre', 'Zodiac'])['is_lead']
              .mean().reset_index())
    
    fig = px.box(summary, x='Genre', y='is_lead', color='Zodiac',
                 title='Lead Role Distribution by Genre and Zodiac Sign')
    
    fig.update_layout(
        xaxis_title='Movie Genre',
        yaxis_title='Lead Role Ratio',
        showlegend=True
    )
    return fig