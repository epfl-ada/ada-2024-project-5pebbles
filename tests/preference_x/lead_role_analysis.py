# lead_role_analysis.py

import pandas as pd
import numpy as np
from scipy import stats
import statsmodels.api as sm
from statsmodels.formula.api import ols

def integrate_role_data(character_meta, role_data):
    """Integrate character data
    
    Args:
        character_meta: Original character metadata
        role_data: New data containing lead role information
    Returns:
        Integrated DataFrame
    """
    # Merge datasets
    merged_data = pd.merge(
        character_meta,
        role_data[['Wikipedia movie ID', 'Actor name', 'is_main_character']],
        on=['Wikipedia movie ID', 'Actor name'],
        how='left'
    )
    return merged_data

def calculate_lead_role_metrics(merged_data):
    """Calculate lead role related metrics
    
    Args:
        merged_data: Integrated data
    Returns:
        DataFrame containing various metrics
    """
    # Calculate overall lead ratio as baseline
    overall_lead_ratio = merged_data['is_main_character'].mean()
    
    # Group by zodiac sign and actor to calculate metrics
    metrics = []
    for zodiac in merged_data['calculated_zodiac'].unique():
        zodiac_data = merged_data[merged_data['calculated_zodiac'] == zodiac]
        
        # Calculate lead ratio for this zodiac
        zodiac_lead_ratio = zodiac_data['is_main_character'].mean()
        
        # Calculate adjusted lead ratio
        adjusted_ratio = zodiac_lead_ratio / overall_lead_ratio if overall_lead_ratio > 0 else 0
        
        # Count statistics
        total_roles = len(zodiac_data)
        lead_roles = zodiac_data['is_main_character'].sum()
        
        metrics.append({
            'Zodiac': zodiac,
            'Lead_Ratio': zodiac_lead_ratio,
            'Adjusted_Ratio': adjusted_ratio,
            'Total_Roles': total_roles,
            'Lead_Roles': lead_roles
        })
    
    return pd.DataFrame(metrics)

def analyze_genre_lead_roles(merged_data, movie_meta, reverse_mapping):
    """Analyze lead role ratios in different movie genres
    
    Args:
        merged_data: Integrated data
        movie_meta: Movie metadata
        reverse_mapping: Genre mapping dictionary
    Returns:
        DataFrame containing genre analysis
    """
    genre_metrics = []
    
    for zodiac in merged_data['calculated_zodiac'].unique():
        zodiac_data = merged_data[merged_data['calculated_zodiac'] == zodiac]
        
        for movie_id in zodiac_data['Wikipedia movie ID'].unique():
            movie_genres = movie_meta[movie_meta['Wikipedia movie ID'] == movie_id]['Movie genres']
            if len(movie_genres) > 0:
                genres_dict = eval(movie_genres.iloc[0])
                for genre in genres_dict.values():
                    if genre in reverse_mapping:
                        main_genre = reverse_mapping[genre]
                        is_lead = zodiac_data[zodiac_data['Wikipedia movie ID'] == movie_id]['is_main_character'].iloc[0]
                        
                        genre_metrics.append({
                            'Zodiac': zodiac,
                            'Genre': main_genre,
                            'is_lead': is_lead
                        })
    
    return pd.DataFrame(genre_metrics)

def perform_statistical_tests(merged_data):
    """Perform statistical tests"""
    # Prepare data
    valid_data = merged_data.dropna(subset=['is_main_character', 'calculated_zodiac'])
    
    # Chi-square test
    observed = pd.crosstab(valid_data['calculated_zodiac'], 
                          valid_data['is_main_character'])
    chi2, chi2_p = stats.chi2_contingency(observed)[:2]
    
    # Kruskal-Wallis H-test
    try:
        zodiac_groups = [group['is_main_character'].values 
                        for _, group in valid_data.groupby('calculated_zodiac')]
        h_stat, kw_p = stats.kruskal(*zodiac_groups)
    except:
        h_stat, kw_p = np.nan, np.nan
    
    # Effect size (Cramer's V)
    n = len(valid_data)
    min_dim = min(observed.shape) - 1
    cramer_v = np.sqrt(chi2 / (n * min_dim)) if n * min_dim > 0 else 0
    
    return {
        'chi2_stat': chi2,
        'chi2_p': chi2_p,
        'kruskal_h': h_stat,
        'kruskal_p': kw_p,
        'cramer_v': cramer_v
    }


