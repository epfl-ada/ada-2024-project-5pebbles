import pandas as pd
import gzip

file_path = '../data/RawDatasets/corenlp_plot_summaries/1031545.xml.gz'


with gzip.open(file_path, 'rt', encoding='utf-8') as file:
    content = file.readlines()

for line in content[:30]:  # Adjust the number to see more or fewer lines. Now it's 0~30
    print(line.strip())

import os
import gzip
import xml.etree.ElementTree as ET
import re

# Function to split a filename into numeric and non-numeric parts for natural sorting
def natural_key(filename):
    # Split the filename into a list of numeric and non-numeric parts
    return [int(part) if part.isdigit() else part for part in re.split(r'(\d+)', filename)]

# Specify the directory containing your XML files
directory = '../data/RawDatasets/corenlp_plot_summaries'

# Get all the .xml.gz files in the directory and sort them using the natural key
files = [f for f in os.listdir(directory) if f.endswith('.xml.gz')]
sorted_files = sorted(files, key=natural_key)

# Initialize counters
total_files = len(sorted_files)
processed_files = 0

for filename in sorted_files[:3]:
    print(f'Processing {filename}...')
    file_path = os.path.join(directory, filename)
    
    with gzip.open(file_path, 'rt', encoding='utf-8') as file:
        # Parse the XML content
        try:
            tree = ET.parse(file)
            root = tree.getroot()
            sentences = root.find('.//sentences')
            
            if sentences is not None:
                # Increment processed_files only once for the file
                processed_files += 1  
                
                for sentence in sentences.findall('sentence'):
                    tokens = sentence.find('tokens')
                    if tokens is not None:
                        # Extract the sentence text with proper spacing
                        sentence_text = ' '.join(token.find('word').text for token in tokens.findall('token'))
                        print(f'Extracted sentence: {sentence_text}')
                    else:
                        print('No tokens found in this sentence.')
            else:
                print('No sentences found in the file.')
                
        except ET.ParseError:
            print(f'Error parsing {filename}')

# Final output of processed file count
print(f'Total files processed: {processed_files} out of {total_files}')

def load_movie_metadata(filepath):
    # Load the metadata with appropriate column names
    column_names = ['movieId', 'uniqueId', 'title', 'releaseDate', 'duration', 'rating', 'languages', 'countries', 'genres']
    metadata_df = pd.read_csv(filepath, sep='\t', header=None, names=column_names)
    return metadata_df

def check_movie_ids_in_filenames(metadata_df, xml_folder):
    """
    Check if XML filenames correspond to movie IDs in the metadata.
    
    Parameters:
    - metadata_df (DataFrame): DataFrame containing movie metadata.
    - xml_folder (str): Path to the folder containing XML files.
    
    Returns:
    - matches (list): A list of filenames that match movie IDs.
    """
    movie_ids = metadata_df['movieId'].astype(str).tolist()
    matches = []

    # Iterate over XML files in the specified directory
    for filename in os.listdir(xml_folder):
        if filename.endswith('.xml.gz'):  # Filter for XML files
            movie_id = filename.split('.')[0]  # Extract the movie ID from the filename
            if movie_id in movie_ids:
                matches.append((movie_id, filename))

    return matches
def load_movie_metadata(filepath):
    # Load the metadata with appropriate column names
    column_names = ['movieId', 'uniqueId', 'title', 'releaseDate', 'duration', 'rating', 'languages', 'countries', 'genres']
    metadata_df = pd.read_csv(filepath, sep='\t', header=None, names=column_names)
    return metadata_df

# Load movie metadata
movie_meta_filepath = '../data/RawDatasets/MovieSummaries/movie.metadata.tsv'
metadata_df = load_movie_metadata(movie_meta_filepath)

# Specify the path to your XML files
xml_folder_path = '../data/RawDatasets/corenlp_plot_summaries/'

# Check for matches
matching_files = check_movie_ids_in_filenames(metadata_df, xml_folder_path)

# Print matches
for movie_id, filename in matching_files[:10]:
    print(f"Match found: Movie ID {movie_id} corresponds to file {filename}")