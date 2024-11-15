import pandas as pd
import numpy as np

def get_movie_meta(filepath):
    """Load movie metadata"""
    MovieMeta = pd.read_csv(filepath, sep='\t')
    
    MovieMeta.columns = [
        'Wikipedia movie ID',
        'Freebase movie ID',
        'Movie name',
        'Movie release date',
        'Movie box office revenue',
        'Movie runtime',
        'Movie languages',
        'Movie countries',
        'Movie genres'
    ]
    return MovieMeta

def get_character_meta(filepath):
    """Load character metadata"""
    CharacterMeta = pd.read_csv(filepath, sep='\t')
    
    CharacterMeta.columns = [
        'Wikipedia movie ID',
        'Freebase movie ID',
        'Movie release date',
        'Character name',
        'Actor date of birth',
        'Actor gender',
        'Actor height',
        'Actor ethnicity',
        'Actor name',
        'Actor age at movie release',
        'Freebase character/actor map ID',
        'Freebase character ID',
        'Freebase actor ID',
        'Zodiac Sign'
    ]
    return CharacterMeta

def print_basic_stats(movie_meta, character_meta):
    """Print basic statistical information"""
    print("=== Basic Statistics ===")
    print("Total number of movies:", len(movie_meta))
    print("Total number of characters/actors:", len(character_meta))
    print("Number of valid birth dates:", 
          character_meta['Actor date of birth'].notna().sum())

def filter_prolific_actors(character_meta, threshold=250):
    """Filter out actors with too many movie appearances"""
    actor_movie_counts = character_meta.groupby('Actor name')['Wikipedia movie ID'].count()
    excluded_actors = actor_movie_counts[actor_movie_counts > threshold].index
    return character_meta[~character_meta['Actor name'].isin(excluded_actors)]

def load_and_prepare_data(movie_filepath, character_filepath):
    """Main data loading function"""
    movie_meta = get_movie_meta(movie_filepath)
    character_meta = get_character_meta(character_filepath)
    print_basic_stats(movie_meta, character_meta)
    
    # 过滤多产演员
    filtered_character_meta = filter_prolific_actors(character_meta)
    
    return movie_meta, filtered_character_meta