def perform_anova_analysis(merged_data, movie_meta, reverse_mapping):
    """
    Perform one-way and two-way ANOVA analysis for zodiac signs and movie genres
    
    Args:
        merged_data: DataFrame containing movie and role information
        movie_meta: DataFrame containing movie metadata
        reverse_mapping: Dictionary for mapping genre categories
    
    Returns:
        dict: Dictionary containing ANOVA results
    """
    # Get genre metrics first
    genre_metrics = analyze_genre_lead_roles(merged_data, movie_meta, reverse_mapping)
    
    # Prepare data for one-way ANOVA
    valid_data = merged_data.copy()
    
    # Handle NaN values before converting to int
    # Fill NaN with 0 (assuming NaN means not a main character)
    valid_data['is_main_character'] = valid_data['is_main_character'].fillna(0)
    valid_data.loc[:, 'is_main_character'] = valid_data['is_main_character'].astype(int)
    
    # Remove any remaining rows with NaN values in relevant columns
    valid_data = valid_data.dropna(subset=['calculated_zodiac'])
    
    # One-way ANOVA for zodiac signs
    zodiac_groups = [group['is_main_character'].values 
                    for name, group in valid_data.groupby('calculated_zodiac')]
    
    # Check if we have enough groups for ANOVA
    if len(zodiac_groups) < 2:
        print("Warning: Not enough groups for ANOVA analysis")
        return {
            'one_way': {
                'f_statistic': float('nan'),
                'p_value': float('nan')
            },
            'two_way': pd.DataFrame(),
            'effect_sizes': {'zodiac': 0.0, 'genre': 0.0, 'interaction': 0.0}
        }
    
    f_stat_zodiac, p_value_zodiac = stats.f_oneway(*zodiac_groups)
    
    # Prepare data for two-way ANOVA
    # Ensure is_lead is numeric in genre_metrics
    genre_metrics['is_lead'] = genre_metrics['is_lead'].fillna(0).astype(float)
    
    try:
        # Create model for two-way ANOVA with simplified formula
        model = ols('is_lead ~ C(Zodiac) + C(Genre)', data=genre_metrics).fit()
        anova_table = sm.stats.anova_lm(model, typ=2)
        
        # Calculate effect sizes (Eta-squared)
        ss_total = anova_table['sum_sq'].sum()
        eta_squared = {
            'zodiac': anova_table['sum_sq'][0] / ss_total,
            'genre': anova_table['sum_sq'][1] / ss_total,
            'interaction': 0.0  # No interaction term in simplified model
        }
    except Exception as e:
        print(f"Warning: Two-way ANOVA failed with error: {str(e)}")
        # Return dummy values if ANOVA fails
        anova_table = pd.DataFrame()
        eta_squared = {'zodiac': 0.0, 'genre': 0.0, 'interaction': 0.0}
    
    return {
        'one_way': {
            'f_statistic': f_stat_zodiac,
            'p_value': p_value_zodiac
        },
        'two_way': anova_table,
        'effect_sizes': eta_squared
    }

def analyze_genre_interactions(genre_metrics):
    """Analyze interactions between zodiac signs and genres
    
    Args:
        genre_metrics: Genre analysis data 
    Returns:
        Interaction analysis results
    """
    # Calculate lead ratio for each zodiac-genre combination 
    interaction_data = (genre_metrics.groupby(['Zodiac', 'Genre'])
                       .agg({'is_lead': ['mean', 'count', 'sum']})
                       .reset_index())
    
    # Rename columns
    interaction_data.columns = ['Zodiac', 'Genre', 'mean', 'count', 'sum']
    
    # Calculate overall baseline ratio
    overall_lead_ratio = genre_metrics['is_lead'].mean()
    
    # Calculate relative effects
    if overall_lead_ratio > 0:
        interaction_data['relative_effect'] = (
            interaction_data['mean'] - overall_lead_ratio) / overall_lead_ratio
    else:
        interaction_data['relative_effect'] = 0
    
    return interaction_data