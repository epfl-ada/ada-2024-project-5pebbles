import pandas as pd
import re





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