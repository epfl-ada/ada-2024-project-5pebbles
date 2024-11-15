import pandas as pd
import re
import matplotlib.pyplot as plt
from datetime import datetime





def getMovieMeta(filepath):

    # Read the file
    MovieMeta = pd.read_csv(filepath, sep='\t')

    # Rename each column
    MovieMeta.columns=['Wikipedia movie ID',
                       'Freebase movie ID',
                       'Movie name',
                       'Movie release date',
                       'Movie box office revenue',
                       'Movie runtime',
                       'Movie languages',
                       'Movie countries',
                       'Movie genres']
    return MovieMeta

def getCharacterMeta(filepath):

    # Read the file
    CharacterMeta=pd.read_csv(filepath, sep='\t')

    # Rename each column
    CharacterMeta.columns=['Wikipedia movie ID',
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
                           'Freebase actor ID']
    return CharacterMeta

def getCharacterMetaCleaned(filepath):

    # Read the file
    CharacterMetaCleaned=pd.read_csv(filepath, sep='\t')

    # Rename each column
    CharacterMetaCleaned.columns=['Wikipedia movie ID',
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
                           'Freebase actor ID' ,
                           'Zodiac Sign']
    return CharacterMetaCleaned

def clean_genre(genre):
    # Replace non-breaking spaces with regular spaces
    genre = genre.replace('\xa0', ' ')  # Handles non-breaking spaces
    genre = re.sub(r'[{}/":]', '', genre)  # Remove characters like {, }, /, ", :
    genre = re.sub(r'\s+', ' ', genre)  # Replace multiple spaces with a single space
    genre = genre.strip()  # Strip any leading/trailing whitespace
    
    return genre

def get_zodiac_sign(birthdate):
    if pd.isnull(birthdate):
        return None  # Handle missing values
    # Ensure birthdate is in datetime format
    birthdate = pd.to_datetime(birthdate, errors='coerce')
    if birthdate is pd.NaT:
        return None

    month, day = birthdate.month, birthdate.day
    
    # Zodiac sign ranges
    zodiac_signs = {
        'Capricorn': [(12, 22), (1, 19)],
        'Aquarius': [(1, 20), (2, 18)],
        'Pisces': [(2, 19), (3, 20)],
        'Aries': [(3, 21), (4, 19)],
        'Taurus': [(4, 20), (5, 20)],
        'Gemini': [(5, 21), (6, 20)],
        'Cancer': [(6, 21), (7, 22)],
        'Leo': [(7, 23), (8, 22)],
        'Virgo': [(8, 23), (9, 22)],
        'Libra': [(9, 23), (10, 22)],
        'Scorpio': [(10, 23), (11, 21)],
        'Sagittarius': [(11, 22), (12, 21)],
    }

    for sign, ((start_month, start_day), (end_month, end_day)) in zodiac_signs.items():
        if (month == start_month and day >= start_day) or (month == end_month and day <= end_day):
            return sign
    return None  # Fallback in case of invalid date

def plot_movies_by_year(MovieMeta):
    """
    This function processes the 'MovieMeta' DataFrame to plot the number of movies released by year.

    Parameters:
    - MovieMeta (DataFrame): The DataFrame containing movie metadata, including the 'Movie release date'.
    
    Returns:
    - None: This function generates a plot.
    """
    # Convert 'Movie release date' to datetime and extract the year
    MovieMeta['Movie release date'] = pd.to_datetime(MovieMeta['Movie release date'], errors='coerce')
    MovieMeta['Release Year'] = MovieMeta['Movie release date'].dt.year

    # Count the number of movies released by year
    movie_count_by_year = MovieMeta['Release Year'].value_counts().sort_index()

    # Plot the data
    plt.figure(figsize=(10, 6))
    movie_count_by_year.plot(kind='bar', color='skyblue')
    plt.title('Number of Movies Released by Year')
    plt.xlabel('Release Year')
    plt.ylabel('Number of Movies')

    # Adjust x-ticks to show every 10th year
    years = movie_count_by_year.index
    plt.xticks(
        ticks=range(0, len(years), 10),  # Set ticks every 10 bars
        labels=years[::10],  # Use every 10th year as a label
        rotation=45
    )

    plt.tight_layout()
    # plt.show()
    return MovieMeta

