import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns
import scipy.stats as stats


def oscar_zodiac_distribution(zodiac_counts):
    # zodiac_counts = CharacterMeta_cleaned['Zodiac Sign'].value_counts(dropna=False).reset_index()
    # zodiac_counts.columns = ['Zodiac Sign', 'Count']
    # zodiac_counts = zodiac_counts.sort_values(by="Count", ascending=False)
    plt.figure(figsize=(10, 6))

    # Create a bar plot with a color map
    ax=sns.barplot(x='Count', y='Zodiac Sign', data=zodiac_counts, palette='coolwarm_r', hue='Zodiac Sign', legend=False)
    for p in ax.patches:
        width = p.get_width()  # 获取条形的宽度
        ax.text(
            width + 1,  # 数值放置在条形右侧
            p.get_y() + p.get_height() / 2.,  # 条形的中心高度
            f'{width:.4f}',  # 显示的数值
            ha='left', va='center', fontsize=12, color='black'  # 字体样式
        )

    # Add labels and title
    plt.title('Number of Oscars Won by Zodiac Sign', fontsize=16)
    plt.xlabel('Count of Times', fontsize=12)
    plt.ylabel('Zodiac Sign', fontsize=12)

    plt.tight_layout()
    plt.show()

def oscar_actor_zodiac_distribution(zodiac_counts):
    # zodiac_counts = CharacterMeta_cleaned['Zodiac Sign'].value_counts(dropna=False).reset_index()
    # zodiac_counts.columns = ['Zodiac Sign', 'Count']
    # zodiac_counts = zodiac_counts.sort_values(by="Count", ascending=False)
    plt.figure(figsize=(10, 6))

    # Create a bar plot with a color map
    sns.barplot(x='Count', y='Zodiac Sign', data=zodiac_counts, palette='coolwarm_r', hue='Zodiac Sign', legend=False)

    # Add labels and title
    plt.title('The zodiac distribution of actors who have won an Oscar', fontsize=16)
    plt.xlabel('Count of Actors', fontsize=12)
    plt.ylabel('Zodiac Sign', fontsize=12)

    plt.tight_layout()
    plt.show()

def GenderOscarAnalysis(data):
    zodiac_gender_counts = data.groupby(['Zodiac Sign', 'award']).size().reset_index(name='count')

    # use seaborn to create bar plot
    plt.figure(figsize=(10, 6))
    sns.barplot(x='Zodiac Sign', y='count', hue='award', data=zodiac_gender_counts)

    # add title and lable
    plt.title('Zodiac Sign Distribution by Gender')

    plt.xlabel('Zodiac Sign')
    plt.ylabel('Number of Times')
    plt.xticks(rotation=45)
    plt.tight_layout()

    # show the graph
    plt.show()

    return

def GenderOscarActAnalysis(data):
    zodiac_gender_counts = data.groupby(['Zodiac Sign', 'award']).size().reset_index(name='count')

    # use seaborn to create bar plot
    plt.figure(figsize=(10, 6))
    sns.barplot(x='Zodiac Sign', y='count', hue='award', data=zodiac_gender_counts)

    # add title and lable
    plt.title('Zodiac Sign Distribution by Gender')

    plt.xlabel('Zodiac Sign')
    plt.ylabel('Number of Actors')
    plt.xticks(rotation=45)
    plt.tight_layout()

    # show the graph
    plt.show()

    return

def OscarAwardRate(actor,oscar):
    actor_count=actor['Zodiac Sign'].value_counts().reset_index()
    actor_count.columns = ['Zodiac Sign', 'Actor Count']
    oscar_count=oscar['Zodiac Sign'].value_counts().reset_index()
    oscar_count.columns = ['Zodiac Sign', 'Oscar Count']
    oscar_count_data=oscar_count.merge(actor_count,on='Zodiac Sign')
    oscar_count_data['rate']=oscar_count_data['Oscar Count']/oscar_count_data['Actor Count']
    oscar_count_data=oscar_count_data.sort_values(by='rate',ascending=False)
    plt.figure(figsize=(10, 6))

    # Create a bar plot with a color map
    sns.barplot(x='rate', y='Zodiac Sign', data=oscar_count_data, palette='coolwarm_r', hue='Zodiac Sign', legend=False)

    # Add labels and title
    plt.title('Oscar Awarding Rate for Each Zodaic Signs', fontsize=16)
    plt.xlabel('Oscar Awarding Rate', fontsize=12)
    plt.ylabel('Zodiac Sign', fontsize=12)

    plt.tight_layout()
    plt.show()

    # Z-score Test
    oscar_count_data['Expected Winner']=oscar_count_data['Actor Count']/oscar_count_data['Actor Count'].sum()*oscar_count_data['Oscar Count'].sum()
    oscar_count_data['Expected std']=np.sqrt(oscar_count_data['Expected Winner']*(1-oscar_count_data['Expected Winner']/oscar_count_data['Actor Count']))

    #
    # Calculate z-scores and p-values
    oscar_count_data['Z-Score'] = (oscar_count_data['Oscar Count'] - oscar_count_data['Expected Winner']) / oscar_count_data['Expected std']
    oscar_count_data['P-Value'] = 2 * (1 - stats.norm.cdf(abs(oscar_count_data['Z-Score'])))
    #
    # Check significance level = 0.05
    oscar_count_data['Significant?'] = oscar_count_data['P-Value'] < 0.05
    #
    print(oscar_count_data[['Zodiac Sign', 'rate', 'Z-Score', 'P-Value', 'Significant?']])

    #
    chi2, p, dof, expected = stats.chi2_contingency(
        [oscar_count_data['Oscar Count'], oscar_count_data['Expected Winner']]
    )

    print("Chi-Square Statistic:", chi2)
    print("p-value:", p)
    print("Degrees of Freedom:", dof)
    print("Expected Winners:\n", expected)