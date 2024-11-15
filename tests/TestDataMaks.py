#1 Preparing the Datasets
#1.1 Loading the datasets
import pandas as pd
import matplotlib.pyplot as plt
import re
import TestFunction
from datetime import datetime

CharacterMeta = TestFunction.getCharacterMeta(r'C:\Users\makss\ada-2024-project-5pebbles\data\RawDatasets\MovieSummaries\character.metadata.tsv')
MovieMeta = TestFunction.getMovieMeta(r'C:\Users\makss\ada-2024-project-5pebbles\data\RawDatasets\MovieSummaries\movie.metadata.tsv')
CharacterMetaCleaned = TestFunction.getCharacterMetaCleaned(r'C:\Users\makss\ada-2024-project-5pebbles\data\ProcessedDatasets\cleaned.character.metadata.tsv')

#1.2 Cleaning the datasets and looking at some informations
MovieMeta = TestFunction.plot_movies_by_year(MovieMeta)

# Initialize a set to store all unique genres
all_genres = set()

# Create a dictionary to store the count of each genre
genre_counts = {}

# Iterate through each row in the 'Movie genres' column
for genres_dict_str in MovieMeta['Movie genres'].dropna():
    # Use eval to convert the string to a dictionary (assuming correct format)
    genres_dict = eval(genres_dict_str)
        
    # Extract only the genre names (values of the dictionary)
    genres = genres_dict.values()
        
    # Update the set of all unique genres
    all_genres.update(genres)
        
    # Count each genre's occurrences
    for genre in genres:
        genre_counts[genre] = genre_counts.get(genre, 0) + 1


MovieMeta, sorted_genres, genre_counts_by_decade, top_genres_by_decade = TestFunction.plot_top_genres_by_decade(genre_counts, MovieMeta)

#2 Analysis
#2.1 Distribution of Actors Based on Zodiac Sign
CharacterMeta, CharacterMetaCleaned, zodiac_counts = TestFunction.plot_zodiac_distribution(CharacterMeta, CharacterMetaCleaned, TestFunction.get_zodiac_sign)
#2.2 Actors Zodiac Sign in Film Genres
merged_data = TestFunction.plot_zodiac_contribution_to_genres(CharacterMetaCleaned, MovieMeta, genre_counts)
#2.3 Normalization and Weighted Average
TestFunction.plot_zodiac_weighted_contribution_to_genres(genre_counts_by_zodiac, zodiac_counts)