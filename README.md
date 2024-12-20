# Actors & Astrology: Zodiac Trends in Movie Field

<br>

## Abstract
Astrology, an ancient practice that predicts present and future events through the movements of celestial bodies, remains popular despite a lack of scientific validation. Many continue to believe that individuals born under different zodiac signs exhibit distinct personality traits. Our project aims to use statistical methods to examine whether zodiac-related trends exist in the film industry, potentially explaining why such pseudoscientific beliefs persist.

To explore these trends, we first analyze the distribution of actors' zodiac signs based on their birthdates. We then investigate whether individuals of different zodiac signs exhibit different patterns within the film industry, such as genre preferences or the types of roles they are cast in. In this stage, we plan to use large language models (LLMs) to obtain data on role types, validating the accuracy of this information to ensure reliable analysis. Finally, we plan to evaluate if there are some factors will influence these distributions and tendencies, such as gender and nationality. 
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
OSCAR Dataset: [Link needed] This dataset is used to explore the relationship between constellations and the Academy Awards (Oscars).

#### Self-Generated Dataset  
We also created a new dataset using GPT and Claude, which examines the relationship between constellations and whether actors played leading roles.

<br><br>

## Methodologies

#### 1. Data Cleaning & Preparation
First, we carefully reviewed each dataset to assess whether its columns were relevant to our project and whether the qualities of the columns were good. Next, we performed data cleaning, removed any inconsistencies and corrupted data lines. After that, we grouped actors by zodiac sign based on their birthdates, and grouped the movies based on its genre.

#### 2. Data Enrichment: 
We created the dataset of power roles. First, we randomly selected a sample of characters and manually labeled their power roles—such as hero or bad guy. Then, we  used LLMs to determine the power roles of these samples and validate the results. After validation, we applied the LLMs to classify power roles across the entire dataset.
We also introduced and utilized the OSCAR dataset.

#### 3. Data Analysis

(1) **Distribution Analysis**: After grouping the actors into different zodiac signs, we calculated the distribution. Then we utilised chi-square to determine if the differences between the zodiac signs are significant or not. We also checked the gender distribution of the actors.  
(2) **Genre Analysis**:  Preferences for movie genres among actors of different zodiac signs: ① Calculate the distribution of different genre ② Calculate the genre distribution of each sign ③ Divide the two proportion ④ use statstical method to test if the trends are significant.  
(3) **Casting preferences** : ① Calculate the distribution of different genre ② Calculate the genre distribution of each sign③ Divide the two proportion ④ use statstical method to test if the trends are significant.  
(4) **Number of Movies** : we calculated the average number of movie the actor perform for each zodiac sign and use use statstical method to test if the differences between the zodiac signs are significant or not.  
(5) **Power Role Analysis**: ① Map each actor’s zodiac sign to their respective role ② Use statistical methods (e.g., chi-square tests, logistic regression) to determine if there is a significant association between zodiac signs and the likelihood of being cast in specific roles. Analyze trends and compare how often actors of certain signs are cast as heroes versus villains or sidekicks.  
(6) **Career longevity**: 

(7) **Type Diversity Index**: 

(8) **Oscar Analysis**: 

<br><br>

## Timeline

| Date       | Milestone                                             | Details                                                                                 |
|------------|-------------------------------------------------------|------------------------------------------------------------------|
| **11.15**  | Data Cleaning and Preparation                         | Initial analysis for Data Analysis goals (1) & (2)                                           |
| **11.29**  | Data Enrichment & Demographic Factors Analysis        | Enrichment and demographic analysis for Data Analysis (1) & (2), plus Deadline for Homework 2       |
| **12.06**  | Finish Data Analysis                                  | Complete all analysis tasks                                                            |
| **12.13**  | Report Writing                                        | Begin drafting and finalizing the project report                                       |
| **12.20**  | Deadline: Milestone 3                                 | Submit the final project deliverables                                                 |

<br><br>

## Team Distribution

| Member           | Primary Contributions                     |
|-------------------|------------------------------------------|
| Zhichen FANG         | (1) (3) (4) (5) (6) (8)& Data Enrichment & README  |
| Jiaqi DING           |  (1) (5) & Data Cleaning & Homework & README   |
| Xin Huang              | (2) (3) (4) (5) (7)   |
| Maksymiliann Schoeffel    | (2) (5) & Homework & Data story constructing     |
| ~~Zoyed~~        | ~~Never showed up and considered quit this project with TA approval~~ |
| Yi REN (joined team later)    | Monitoring and Optimising & Homework & Data story constructing    |

Note:
1. (n) means the task lindex.  
2. All group members engaged in demographic factors analysis, and working for the final data story. All work are discussed and optimized within group.  
3. we have assigned some member to do the homework while others doing project.  
<br><br>
## Project Structure

```
├── data                        <- data here
│   ├── ProcessedDatasets                <- cleaned movie dataset and processed Oscar
│   ├── RawDatasets                      <- raw datasets: MovieSummary and Oscar
│
├── figures                     <- Graph for Analysis
├── src                         <- Source code
│   ├── data                            <- Not used
│   ├── models                          <- Not used
│   ├── scripts                         <- Not used
│   ├── utils                           <- Utility directory contains the functions used in results
│
├── tests                       <- containing all the utils and test python files
│
├── results.ipynb               <- well-structured notebook showing the results
│
├── .gitignore                  
├── pip_requirements.txt        
└── README.md
```



