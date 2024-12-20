# Actors & Astrology: Zodiac Trends in Movie Field

<br>

## Website for Our Data Story
https://maksymiliann.github.io/Team-5Pebbles/

## Abstract
Astrology, an ancient practice connecting celestial movements to earthly events, continues to influence modern beliefs despite its lack of scientific foundation. Our project delves into the intersection of astrology and the film industry by examining zodiac-related trends among actors. Using statistical methods and enriched datasets, we uncover notable patterns linking zodiac signs to various aspects of actors’ careers. Our project offers insights into the persistence of pseudoscientific beliefs and their subtle manifestations in cultural industries like cinema.


Key findings include a non-uniform distribution of actors across zodiac signs, with certain signs dominating in representation. Genre preferences and casting tendencies show significant variation by zodiac sign, revealing potential biases in the industry. Analysis of actors' roles indicates patterns in the assignment of power roles (e.g., heroes and villains) and correlations between zodiac signs and career longevity. Additionally, we observe varying probabilities of Oscar wins among zodiac signs.

<br><br>

## Research Questions

These questions serve as guideline of our project.

(1) **Distribution Analysis**: Is the distribution of actors across zodiac signs uniform, or are certain signs more represented than others? Which zodiac sign has the highest representation among actors?  What is the distribution of some domographic factors like gender?

(2) **Genre Analysis**: Do actors of different zodiac signs tend to prefer specific movie genres?

(3) **Casting preferences**: Do certain movie genres show a preference for actors of specific zodiac signs during casting?

(4) **Number of Movies acted**: What is the difference in the number of movies performed by actors of different zodiac signs?

(5) **Power Role Analysis**: How do zodiac signs influence the assignment of power roles, such as heroes, villains, and sidekicks?  

(6) **Career longevity**: How do zodiac signs correlate with actors' career longevity, examining the timespan from their first to last movie appearances?  

(7) **Type Diversity Index**: Which zodiac signs demonstrate greater versatility in genre-switching, and how successful are they in different genres throughout their careers?  

(8) **Oscar Analysis**: Are actors of different zodiac signs equally likely to win an Oscar? Which zodiac sign has the highest probability of winning an Oscar?

<br><br>

