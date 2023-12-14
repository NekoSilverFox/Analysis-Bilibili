import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

if __name__ == "__main__":
    """ 
    根据情感倾向生成不同类型的图表，包括直方图、箱型图、条状图、饼图和主导情绪的条状图。
    最后一部分将描述性统计信息保存到了emotion_report.csv文件，以便进一步分析。
    """
    # 必要时设置Seaborn样式
    sns.set()

    # 读取CSV文件
    df = pd.read_csv('concatenated.csv', header=None)
    # 为列命名
    df.columns = ['Angry', 'Disgust', 'Happy', 'Love', 'Sad']

    # 绘制所有情绪倾向的直方图并保存
    plt.figure(figsize=(10, 6))
    sns.histplot(df, bins=50, kde=True)
    plt.title('Probability Distribution of Emotions')
    plt.xlabel('Probability')
    plt.ylabel('Frequency')
    plt.savefig('histogram_of_emotions.png')  # 保存直方图
    plt.clf()  # 清除当前图形

    # 绘制所有情绪倾向的箱型图并保存
    plt.figure(figsize=(10, 6))
    sns.boxplot(data=df)
    plt.title('Boxplot Distribution of Emotions')
    plt.xlabel('Emotion Type')
    plt.ylabel('Probability')
    plt.savefig('boxplot_of_emotions.png')  # 保存箱型图
    plt.clf()  # 清除当前图形

    # 计算每种情绪的平均倾向，并绘制条状图
    emotion_means = df.mean().sort_values()
    plt.figure(figsize=(10, 6))
    sns.barplot(x=emotion_means.index, y=emotion_means.values)
    plt.title('Average Probability of Emotions')
    plt.xlabel('Emotion Type')
    plt.ylabel('Average Probability')
    plt.savefig('barplot_of_average_emotions.png')  # 保存条状图
    plt.clf()  # 清除当前图形

    # 计算每种情绪倾向的总和百分比，并绘制饼状图
    emotion_sums = df.sum()
    plt.figure(figsize=(8, 8))
    emotion_sums.plot(kind='pie', autopct='%1.1f%%')
    plt.title('Percentage of Emotional Tendencies')
    # 饼图通常不需要y轴标签
    plt.ylabel('')
    plt.savefig('pie_chart_of_emotions.png')  # 保存饼状图
    plt.clf()  # 清除当前图形

    # 提供一个主导情绪倾向的概览
    df['Dominant Emotion'] = df.idxmax(axis=1)
    dominant_emotion_counts = df['Dominant Emotion'].value_counts()
    plt.figure(figsize=(10, 6))
    sns.barplot(x=dominant_emotion_counts.index, y=dominant_emotion_counts.values)
    plt.title('Dominant Emotion Count')
    plt.xlabel('Emotion Type')
    plt.ylabel('Count')
    plt.savefig('barplot_of_dominant_emotions.png')  # 保存主导情绪条状图
    plt.clf()  # 清除当前图形