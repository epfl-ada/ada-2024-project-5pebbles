import pandas as pd

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


CharacterMeta=getCharacterMeta(r'F:\courses\AppiedDataAnalysis\FinalProject\Data\MovieSummaries\MovieSummaries\character.metadata.tsv')
MovieMeta=getMovieMeta(r'F:\courses\AppiedDataAnalysis\FinalProject\Data\MovieSummaries\MovieSummaries\movie.metadata.tsv')

print(CharacterMeta['Movie release date'].isna().sum())
print(CharacterMeta.shape)
print(CharacterMeta['Actor height'].isna().sum())
print(CharacterMeta['Actor date of birth'].isna().sum())
print(CharacterMeta['Actor gender'].isna().sum())
print(CharacterMeta['Actor ethnicity'].isna().sum())
print(CharacterMeta['Actor name'].isna().sum())
print(CharacterMeta['Actor age at movie release'].isna().sum())
print(CharacterMeta['Freebase character ID'].isna().sum())
print(MovieMeta['Movie name'].isna().sum())
print(MovieMeta['Movie release date'].isna().sum())
print(MovieMeta['Movie box office revenue'].isna().sum())
print(MovieMeta['Movie runtime'].isna().sum())
print(MovieMeta['Movie languages'].isna().sum())
print(MovieMeta['Movie countries'].isna().sum())
print(MovieMeta['Movie genres'].isna().sum())
print(MovieMeta.shape)