## Additional datasets
#### External Dataset  
OSCAR Dataset: [https://data.world/crowdflower/academy-awards-demographics] This dataset is used to explore the relationship between constellations and the Academy Awards (Oscars).

#### Self-Generated Dataset  
We also created a new dataset using GPT and Claude, which examines the relationship between constellations and whether actors played leading roles.

##### Data Preprocessing
The initial dataset was created by merging three original files from the CMU Movie Summary Corpus:
- Character metadata file (containing character and actor information)
- Movie metadata file (containing movie titles and IDs)
- Plot summaries file (containing movie plots)

These files were combined to create a comprehensive dataset where each entry contains both character and movie information.

##### AI Analysis Process

###### Prompt Design
For each character, we constructed a standardized prompt containing:
- Movie title
- Complete plot summary
- List of all actors in the movie
- Target actor name

The prompt asks the AI to determine whether the target actor plays a main character, requiring a simple "True" or "False" response.

###### Dual AI Validation
We employed two state-of-the-art language models:
- GPT-4o mini (OpenAI)
- Claude-3.5 Haiku (Anthropic)

Each model processed the entire dataset independently:
- GPT-4o mini provided decisions for 78,265 characters
- Claude-3.5 Haiku provided decisions for 78,263 characters

###### Cross-Validation Results
The final dataset was created by cross-referencing decisions from both AIs:
- Total characters analyzed: 103,071
- Characters with AI agreement: 67,580
- Identified main characters (with agreement): 20,773

##### Validation
A manual verification of 50 randomly selected samples from the AI-agreed dataset was conducted against online sources, confirming high reliability of the cross-validated results.


<br><br>

## Methodologies

#### 1. Data Cleaning & Preparation
First, we carefully reviewed each dataset to assess whether its columns were relevant to our project and whether the qualities of the columns were good. Next, we performed data cleaning, removed any inconsistencies and corrupted data lines. After that, we grouped actors by zodiac sign based on their birthdates, and grouped the movies based on its genre.

#### 2. Data Enrichment: 
We created the dataset of power roles. First, we randomly selected a sample of characters and manually labeled their power roles—such as hero or bad guy. Then, we  used LLMs to determine the power roles of these samples and validate the results. After validation, we applied the LLMs to classify power roles across the entire dataset.
We also introduced and utilized the OSCAR dataset.

#### 3. Data Analysis

(1) **Distribution Analysis**: ① Grouping the actors into different zodiac signs ② calculated the distribution ③ utilised chi-square to determine if the differences between the zodiac signs are significant or not ④ checked the gender distribution of the actors.  
(2) **Genre Analysis**: ① Calculate the overall distribution of film genres in the dataset ② Calculate the genre distribution for each zodiac sign ③ Compare both distributions to identify over/under-representation patterns ④ Use chi-square tests and ANOVA to determine if the genre preferences across zodiac signs are statistically significant.
(3) **Casting preferences** : ① Calculate the distribution of different genre ② Calculate the genre distribution of each sign ③ Divide the two proportion ④ use statstical method to test if the trends are significant.  
(4) **Number of Movies** :  ① calculate the average number of movie the actor perform for each zodiac sign ② use use statstical method to test if the differences between the zodiac signs are significant or not.  
(5) **Power Role Analysis**: ① Map each actor's zodiac sign to their respective leading/supporting roles using character billing position and role significance ② Calculate the lead role ratio for each zodiac sign ③ Use statistical methods (chi-square tests, ANOVA) to determine if there are significant associations between zodiac signs and lead roles ④ Analyze the interaction effects between zodiac signs and film genres for lead roles.
(6) **Career longevity**: ① calculated the average career entry time, retirement time, and the time span between them for actors of each zodiac sign.  ② Statistical tests were then applied to determine whether the observed differences in these averages across zodiac signs were significant.  
(7) **Type Diversity Index**: ① Developed a comprehensive Genre Diversity Index (GDI) combining Raw Diversity Score (30%), Shannon Diversity Index (40%), and Genre Balance Score (30%) ② Calculated GDI scores for actors of each zodiac sign ③ Used Kruskal-Wallis test to determine if the differences in GDI scores between zodiac signs are statistically significant ④ Analyzed the distribution patterns and variability of GDI scores across different signs.
(8) **Oscar Analysis**: ① Calculate the zodiac distribution of Oscar winners Calculate the awarding rate of different zodiac signs ② Use z-score and Chi-square Test to test if the differences of awarding rate among different zodiac signs are significant

<br><br>

## Timeline

| Date       | Description                                             | Details                                                                                 |
|------------|-------------------------------------------------------|------------------------------------------------------------------|
| **11.15**  | Data Cleaning and Preparation                         | Initial analysis for Data Analysis goals (1) & (2)                                           |
| **11.29**  | Data Enrichment & Demographic Factors Analysis        | Enrichment and demographic analysis, plus Deadline for Homework 2       |
| **12.06**  | Finish Major Data Analysis                                  | Completed all analysis tasks                                                            |
| **12.13**  | Refinement and Story website building                           | Begin drafting and finalizing the project report                                       |
| **12.20**  | Deadline: Milestone 3                                 | Submit the final project deliverables                                                 |

<br><br>

## Team Distribution

| Member           | Primary Contributions                     |
|-------------------|------------------------------------------|
| Zhichen FANG         | (1) (2) (4) (6) (8) & Introducing Oscar dataset & README  |
| Jiaqi DING           |  (1) (5) & Data Cleaning & Homework & README   |
| Xin Huang              | (2) (5) (7)  & Generating power role dataset |
| Maksymiliann Schoeffel    | (2) (3) & Homework & Website constructing    |
| ~~Zoyed~~        | ~~Never showed up and considered quit this project with TA approval~~ |
| Yi REN (joined team later)    | (3) & Coordination & Homework   |

Note:
1. (n) means the task lindex.  
2. All group members contributed to compiling portions of the final data story. All work was collaboratively discussed and optimized within the group.  
3. we have assigned some member to do the homework while others doing project.  
<br><br>
## Project Structure

```
├── data                        <- data here
│   ├── ProcessedDatasets                <- cleaned movie dataset, processed Oscar and self generate data
│   ├── RawDatasets                      <- raw datasets: MovieSummary and Oscar
│
├── figures                     <- Graph for Analysis
├── src                         <- Source code
│   ├── data                            <- data loader
│   ├── models                          <- Not used
│   ├── scripts                         <- Not used
│   ├── utils                           <- Utility directory contains the functions used in results
│
├── tests                       <- containing test python files and the code using llms to generate the additional data  
│
├── results.ipynb               <- well-structured notebook showing the results
│
├── .gitignore                  
├── pip_requirements.txt        
└── README.md
```