def plot_top_genres_by_decade(genre_counts, MovieMeta):
    """
    This function processes the 'MovieMeta' DataFrame to clean the 'Movie genres', 
    calculate the top genres per decade, and plot the results.

    Parameters:
    - MovieMeta (DataFrame): The DataFrame containing movie metadata, including 'Movie genres' and 'Release Year'.
    
    Returns:
    - None: This function generates a plot.
    """
    
    

    # Print out the most common genres
    print("\n=== Most Common Movie Genres ===")
    sorted_genres = sorted(genre_counts.items(), key=lambda x: x[1], reverse=True)

    # Display the top 10 genres
    for genre, count in sorted_genres[:10]:
        print(f"{genre}: {count}")

    # Store the cleaned genre list into the 'Cleaned Movie genres' column
    MovieMeta['Cleaned Movie genres'] = MovieMeta['Movie genres'].apply(
        lambda genres_str: list(eval(genres_str).values()) if isinstance(genres_str, str) else []
    )

    MovieMeta['Release Decade'] = (MovieMeta['Release Year'] // 10) * 10

    # Explode the 'Cleaned Movie genres' to separate rows for each genre
    MovieMeta = MovieMeta.explode('Cleaned Movie genres')

    # Calculate genre counts by decade
    genre_counts_by_decade = MovieMeta.groupby(['Release Decade', 'Cleaned Movie genres']).size().reset_index(name='Count')

    # Get top 3-4 genres for each decade
    top_genres_by_decade = genre_counts_by_decade.groupby('Release Decade').apply(
        lambda x: x.nlargest(4, 'Count')
    ).reset_index(drop=True)

    # Plot the results
    plt.figure(figsize=(12, 8))
    for decade, group in top_genres_by_decade.groupby('Release Decade'):
        plt.bar(group['Cleaned Movie genres'] + f' ({decade}s)', group['Count'], label=f'{decade}s')

    plt.ylabel('Number of Movies')
    plt.xlabel('Genres by Decade')
    plt.title('Top 3-4 Movie Genres per Decade')
    plt.xticks(rotation=45, ha='right')  # Rotate x-axis labels for readability
    plt.legend(title='Decade', loc='upper right')
    plt.tight_layout()
    # plt.show()

    # Step 9: Print the top 4 most popular genres by decade
    print("Top 4 Most Popular Movie Genres by Decade:")
    for decade, group in top_genres_by_decade.groupby('Release Decade'):
        print(f"\n{decade}s:")
        for _, row in group.iterrows():
            print(f"  Genre: {row['Cleaned Movie genres']} - Count: {row['Count']}")
    return MovieMeta, sorted_genres, genre_counts_by_decade, top_genres_by_decade

def plot_zodiac_distribution(CharacterMeta, CharacterMetaCleaned, get_zodiac_sign_function):
    """
    This function processes the 'CharacterMeta' DataFrame to calculate the zodiac sign distribution 
    and plot the results.

    Parameters:
    - CharacterMeta (DataFrame): The DataFrame containing actor metadata, including 'Actor date of birth'.
    - CharacterMetaCleaned (DataFrame): A cleaned version of CharacterMeta, also with 'Zodiac Sign' column.
    - get_zodiac_sign_function (function): A function to calculate zodiac sign from date of birth.
    
    Returns:
    - None: This function generates a plot and prints the zodiac distribution.
    """

    # Step 1: Get the zodiac sign for each actor based on the 'Actor date of birth' column
    CharacterMeta['Zodiac Sign'] = CharacterMeta['Actor date of birth'].apply(get_zodiac_sign_function)

    # Step 2: Calculate the counts of each zodiac sign
    zodiac_counts = CharacterMeta['Zodiac Sign'].value_counts().sort_index()
    zodiac_counts_cleaned = CharacterMetaCleaned['Zodiac Sign'].value_counts().sort_index()

    # For consistency, use the cleaned zodiac counts
    zodiac_counts = zodiac_counts_cleaned

    # Step 3: Plot the distribution of zodiac signs
    plt.figure(figsize=(10, 6))
    zodiac_counts.plot(kind='bar', color='lightcoral')
    plt.title('Distribution of Actors by Zodiac Sign')
    plt.xlabel('Zodiac Sign')
    plt.ylabel('Number of Actors')
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()

    # Step 4: Print the zodiac distribution (actor count per zodiac sign)
    print("Actor Count by Zodiac Sign:")
    for sign, count in zodiac_counts.items():
        print(f"{sign}: {count}")
    return CharacterMeta, CharacterMetaCleaned, zodiac_counts

def plot_zodiac_contribution_to_genres(CharacterMetaCleaned, MovieMeta, genre_counts):
    # Ensure we use the cleaned CharacterMeta dataset
    merged_data = pd.merge(CharacterMetaCleaned, MovieMeta, on='Wikipedia movie ID', how='inner')

    # Count the genres by zodiac
    genre_counts_by_zodiac = merged_data.groupby(['Zodiac Sign', 'Cleaned Movie genres']).size().reset_index(name='Count')

    # Calculate total genre counts
    total_genre_counts = genre_counts_by_zodiac.groupby('Cleaned Movie genres')['Count'].sum().reset_index(name='Total Genre Count')

    # Get the top 10 genres by total count
    top_genres = total_genre_counts.nlargest(10, 'Total Genre Count')['Cleaned Movie genres']

    # Filter the data to include only the top 10 genres
    genre_counts_by_zodiac = genre_counts_by_zodiac[genre_counts_by_zodiac['Cleaned Movie genres'].isin(top_genres)]

    # Recalculate the total counts for the filtered genres
    total_genre_counts = genre_counts_by_zodiac.groupby('Cleaned Movie genres')['Count'].sum().reset_index(name='Total Genre Count')

    # Merge and calculate percentage contribution
    genre_counts_by_zodiac = pd.merge(genre_counts_by_zodiac, total_genre_counts, on='Cleaned Movie genres')
    genre_counts_by_zodiac['Percentage Contribution'] = (genre_counts_by_zodiac['Count'] / genre_counts_by_zodiac['Total Genre Count']) * 100

    # Filter to include both the top 3 and bottom 3 zodiac signs by percentage for each genre
    top_and_bottom_3_zodiac_by_genre = genre_counts_by_zodiac.groupby('Cleaned Movie genres').apply(
        lambda group: pd.concat([
            group.nlargest(3, 'Percentage Contribution'),
            group.nsmallest(3, 'Percentage Contribution').iloc[::-1]  # Reverse the order of the smallest 3
        ])
    ).reset_index(drop=True)

    # Plot the filtered data
    plt.figure(figsize=(18, 12))  # Increase figure size to accommodate labels and legends

    for genre, group in top_and_bottom_3_zodiac_by_genre.groupby('Cleaned Movie genres'):
        plt.bar(group['Zodiac Sign'] + f' ({genre})', group['Percentage Contribution'], label=genre)

    # Labeling the axes and title
    plt.ylabel('Percentage Contribution of Zodiac Sign to Genre')
    plt.xlabel('Zodiac Sign by Genre')
    plt.title('Top and Bottom 3 Zodiac Signs Contribution to Top 10 Genres')

    # Rotate x-axis labels and align for better readability
    plt.xticks(rotation=45, ha='right')

    # Adjust the layout manually without using tight_layout
    plt.subplots_adjust(left=0.1, right=0.9, top=0.9, bottom=0.35)  # Custom margins

    # Display legend outside of the plot area
    plt.legend(title='Genre', bbox_to_anchor=(1.05, 1), loc='upper left')

    # Show the plot
    plt.show()

    # Print the filtered contributions
    print("Top and Bottom 3 Zodiac Signs Contribution to Each of the Top 10 Genres:")
    for genre, group in top_and_bottom_3_zodiac_by_genre.groupby('Cleaned Movie genres'):
        print(f"\nGenre: {genre}")
        for _, row in group.iterrows():
            print(f"  Zodiac Sign: {row['Zodiac Sign']} - Contribution: {row['Percentage Contribution']:.2f}%")
    return merged_data

def plot_zodiac_weighted_contribution_to_genres(genre_counts_by_zodiac, zodiac_counts):
    # Calculate the total number of actors
    total_actors = zodiac_counts.sum()

    # Calculate the average actor count (total actors divided by 12)
    average_actor_count = total_actors / 12

    # Calculate the weight for each zodiac sign based on the average actor count
    zodiac_weights = average_actor_count / zodiac_counts

    # Print the weight for each zodiac sign
    print(f"Total unique actors: {total_actors}")
    print("\nZodiac Sign Weights:")
    for zodiac, weight in zodiac_weights.items():
        print(f"  Zodiac Sign: {zodiac} - Weight: {weight:.2f}")

    # Apply the weights to the genre counts by zodiac (multiply percentage by weight)
    genre_counts_by_zodiac['Weighted Contribution'] = genre_counts_by_zodiac.apply(
        lambda row: row['Percentage Contribution'] * zodiac_weights.get(row['Zodiac Sign'], 1), axis=1
    )

    # Filter to include both the top 3 and bottom 3 zodiac signs by percentage for each genre
    top_and_bottom_3_zodiac_by_genre = genre_counts_by_zodiac.groupby('Cleaned Movie genres').apply(
        lambda group: pd.concat([
            group.nlargest(3, 'Weighted Contribution'),
            group.nsmallest(3, 'Weighted Contribution').iloc[::-1]  # Reverse the order of the smallest 3
        ])
    ).reset_index(drop=True)

    # Plot the filtered data
    plt.figure(figsize=(18, 12))  # Increase figure size to accommodate labels and legends

    for genre, group in top_and_bottom_3_zodiac_by_genre.groupby('Cleaned Movie genres'):
        plt.bar(group['Zodiac Sign'] + f' ({genre})', group['Weighted Contribution'], label=genre)

    # Labeling the axes and title
    plt.ylabel('Weighted Contribution of Zodiac Sign to Genre')
    plt.xlabel('Zodiac Sign by Genre')
    plt.title('Top and Bottom 3 Zodiac Signs Contribution to Top 10 Genres')

    # Rotate x-axis labels and align for better readability
    plt.xticks(rotation=45, ha='right')

    # Adjust the layout manually without using tight_layout
    plt.subplots_adjust(left=0.1, right=0.9, top=0.9, bottom=0.35)  # Custom margins

    # Display legend outside of the plot area
    plt.legend(title='Genre', bbox_to_anchor=(1.05, 1), loc='upper left')

    # Show the plot
    plt.show()

    # Print the filtered contributions
    print("Top and Bottom 3 Zodiac Signs Contribution to Each of the Top 10 Genres:")
    for genre, group in top_and_bottom_3_zodiac_by_genre.groupby('Cleaned Movie genres'):
        print(f"\nGenre: {genre}")
        for _, row in group.iterrows():
            print(f"  Zodiac Sign: {row['Zodiac Sign']} - Weighted Contribution: {row['Weighted Contribution']:.2f}%")
            

