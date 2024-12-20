# diversity_visualization.py

import plotly.express as px
import plotly.graph_objects as go
import numpy as np

def create_gdi_boxplot(actor_gdi_df):
    """Create GDI boxplot"""
    fig = px.box(actor_gdi_df, x='Zodiac', y='GDI',
                 title='Genre Diversity Index Distribution by Zodiac Sign')
    
    fig.update_layout(
        xaxis_title='Zodiac Sign',
        yaxis_title='Genre Diversity Index',
        showlegend=False
    )
    return fig

def create_gdi_violin_plot(actor_gdi_df):
    """Create GDI violin plot"""
    fig = px.violin(actor_gdi_df, x='Zodiac', y='GDI',
                    title='Genre Diversity Index Distribution by Zodiac Sign (Violin Plot)')
    
    fig.update_layout(
        xaxis_title='Zodiac Sign',
        yaxis_title='Genre Diversity Index',
        showlegend=False
    )
    return fig

def create_mean_gdi_bar(zodiac_stats):
    """Create mean GDI bar chart"""
    fig = px.bar(zodiac_stats, x='Zodiac', y='Mean_GDI',
                 error_y='Std_GDI',
                 title='Mean Genre Diversity Index by Zodiac Sign')
    
    fig.update_layout(
        xaxis_title='Zodiac Sign',
        yaxis_title='Mean Genre Diversity Index',
        showlegend=False
    )
    return fig