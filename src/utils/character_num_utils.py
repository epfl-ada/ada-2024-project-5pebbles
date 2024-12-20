import scipy.stats as stats
import pandas as pd
import matplotlib.pyplot as plt
# Count the number of roles per actor
import seaborn as sns
def RolesNumberDistribution(character_data):
    # Count the number of roles per actor
    role_num=character_data.groupby('Freebase actor ID').size().reset_index(name='RoleCount')
    actor_roles = role_num.merge(character_data[['Freebase actor ID', 'Zodiac Sign']].drop_duplicates(), on='Freebase actor ID')
    result = actor_roles.groupby('Zodiac Sign')['RoleCount'].mean().reset_index()
    result=result.sort_values(by="RoleCount", ascending=False)
    plt.figure(figsize=(10, 6))
    ax=sns.barplot(x='Zodiac Sign', y='RoleCount', data=result, palette="pastel",hue='Zodiac Sign', legend=False)
    ax.set_ylim(4.5,5.6)
    # 手动添加数值标签
    for p in ax.patches:
        height = p.get_height()  # 获取每个条形的高度
        ax.text(
            p.get_x() + p.get_width() / 2., height,  # 条形的中心位置
            f'{height:.3f}',  # 标签内容
            ha='center', va='bottom', fontsize=12, color='black'  # 字体和位置
        )

    plt.title("Average Number of Roles per Zodiac Sign", fontsize=16)
    plt.xlabel("Zodiac Sign", fontsize=12)
    plt.ylabel("Average Role Count", fontsize=12)
    plt.xticks(fontsize=10)
    plt.yticks(fontsize=10)
    plt.show()
    return

def ANOVA_Role_Num(actor, alpha=0.05):
    groups = [actor[actor['Zodiac Sign'] == zodiac]['RoleCount'] for zodiac in
              actor['Zodiac Sign'].unique()]
    f_stat, p_value = stats.f_oneway(*groups)
    print(f"F-statistic: {f_stat}")
    print(f"P-value: {p_value}")

    if p_value < alpha:
        print("The difference in role counts among zodiac signs is significant")
    else:
        print("The difference in role counts among zodiac signs is not significant.")