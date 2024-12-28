import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os
from collections import Counter
import nltk
from nltk.corpus import stopwords

file_path = 'train_data_1.parquet'
df = pd.read_parquet(file_path)

output_dir = "diagrams"
os.makedirs(output_dir, exist_ok=True)

print(df.info())

if 'text' not in df.columns or df['text'].isnull().all():
    print("Error: 'text' column is missing or empty.")
else:
    df['word_count'] = df['text'].apply(lambda x: len(str(x).split()))
    plt.figure(figsize=(8, 4))
    sns.histplot(df['word_count'], bins=20, kde=True, color='blue')
    plt.title('Word Count Distribution')
    plt.xlabel('Word Count')
    plt.ylabel('Frequency')
    plt.savefig(f'{output_dir}/word_count_distribution.png')
    plt.show()

    df['char_count'] = df['text'].apply(lambda x: len(str(x)))
    plt.figure(figsize=(8, 4))
    sns.histplot(df['char_count'], bins=20, kde=True, color='green')
    plt.title('Character Count Distribution')
    plt.xlabel('Character Count')
    plt.ylabel('Frequency')
    plt.savefig(f'{output_dir}/char_count_distribution.png')
    plt.show()

    nltk.download('stopwords')
    stop_words = set(stopwords.words('english'))

    all_words = ' '.join(df['text'].dropna().astype(str)).split()
    filtered_words = [word for word in all_words if word.lower() not in stop_words]
    word_counts = Counter(filtered_words)
    top_words = word_counts.most_common(20)

    if top_words:
        top_words_df = pd.DataFrame(top_words, columns=['Word', 'Frequency'])
        plt.figure(figsize=(8, 6))
        sns.barplot(x='Frequency', y='Word', data=top_words_df, palette='viridis')
        plt.title('Top 20 Words')
        plt.xlabel('Frequency')
        plt.ylabel('Word')
        plt.savefig(f'{output_dir}/top_words.png')
        plt.show()
    else:
        print("No words found to plot.")

    if 'Story' in df.columns:
        plt.figure(figsize=(8, 4))
        df['Story'].value_counts().plot(kind='bar', color='orange', alpha=0.7)
        plt.title('Value Counts of Story Column')
        plt.ylabel('Count')
        plt.xlabel('Story')
        plt.savefig(f'{output_dir}/story_value_counts.png')
        plt.show()
    else:
        print("Error: 'Story' column is missing.")

