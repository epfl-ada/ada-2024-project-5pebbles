import scipy.stats as stats
import pandas as pd

def ANOVA_Role_Num(actor_longevity, alpha=0.05):
    groups = [actor_longevity[actor_longevity['Zodiac Sign'] == zodiac][''] for zodiac in
              actor_longevity['Zodiac Sign'].unique()]
    f_stat, p_value = stats.f_oneway(*groups)
    print(f"F-statistic: {f_stat}")
    print(f"P-value: {p_value}")

    if p_value < alpha:
        print("The difference in role counts among zodiac signs is significant")
    else:
        print("The difference in role counts among zodiac signs is not significant.")