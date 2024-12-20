from langchain_anthropic import ChatAnthropic
import pandas as pd
import json
import os
from tqdm import tqdm

class ClaudeAnalyzer:
    def __init__(self, api_keys_path='MovieSummaries/api_keys.json'):
        with open(api_keys_path, 'r') as f:
            api_keys = json.load(f)
            
        self.claude_model = ChatAnthropic(
            model="claude-3-5-haiku-20241022",
            api_key=api_keys['anthropic_key'],
            temperature=0,
            max_tokens=1024
        )
        
        self.temp_file = 'MovieSummaries/temp_claude_results.tsv'
        self.final_file = 'MovieSummaries/character_metadata_with_claude.tsv'
        self.plot_file = 'MovieSummaries/plot_summaries.txt'
        self.plot_summaries = self._load_plot_summaries()
    
    
    def _load_plot_summaries(self):
        summaries = {}
        with open(self.plot_file, 'r', encoding='utf-8') as f:
            for line in f:
                wiki_id, summary = line.strip().split('\t', 1)
                summaries[wiki_id] = summary
        return summaries
    
    def _load_existing_results(self):
        if os.path.exists(self.temp_file):
            return pd.read_csv(self.temp_file, sep='\t')
        return None
    
    def _create_prompt(self, movie_name, plot_summary, all_actors, target_actor):
        prompt = f"""
        Movie: {movie_name}
        Plot Summary: {plot_summary}
        All actors in the movie: {', '.join(all_actors)}
        
        Is the actor "{target_actor}" a main character in this movie?
        Please only answer with "True" if they are a main character, or "False" if they are not.
        ANSWER WITH ONLY TRUE OR FALSE.
        """
        return prompt
    
    def extract_decision(self, response):
        response = response.lower()
        has_true = 'true' in response
        has_false = 'false' in response
        
        if (has_true and has_false) or (not has_true and not has_false):
            return None
        return has_true
    
    
    def analyze_characters(self, character_data, batch_size=100):
        existing_results = self._load_existing_results()
        if existing_results is not None:
            character_data = pd.concat([
                character_data,
                existing_results[['Wikipedia movie ID', 'Actor name', 'claude_decision']]
            ]).drop_duplicates(subset=['Wikipedia movie ID', 'Actor name'], keep='last')
        
        if 'claude_decision' not in character_data.columns:
            character_data['claude_decision'] = None
        
        progress_bar = tqdm(total=len(character_data))
        count = 0
        
        for wiki_id, group in character_data.groupby('Wikipedia movie ID'):
            wiki_id_str = str(wiki_id)
            if wiki_id_str not in self.plot_summaries:
                continue
                
            movie_name = group['Movie name'].iloc[0]
            plot_summary = self.plot_summaries[wiki_id_str]
            all_actors = group['Actor name'].tolist()
            
            for _, row in group.iterrows():
                if pd.isna(row['claude_decision']):
                    try:
                        prompt = self._create_prompt(movie_name, plot_summary, all_actors, row['Actor name'])
                        response = self.claude_model.predict(prompt).strip().lower()
                        decision = self.extract_decision(response)
                        
                        character_data.loc[row.name, 'claude_decision'] = decision
                        count += 1
                        
                        if count % batch_size == 0:
                            character_data.to_csv(self.temp_file, sep='\t', index=False)
                            
                    except Exception as e:
                        print(f"Error processing {row['Actor name']} in {movie_name}: {str(e)}")
                
                progress_bar.update(1)
        
        progress_bar.close()
        character_data.to_csv(self.final_file, sep='\t', index=False)
        return character_data

def main():
    # Load the character metadata
    character_data = pd.read_csv('MovieSummaries/character_metadata_with_movies.tsv', sep='\t')
    
    # Initialize analyzer
    analyzer = ClaudeAnalyzer()
    
    # Run analysis
    result_data = analyzer.analyze_characters(character_data)
    
    print("Analysis completed!")
    print(f"Total characters processed: {len(result_data)}")
    print(f"Characters with Claude decision: {result_data['claude_decision'].notna().sum()}")
    print("\nSample of results:")
    print(result_data[['Movie name', 'Actor name', 'claude_decision']].sample(5))

if __name__ == "__main__":
    main()