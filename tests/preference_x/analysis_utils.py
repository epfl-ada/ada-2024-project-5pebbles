import pandas as pd
import numpy as np
from scipy import stats
from statsmodels.stats.multitest import multipletests

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
                
    genre_base_rates = {genre: count/total_movies 
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