#First, we should import the dataset.
import pandas as pd

def getCharacterMeta(filepath):
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
        'Freebase actor ID'
    ]
    return CharacterMeta

# Load Data
file_path = "../data/RawDatasets/MovieSummaries/character.metadata.tsv"
CharacterMeta = getCharacterMeta(file_path)

total_records = len(CharacterMeta)
print(f"Total records: {total_records}")

#To get as much as valid data as we can, I want to check the data format, and transform some of them if possible. Now, I will explore the data format for the 'Actor date of birth' column.
df_dates = CharacterMeta['Actor date of birth'].fillna("").copy()
df_dates = "'" + df_dates + "'"

# Get value_counts from dataset, and reset index
date_formats = df_dates.value_counts(dropna=False).reset_index()
date_formats.columns = ['Presentation', 'Count']
date_formats['Length'] = date_formats['Presentation'].apply(len)-2  # Account for quotes

date_formats = date_formats.sort_values(by='Length')

combined_formats = pd.concat([date_formats.head(), date_formats.tail(5)])
print("Date Formats in Actor date of birth:\n", combined_formats)

import re


def classify_date_format(date_str):
    if pd.isna(date_str) or date_str.strip() == '':
        return 'Empty'
    elif re.match(r'^\d{4}$', date_str):  # Matches year only format (e.g., '1953')
        return 'Year only'
    elif re.match(r'^\d{4}-\d{2}$', date_str):  # Matches year-month format (e.g., '1938-01')
        return 'Year-Month'
    elif re.match(r'^\d{4}-\d{2}-\d{2}$', date_str):  # Matches full date (e.g., '1971-10-06')
        return 'Full date (YYYY-MM-DD)'
    elif re.match(r'^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}(:\d{2})?([+-]\d{2}:\d{2})?$', date_str):
        # Matches datetime with optional seconds and timezone (e.g., '1961-08-04T19:24-10:00')
        return 'Datetime with timezone'
    else:
        return 'Other'

CharacterMeta['Date Format Type'] = CharacterMeta['Actor date of birth'].fillna("").apply(classify_date_format)
date_format_counts = CharacterMeta['Date Format Type'].value_counts(dropna=False).reset_index()
date_format_counts.columns = ['Date Format Type', 'Count']

print(date_format_counts)

# Filter to show only rows where the Date Format Type is 'Other'
# These code were run several times to gradually clean out the 'other' format than full date format.
other_formats = CharacterMeta[CharacterMeta['Date Format Type'] == 'Other']

other_format_counts = other_formats['Actor date of birth'].value_counts().reset_index()
other_format_counts.columns = ['Actor date of birth', 'Count']

if other_format_counts.empty:
    print('Completed: types of data representation are all detected.')
else:
    print(other_format_counts)

#After sorting out all the datatypes, we can start cleaning dataset.
CharacterMeta_cleaned = CharacterMeta.copy()

# Filter out rows with "Empty", "Year only", and "Year-Month" in the 'Date Format Type' column
CharacterMeta_cleaned = CharacterMeta_cleaned[
    ~CharacterMeta_cleaned['Date Format Type'].isin(['Empty', 'Year only', 'Year-Month'])
]


def convert_to_date_only(date_str):
    if 'T' in date_str:
        return date_str[:10]  # Extract only the 'YYYY-MM-DD' part
    return date_str
    
CharacterMeta_cleaned['Actor date of birth'] = CharacterMeta_cleaned['Actor date of birth'].apply(convert_to_date_only)


# Verify
CharacterMeta_cleaned['Date Format Type'] = CharacterMeta_cleaned['Actor date of birth'].fillna("").apply(classify_date_format)
date_format_counts = CharacterMeta_cleaned['Date Format Type'].value_counts(dropna=False).reset_index()
date_format_counts.columns = ['Date Format Type', 'Count']
print(date_format_counts)

# Check again
missing_birthdates = CharacterMeta_cleaned['Actor date of birth'].isna().sum()
print(f"Number of missing or invalid birthdates: {missing_birthdates}")
#Now, all the data are in the form of YYYY-MM-DD. However, we can't simply trust the data recorders just like that. What if a 0000-00-00 exsits? After searching, we find a useful library called datetime, which can automatically convert invalid data to none.
# Create a backup of the original 'Actor date of birth' column
CharacterMeta_cleaned['Original Actor date of birth'] = CharacterMeta_cleaned['Actor date of birth']

# Attempt to convert 'Actor date of birth' to datetime, marking invalid ones as NaT
CharacterMeta_cleaned['Converted Date'] = pd.to_datetime(CharacterMeta_cleaned['Actor date of birth'], errors='coerce')

invalid_dates = CharacterMeta_cleaned[CharacterMeta_cleaned['Converted Date'].isna()]

print("Invalid dates before cleaning:")
print(invalid_dates[['Original Actor date of birth']])

# Drop rows where 'Converted Date' is NaT
CharacterMeta_cleaned = CharacterMeta_cleaned.dropna(subset=['Converted Date'])

# Replace the old 'Actor date of birth' with 'Converted Date' and drop 'Original Actor date of birth'
CharacterMeta_cleaned['Actor date of birth'] = CharacterMeta_cleaned['Converted Date']
CharacterMeta_cleaned = CharacterMeta_cleaned.drop(columns=['Original Actor date of birth', 'Converted Date', 'Date Format Type'])

print(CharacterMeta_cleaned.head())
print(f"\nNumber of remaining rows: {len(CharacterMeta_cleaned)}")

