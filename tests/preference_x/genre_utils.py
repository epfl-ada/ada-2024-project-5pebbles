def create_genre_mapping():
    """Create movie genre mapping"""
    genre_mapping = {
        'Comedy': ['Comedy', 'Comedy film'],
        'Romance Film': ['Romance Film', 'Romantic drama'],
        'Action/Adventure': ['Action', 'Action/Adventure', 'Adventure'],
        'Drama': ['Drama'],
        'Thriller': ['Thriller'],
        'Horror': ['Horror'],
        'Documentary': ['Documentary'],
        'Animation': ['Animation'],
        'Crime Fiction': ['Crime Fiction'],
        'Musical': ['Musical'],
        'Family Film': ['Family Film']
    }
    
    # 创建反向映射
    reverse_mapping = {}
    for main_genre, aliases in genre_mapping.items():
        for alias in aliases:
            reverse_mapping[alias] = main_genre
            
    return genre_mapping, reverse_mapping

def get_unique_genres(movie_meta):
    """Extract all unique movie genres"""
    all_genres = set()
    for genres_dict_str in movie_meta['Movie genres'].dropna():
        genres_dict = eval(genres_dict_str)
        genres = genres_dict.values()
        all_genres.update(genres)
    return all_genres

def analyze_genre_distribution(movie_meta, reverse_mapping):
    """Analyze movie genre distribution"""
    genre_counts = {}
    for genres_dict_str in movie_meta['Movie genres'].dropna():
        genres_dict = eval(genres_dict_str)
        for genre in genres_dict.values():
            if genre in reverse_mapping:
                main_genre = reverse_mapping[genre]
                genre_counts[main_genre] = genre_counts.get(main_genre, 0) + 1
    return genre_counts