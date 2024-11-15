import ephem
import pandas as pd
from datetime import datetime

def get_zodiac_sign_accurate(date_str):
    """Calculate zodiac sign accurately based on date"""
    if pd.isna(date_str):
        return None
    
    try:
        if '-' in str(date_str):
            date = pd.to_datetime(date_str)
        else:
            return None
            
        # Creating an ephemeral Date object
        ephem_date = ephem.Date(date)
        
        # 获取太阳在黄道带上的位置
        sun = ephem.Sun()
        sun.compute(ephem_date)
        
        # 将角度转换为度数
        deg = float(sun.ra) * 180 / ephem.pi
        
        # 根据度数判断星座
        zodiac_ranges = [
            (0, 30, 'Aries'),
            (30, 60, 'Taurus'),
            (60, 90, 'Gemini'),
            (90, 120, 'Cancer'),
            (120, 150, 'Leo'),
            (150, 180, 'Virgo'),
            (180, 210, 'Libra'),
            (210, 240, 'Scorpio'),
            (240, 270, 'Sagittarius'),
            (270, 300, 'Capricorn'),
            (300, 330, 'Aquarius'),
            (330, 360, 'Pisces')
        ]
        
        for start, end, sign in zodiac_ranges:
            if start <= deg < end:
                return sign
        return 'Pisces'  # 处理360度的情况
        
    except:
        return None

def calculate_zodiac_signs(character_meta):
    """Calculate zodiac signs for all actors"""
    character_meta['calculated_zodiac'] = character_meta['Actor date of birth'].apply(get_zodiac_sign_accurate)
    return character_meta

def get_zodiac_actor_stats(character_meta):
    """Get actor statistics for each zodiac sign"""
    actor_counts = character_meta.groupby(['calculated_zodiac', 'Actor name'])['Wikipedia movie ID'].count()
    
    # Find the most prolific actor for each zodiac sign
    top_actors = actor_counts.reset_index().groupby('calculated_zodiac').apply(
        lambda x: x.nlargest(3, 'Wikipedia movie ID')
    ).reset_index(drop=True)
    
    # Rename columns and sort
    top_actors.columns = ['Zodiac Sign', 'Actor Name', 'Movie Count']
    top_actors = top_actors.sort_values('Movie Count', ascending=False)
    
    return top_actors

def analyze_specific_zodiac_actor(character_meta, movie_meta, zodiac_sign, genre_mapping, reverse_mapping):
    """Analyze movie genre distribution for specific zodiac sign actor"""
    top_actors = get_zodiac_actor_stats(character_meta)
    
    if zodiac_sign in top_actors['Zodiac Sign'].values:
        top_actor = top_actors[top_actors['Zodiac Sign'] == zodiac_sign].iloc[0]['Actor Name']
        
        # Get all the movies of this actor
        actor_movies = character_meta[character_meta['Actor name'] == top_actor]['Wikipedia movie ID']
        
        # 获取这些电影的类型
        actor_genres = movie_meta[movie_meta['Wikipedia movie ID'].isin(actor_movies)]['Movie genres']
        
        # Statistical type distribution
        genre_counts = {}
        for genres_str in actor_genres:
            if pd.notna(genres_str):
                genres_dict = eval(genres_str)
                for genre in genres_dict.values():
                    if genre in reverse_mapping:
                        main_genre = reverse_mapping[genre]
                        genre_counts[main_genre] = genre_counts.get(main_genre, 0) + 1
        
        return genre_counts
    return None

def get_zodiac_genre_matrix(character_meta, movie_meta, genre_mapping, reverse_mapping):
    """Create zodiac-genre matrix"""
    zodiac_genre_matrix = {}
    zodiac_counts = {}
    
    for _, char_row in character_meta.iterrows():
        zodiac = char_row['calculated_zodiac']
        movie_id = char_row['Wikipedia movie ID']
        
        if pd.isna(zodiac):
            continue
            
        movie_row = movie_meta[movie_meta['Wikipedia movie ID'] == movie_id]
        if len(movie_row) == 0:
            continue
            
        genres_str = movie_row.iloc[0]['Movie genres']
        if pd.isna(genres_str):
            continue
            
        if zodiac not in zodiac_genre_matrix:
            zodiac_genre_matrix[zodiac] = {}
            zodiac_counts[zodiac] = 0
            
        zodiac_counts[zodiac] += 1
        
        genres_dict = eval(genres_str)
        for genre in genres_dict.values():
            if genre in reverse_mapping:
                main_genre = reverse_mapping[genre]
                zodiac_genre_matrix[zodiac][main_genre] = zodiac_genre_matrix[zodiac].get(main_genre, 0) + 1
                
    return zodiac_genre_matrix, zodiac_counts