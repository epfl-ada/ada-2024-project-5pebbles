import pandas as pd
import os
from datetime import datetime
import matplotlib.pyplot as plt
import seaborn as sns
import scipy.stats as stats

def actor_longevity_analysis(actor_longevity):
    # longevity
    actor_longevity_counts=actor_longevity.groupby('Zodiac Sign')['Career Longevity'].mean().reset_index()
    actor_longevity_counts = actor_longevity_counts.sort_values(by='Career Longevity', ascending=False)
    plt.figure(figsize=(10, 4))
    ax=sns.barplot(x='Zodiac Sign', y='Career Longevity', data=actor_longevity_counts, palette="pastel",  hue='Zodiac Sign', legend=False)
    # 手动添加数值标签
    for p in ax.patches:
        height = p.get_height()  # 获取每个条形的高度
        ax.text(
            p.get_x() + p.get_width() / 2., height,  # 条形的中心位置
            f'{height:.3f}',  # 标签内容
            ha='center', va='bottom', fontsize=12, color='black'  # 字体和位置
        )

    ax.set_ylim(9.6,10.4)
    plt.title("Average Career Longevity of Different Zodiac Signs", fontsize=16)
    plt.xlabel("Zodiac Sign", fontsize=12)
    plt.ylabel("Average Career Longevity", fontsize=12)
    plt.xticks(fontsize=10)
    plt.yticks(fontsize=10)
    plt.show()
    return


def actor_entry_age_analysis(actor_longevity):
    # min
    entry_age_counts=actor_longevity.groupby('Zodiac Sign')['min'].mean().reset_index()
    entry_age_counts = entry_age_counts.sort_values(by='min', ascending=False)
    plt.figure(figsize=(10, 4))
    ax=sns.barplot(x='Zodiac Sign',y='min', data=entry_age_counts, palette="pastel",hue='Zodiac Sign', legend=False)
    ax.set_ylim(30.3, 31.3)
    # 手动添加数值标签
    for p in ax.patches:
        height = p.get_height()  # 获取每个条形的高度
        ax.text(
            p.get_x() + p.get_width() / 2., height,  # 条形的中心位置
            f'{height:.3f}',  # 标签内容
            ha='center', va='bottom', fontsize=12, color='black'  # 字体和位置
        )

    plt.title("Average Entry Age of Zodiac Signs", fontsize=16)
    plt.xlabel("Zodiac Sign", fontsize=12)
    plt.ylabel("Average Entry Age", fontsize=12)
    plt.xticks(fontsize=10)
    plt.yticks(fontsize=10)
    plt.show()
    return

def actor_retire_age_analysis(actor_longevity):
    # Max
    retire_age_counts=actor_longevity.groupby('Zodiac Sign')['max'].mean().reset_index()
    retire_age_counts = retire_age_counts.sort_values(by='max', ascending=False)
    plt.figure(figsize=(10, 4))
    ax=sns.barplot(x='Zodiac Sign', y='max', data=retire_age_counts, palette="pastel",hue='Zodiac Sign', legend=False)
    ax.set_ylim(39.4, 40.4)
    # 手动添加数值标签
    for p in ax.patches:
        height = p.get_height()  # 获取每个条形的高度
        ax.text(
            p.get_x() + p.get_width() / 2., height,  # 条形的中心位置
            f'{height:.3f}',  # 标签内容
            ha='center', va='bottom', fontsize=12, color='black'  # 字体和位置
        )

    plt.title("Average Retire Age of Zodiac Signs", fontsize=16)
    plt.xlabel("Zodiac Sign", fontsize=12)
    plt.ylabel("Average Retire Age", fontsize=12)
    plt.xticks(fontsize=10)
    plt.yticks(fontsize=10)
    plt.show()
    return



def ANOVA_Career(actor_roles, alpha=0.05, factors='Career Longevity'):
    index=factors
    if index == 'Entry Age':
        index='min'
    elif index == 'Retire Age':
        index='max'

    groups = [actor_roles[actor_roles['Zodiac Sign'] == zodiac][index] for zodiac in
              actor_roles['Zodiac Sign'].unique()]
    f_stat, p_value = stats.f_oneway(*groups)
    print(f"F-statistic: {f_stat}")
    print(f"P-value: {p_value}")

    if p_value < alpha:
        print(f"The difference in {factors} among zodiac signs is significant")
    else:
        print(f"The difference in {factors} among zodiac signs is not significant.")
    return


def KruskalWallis_Career(actor_roles, alpha=0.05,factors='Career Longevity'):
    index = factors
    if index == 'Entry Age':
        index = 'min'
    elif index == 'Retire Age':
        index = 'max'

    groups = [actor_roles[actor_roles['Zodiac Sign'] == zodiac][index] for zodiac in
              actor_roles['Zodiac Sign'].unique()]

    h_stat, p_value = stats.kruskal(*groups)

    print(f"H-statistic: {h_stat}")
    print(f"P-value: {p_value}")

    if p_value < alpha:
        print(f"The difference in {factors} among zodiac signs is significant")
    else:
        print(f"The difference in {factors} among zodiac signs is not significant.")
        return