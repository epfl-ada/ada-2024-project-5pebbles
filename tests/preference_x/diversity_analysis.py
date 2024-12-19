# diversity_analysis.py

import pandas as pd
import numpy as np
from scipy import stats
import math

def calculate_raw_diversity_score(actor_genres):
    """Calculate raw diversity score
    
    Args:
        actor_genres: List of all movie genres the actor has appeared in
    Returns:
        Raw diversity score (0-1)
    """
    unique_genres = len(set(actor_genres))
    return unique_genres / 11  # 11 is our defined total number of genres

def calculate_shannon_diversity(genre_counts):
    """Calculate Shannon diversity index
    
    Args:
        genre_counts: Dictionary with genres as keys and movie counts as values
    Returns:
        Shannon diversity index
    """
    total = sum(genre_counts.values())
    if total == 0:
        return 0
        
    shannon_index = 0
    for count in genre_counts.values():
        if count > 0:
            p_i = count / total
            shannon_index -= p_i * math.log(p_i)
    return shannon_index

def calculate_genre_balance_score(genre_counts):
    """Calculate genre balance score
    
    Args:
        genre_counts: Dictionary with genres as keys and movie counts as values
    Returns:
        Genre balance score (0-1)
    """
    if not genre_counts:
        return 0
        
    values = list(genre_counts.values())
    total = sum(values)
    if total == 0:
        return 0
        
    proportions = [v/total for v in values]
    return 1 - (max(proportions) - min(proportions))

def calculate_actor_gdi(movie_data, actor_data, actor_name, genres, 
                       weights=(0.3, 0.4, 0.3)):
    """Calculate actor's Genre Diversity Index (GDI)
    
    Args:
        movie_data: Movie data DataFrame 
        actor_data: Actor data DataFrame
        actor_name: Name of actor
        genres: List of all possible genres
        weights: (RDS weight, SDI weight, GBS weight)
    Returns:
        GDI score (0-1)
    """
    # Get all movies for actor
    actor_movies = actor_data[actor_data['Actor name'] == actor_name]['Wikipedia movie ID']
    if len(actor_movies) == 0:
        return 0
        
    # Count movies in each genre
    genre_counts = {genre: 0 for genre in genres}
    for movie_id in actor_movies:
        movie_genres = movie_data[movie_data['Wikipedia movie ID'] == movie_id]['Movie genres']
        if len(movie_genres) > 0:
            genres_dict = eval(movie_genres.iloc[0])
            for genre in genres_dict.values():
                if genre in genre_counts:
                    genre_counts[genre] += 1
    
    # Calculate three components
    rds = calculate_raw_diversity_score(list(genre_counts.keys()))
    sdi = calculate_shannon_diversity(genre_counts)
    gbs = calculate_genre_balance_score(genre_counts)
    
    # Normalize Shannon index (typically between 0-ln(n))
    max_shannon = math.log(len(genres))
    sdi_normalized = sdi / max_shannon if max_shannon > 0 else 0
    
    # Calculate weighted GDI
    gdi = weights[0] * rds + weights[1] * sdi_normalized + weights[2] * gbs
    
    return gdi

def analyze_zodiac_diversity(movie_meta, character_meta, genres, min_movies=5):
    """Analyze genre diversity for each zodiac sign
    
    Args:
        movie_meta: Movie metadata DataFrame
        character_meta: Character metadata DataFrame 
        genres: List of all possible genres
        min_movies: Minimum number of movies threshold
    Returns:
        DataFrame containing GDI statistics for each zodiac sign
    """
    # Calculate GDI for each actor
    actor_gdis = []
    for actor_name in character_meta['Actor name'].unique():
        # Check minimum movie count
        movie_count = len(character_meta[character_meta['Actor name'] == actor_name])
        if movie_count >= min_movies:
            # Get actor's zodiac sign
            zodiac = character_meta[character_meta['Actor name'] == actor_name]['calculated_zodiac'].iloc[0]
            if pd.notna(zodiac):
                gdi = calculate_actor_gdi(movie_meta, character_meta, actor_name, genres)
                actor_gdis.append({
                    'Actor': actor_name,
                    'Zodiac': zodiac,
                    'GDI': gdi,
                    'Movie_Count': movie_count
                })
    
    actor_gdi_df = pd.DataFrame(actor_gdis)
    
    # Calculate statistics for each zodiac sign
    zodiac_stats = []
    for zodiac in actor_gdi_df['Zodiac'].unique():
        zodiac_gdis = actor_gdi_df[actor_gdi_df['Zodiac'] == zodiac]['GDI']
        stats_dict = {
            'Zodiac': zodiac,
            'Mean_GDI': zodiac_gdis.mean(),
            'Median_GDI': zodiac_gdis.median(),
            'Std_GDI': zodiac_gdis.std(),
            'Actor_Count': len(zodiac_gdis),
            'Top_Actors': ', '.join(actor_gdi_df[
                (actor_gdi_df['Zodiac'] == zodiac) & 
                (actor_gdi_df['GDI'] >= np.percentile(zodiac_gdis, 90))
            ]['Actor'].head().tolist())
        }
        zodiac_stats.append(stats_dict)
    
    return pd.DataFrame(zodiac_stats), actor_gdi_df

def perform_diversity_statistical_tests(actor_gdi_df):
    """Perform statistical tests
    
    Args:
        actor_gdi_df: DataFrame containing actor GDI data
    Returns:
        Dictionary of statistical test results
    """
    # Prepare data
    zodiac_groups = [group['GDI'].values for name, group in actor_gdi_df.groupby('Zodiac')]
    
    # Perform Kruskal-Wallis H-test
    h_stat, kw_p = stats.kruskal(*zodiac_groups)
    
    # Calculate effect size (Eta-squared)
    n = len(actor_gdi_df)
    eta_squared = (h_stat - len(zodiac_groups) + 1) / (n - len(zodiac_groups))
    
    return {
        'kruskal_h': h_stat,
        'kruskal_p': kw_p,
        'effect_size': eta_squared
    }