#Now the data is cleaned. These data will be used to represent the zodiac. It's time to define the zodiac sign function.
# Zodiac sign function provided by user (modified to clarify the Capricorn range)
def get_zodiac_sign(birthdate):
    if pd.isna(birthdate):  # Check for NaT
        return None
    month_day = birthdate.strftime("%m-%d")  # Extract 'MM-DD' as a string
    if "03-21" <= month_day <= "04-19":
        return "Aries"
    elif "04-20" <= month_day <= "05-20":
        return "Taurus"
    elif "05-21" <= month_day <= "06-20":
        return "Gemini"
    elif "06-21" <= month_day <= "07-22":
        return "Cancer"
    elif "07-23" <= month_day <= "08-22":
        return "Leo"
    elif "08-23" <= month_day <= "09-22":
        return "Virgo"
    elif "09-23" <= month_day <= "10-22":
        return "Libra"
    elif "10-23" <= month_day <= "11-21":
        return "Scorpio"
    elif "11-22" <= month_day <= "12-21":
        return "Sagittarius"
    # elif "12-22" <= month_day <= "12-31" or "01-01" <= month_day <= "01-19":
    elif "12-22" <= month_day or month_day <= "01-19":
        return "Capricorn"
    elif "01-20" <= month_day <= "02-18":
        return "Aquarius"
    elif "02-19" <= month_day <= "03-20":
        return "Pisces"
    return None



CharacterMeta_cleaned['Zodiac Sign'] = CharacterMeta_cleaned['Actor date of birth'].apply(get_zodiac_sign)

# count the occurrences of each zodiac
zodiac_counts = CharacterMeta_cleaned['Zodiac Sign'].value_counts(dropna=False).reset_index()
zodiac_counts.columns = ['Zodiac Sign', 'Count']

zodiac_counts = zodiac_counts.sort_values(by="Count", ascending=False)
print(zodiac_counts)

import seaborn as sns
import matplotlib.pyplot as plt

def illstrate_zodiac_distribution():
    plt.figure(figsize=(10, 6))
    
    # Create a bar plot with a color map
    sns.barplot(x='Count', y='Zodiac Sign', data=zodiac_counts, palette='coolwarm_r',hue='Zodiac Sign',legend=False)
    
    # Add labels and title
    plt.title('Distribution of Zodiac Signs among Actors', fontsize=16)
    plt.xlabel('Count of Actors', fontsize=12)
    plt.ylabel('Zodiac Sign', fontsize=12)
    
    plt.tight_layout()
    plt.show()
illstrate_zodiac_distribution()

#Compare observed proportion for each zodiac sign to the overall mean proportion.
from scipy.stats import norm
import numpy as np
def calculate_z_scores():
    # Compute the observed proportions
    total_count = zodiac_counts['Count'].sum()
    zodiac_counts['Proportion'] = zodiac_counts['Count'] / total_count
    
    # Compute the overall mean proportion
    mean_proportion = 1 / len(zodiac_counts['Zodiac Sign'].dropna())
    std_proportion = np.sqrt(mean_proportion * (1 - mean_proportion) / total_count)
    
    # Calculate z-scores and p-values
    zodiac_counts['Z-Score'] = (zodiac_counts['Proportion'] - mean_proportion) / std_proportion
    zodiac_counts['P-Value'] = 2 * (1 - norm.cdf(abs(zodiac_counts['Z-Score'])))
    
    # Check significance level = 0.05
    zodiac_counts['Significant?'] = zodiac_counts['P-Value'] < 0.05
    
    print(zodiac_counts[['Zodiac Sign', 'Proportion', 'Z-Score', 'P-Value', 'Significant?']])
calculate_z_scores()

#Compare the observed zodiac distribution to an expected uniform distribution.
from scipy.stats import chisquare

def calculate_chi_square():
    total_count = zodiac_counts['Count'].sum()
    # Expected uniform distribution
    expected_counts = [total_count / len(zodiac_counts['Zodiac Sign'].dropna())] * len(zodiac_counts['Zodiac Sign'].dropna())
    
    # Observed counts
    observed_counts = zodiac_counts['Count'].dropna()
    
    chi2_stat, p_value = chisquare(f_obs=observed_counts, f_exp=expected_counts)
    
    print(f"Chi-Square Statistic: {chi2_stat}")
    print(f"P-Value: {p_value}")
    
    # Check significance level
    if p_value < 0.05:
        print("Reject H0: The zodiac distribution is significantly different from uniform.")
    else:
        print("Fail to reject H0: The zodiac distribution is not significantly different from uniform.")
calculate_chi_square()

import os

output_directory = '../data/ProcessedDatasets/'
output_filename = 'cleaned.character.metadata.tsv'
output_path = os.path.join(output_directory, output_filename)

# Ensure the directory exists
os.makedirs(output_directory, exist_ok=True)

# Check if the file already exists
if not os.path.exists(output_path):
    CharacterMeta_cleaned.to_csv(output_path, sep='\t', index=False)
    print(f"Dataset successfully exported to: {output_path}")
else:
    print(f"File already exists: {output_path}. Export skipped.")
file_path = "../data/ProcessedDatasets/cleaned.character.metadata.tsv"
def getCharacterMeta(filepath):
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
        'Zodiac sign'
    ]
    return CharacterMeta

CharacterMeta = getCharacterMeta(file_path)
total_records = len(CharacterMeta)
print(f"Total records: {total_records}")
