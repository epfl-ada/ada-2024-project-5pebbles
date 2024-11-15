import re
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from scipy.stats import norm, chisquare
import sys
import os
from datetime import datetime
import numpy as np


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


def convert_to_date_only(date_str):
    if 'T' in date_str:
        return date_str[:10]  # Extract only the 'YYYY-MM-DD' part
    return date_str


def get_zodiac_sign(birthdate):
    if pd.isna(birthdate):  # Check for NaN or NaT
        return None

    # Convert string to datetime if necessary
    if isinstance(birthdate, str):
        try:
            birthdate = pd.to_datetime(birthdate)  # Convert to datetime
        except ValueError:
            return None  # Return None for invalid date strings

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
    elif "12-22" <= month_day <= "01-19":
        return "Capricorn"
    elif "01-20" <= month_day <= "02-18":
        return "Aquarius"
    elif "02-19" <= month_day <= "03-20":
        return "Pisces"
    else:
        return None


def illstrate_zodiac_distribution(zodiac_counts):
    # zodiac_counts = CharacterMeta_cleaned['Zodiac Sign'].value_counts(dropna=False).reset_index()
    # zodiac_counts.columns = ['Zodiac Sign', 'Count']
    # zodiac_counts = zodiac_counts.sort_values(by="Count", ascending=False)
    plt.figure(figsize=(10, 6))

    # Create a bar plot with a color map
    sns.barplot(x='Count', y='Zodiac Sign', data=zodiac_counts, palette='coolwarm_r', hue='Zodiac Sign', legend=False)

    # Add labels and title
    plt.title('Distribution of Zodiac Signs among Actors', fontsize=16)
    plt.xlabel('Count of Actors', fontsize=12)
    plt.ylabel('Zodiac Sign', fontsize=12)

    plt.tight_layout()
    plt.show()


def calculate_z_scores(zodiac_counts):
    # zodiac_counts = CharacterMeta_cleaned['Zodiac Sign'].value_counts(dropna=False).reset_index()
    # zodiac_counts.columns = ['Zodiac Sign', 'Count']
    # zodiac_counts = zodiac_counts.sort_values(by="Count", ascending=False)
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


def calculate_chi_square(zodiac_counts):
    # zodiac_counts = CharacterMeta_cleaned['Zodiac Sign'].value_counts(dropna=False).reset_index()
    # zodiac_counts.columns = ['Zodiac Sign', 'Count']
    # zodiac_counts = zodiac_counts.sort_values(by="Count", ascending=False)
    total_count = zodiac_counts['Count'].sum()
    # Expected uniform distribution
    expected_counts = [total_count / len(zodiac_counts['Zodiac Sign'].dropna())] * len(
        zodiac_counts['Zodiac Sign'].dropna())

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