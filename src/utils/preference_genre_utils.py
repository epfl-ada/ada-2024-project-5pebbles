import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from scipy import stats
from statsmodels.stats.multitest import multipletests
import ephem
from datetime import datetime


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


def calculate_preference_matrix(zodiac_genre_matrix, zodiac_counts, genres):
    """Calculate preference matrix"""
    preference_matrix = {}
    for zodiac in zodiac_genre_matrix.keys():
        preference_matrix[zodiac] = {}
        total_movies = zodiac_counts[zodiac]
        for genre in genres:
            if total_movies > 0:
                preference = zodiac_genre_matrix[zodiac].get(genre, 0) / total_movies
            else:
                preference = 0
            preference_matrix[zodiac][genre] = preference
    return preference_matrix


def calculate_base_rates(movie_meta, reverse_mapping):
    """Calculate base rates"""
    all_genre_counts = {}
    total_movies = 0

    for _, row in movie_meta.iterrows():
        if pd.isna(row['Movie genres']):
            continue

        genres_dict = eval(row['Movie genres'])
        total_movies += 1

        for genre in genres_dict.values():
            if genre in reverse_mapping:
                main_genre = reverse_mapping[genre]
                all_genre_counts[main_genre] = all_genre_counts.get(main_genre, 0) + 1

    genre_base_rates = {genre: count / total_movies
                        for genre, count in all_genre_counts.items()}
    return genre_base_rates


def perform_statistical_tests(preference_data, genres, zodiac_signs):
    """Perform statistical tests"""
    # 1. Normality test
    normality_results = {}
    for genre_idx, genre in enumerate(genres):
        genre_data = [row[genre_idx] for row in preference_data]
        # Shapiro-Wilk检验
        stat, p_value = stats.shapiro(genre_data)
        # D'Agostino's K^2检验
        k2_stat, k2_p = stats.normaltest(genre_data)
        normality_results[genre] = {
            'Shapiro_stat': stat,
            'Shapiro_p': p_value,
            'K2_stat': k2_stat,
            'K2_p': k2_p
        }

    # 2. Preparing ANOVA data
    genre_preferences = {genre: [] for genre in genres}
    for zodiac_idx, zodiac in enumerate(zodiac_signs):
        for genre_idx, genre in enumerate(genres):
            genre_preferences[genre].append(preference_data[zodiac_idx][genre_idx])

    # 3. Run ANOVA
    f_stat, anova_p = stats.f_oneway(*[genre_preferences[genre] for genre in genres])

    # 4. Kruskal-Wallis H-test
    h_stat, kw_p = stats.kruskal(*[genre_preferences[genre] for genre in genres])

    # 5. Correction for multiple comparisons
    all_p_values = []
    p_value_sources = []

    # Collect p-values for normality tests
    for genre, results in normality_results.items():
        all_p_values.extend([results['Shapiro_p'], results['K2_p']])
        p_value_sources.extend([f"{genre}_shapiro", f"{genre}_k2"])

    # Adding p-values for ANOVA
    all_p_values.append(anova_p)
    p_value_sources.append("ANOVA")

    # Correction for multiple comparisons
    reject, corrected_p_values, _, _ = multipletests(all_p_values, method='bonferroni')

    return {
        'normality': normality_results,
        'anova': (f_stat, anova_p),
        'kruskal': (h_stat, kw_p),
        'multiple_comparison': list(zip(p_value_sources, all_p_values,
                                        corrected_p_values, reject))
    }


def calculate_specificity_scores(pref_df, base_rates):
    """Calculate specificity scores"""
    specificity_scores = pd.DataFrame(index=pref_df.index, columns=pref_df.columns)

    # 首先根据基准比率标准化偏好
    normalized_prefs = pd.DataFrame(index=pref_df.index, columns=pref_df.columns)
    for genre in pref_df.columns:
        if base_rates[genre] > 0:
            normalized_prefs[genre] = (pref_df[genre] - base_rates[genre]) / base_rates[genre]
        else:
            normalized_prefs[genre] = 0

    # 然后计算相对于其他星座的特异性
    for genre in normalized_prefs.columns:
        for zodiac in normalized_prefs.index:
            others_mean = normalized_prefs[genre][normalized_prefs.index != zodiac].mean()
            if others_mean != 0:
                specificity_scores.loc[zodiac, genre] = (
                        normalized_prefs.loc[zodiac, genre] - others_mean
                )
            else:
                specificity_scores.loc[zodiac, genre] = normalized_prefs.loc[zodiac, genre]

    return specificity_scores


def find_significant_preferences(z_scores, specificity_scores, zodiac_signs, genres,
                                 z_threshold=1.96):
    """Find significant preferences"""
    significant_preferences = []
    for zodiac in zodiac_signs:
        for genre in genres:
            z_score = z_scores.loc[zodiac, genre]
            specificity = specificity_scores.loc[zodiac, genre]
            if abs(z_score) > z_threshold:
                significant_preferences.append({
                    'Zodiac': zodiac,
                    'Genre': genre,
                    'Z-score': float(f'{z_score:.3f}'),
                    'Specificity': float(f'{specificity:.3f}')
                })
    return pd.DataFrame(significant_preferences)


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
        textfont={"size": 10},
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
        textfont={"size": 10},
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
        textfont={"size": 10},
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