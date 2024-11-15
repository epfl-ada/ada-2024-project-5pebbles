import plotly.express as px
import plotly.graph_objects as go
import pandas as pd

def create_variability_plot(zodiac_cv, zodiac_signs):
    """Create coefficient of variation bar plot"""
    fig = px.bar(
        x=zodiac_signs,
        y=zodiac_cv,
        title='Variability in Genre Preferences by Zodiac Sign (Filtered)',
        labels={'x': 'Zodiac Sign', 'y': 'Coefficient of Variation'}
    )
    return fig

def create_specificity_heatmap(specificity_scores, genres, zodiac_signs):
    """Create specificity heatmap"""
    text_matrix = [[f'{val:.3f}' for val in row] for row in specificity_scores.values]
    
    fig = go.Figure(data=go.Heatmap(
        z=specificity_scores.values,
        x=genres,
        y=zodiac_signs,
        colorscale='RdBu',
        zmid=0,
        text=text_matrix,
        texttemplate='%{text}',
        textfont={"size":10},
        colorbar=dict(title='Specificity Index')
    ))
    
    fig.update_layout(
        title='Genre Preference Specificity by Zodiac Sign (Filtered)',
        xaxis_title='Movie Genres',
        yaxis_title='Zodiac Signs',
        width=1000,
        height=600
    )
    return fig

def create_preference_heatmap(preference_data, genres, zodiac_signs):
    """Create preference heatmap"""
    fig = go.Figure(data=go.Heatmap(
        z=preference_data,
        x=genres,
        y=zodiac_signs,
        colorscale='Viridis',
        text=[[f'{val:.1f}%' for val in row] for row in preference_data],
        texttemplate='%{text}',
        textfont={"size":10},
        colorbar=dict(title='Percentage')
    ))
    
    fig.update_layout(
        title='Movie Genre Preferences by Zodiac Sign',
        xaxis_title='Movie Genres',
        yaxis_title='Zodiac Signs',
        width=1000,
        height=600
    )
    return fig

def create_normalized_preference_heatmap(preference_data, base_rates, genres, zodiac_signs):
    """Create a heatmap showing normalized preferences corrected for baseline rates"""
    # Calculate normalized preferences
    normalized_data = []
    for zodiac_idx, zodiac in enumerate(zodiac_signs):
        row = []
        for genre_idx, genre in enumerate(genres):
            original_pref = preference_data[zodiac_idx][genre_idx]
            base_rate = base_rates[genre]
            # Calculate deviation from baseline
            if base_rate > 0:
                normalized_value = (original_pref - base_rate) / base_rate
            else:
                normalized_value = 0
            row.append(normalized_value)
        normalized_data.append(row)

    fig = go.Figure(data=go.Heatmap(
        z=normalized_data,
        x=genres,
        y=zodiac_signs,
        colorscale='RdBu',
        zmid=0,  # Set 0 as midpoint to clearly show preferences above/below baseline
        text=[[f'{val:.2f}' for val in row] for row in normalized_data],
        texttemplate='%{text}',
        textfont={"size":10},
        colorbar=dict(title='Relative Preference')
    ))

    fig.update_layout(
        title='Normalized Movie Genre Preferences by Zodiac Sign',
        xaxis_title='Movie Genres',
        yaxis_title='Zodiac Signs',
        width=1000,
        height=600
    )
    return fig