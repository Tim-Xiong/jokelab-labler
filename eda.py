import pandas as pd
import numpy as np
from collections import Counter
from sklearn.feature_extraction.text import CountVectorizer
import matplotlib.pyplot as plt

# Load the CSV files
joke_df = pd.read_csv('csv_exports/joke.csv')
label_df = pd.read_csv('csv_exports/label.csv')
label_segment_df = pd.read_csv('csv_exports/label_segment.csv')
visitor_df = pd.read_csv('csv_exports/visitor.csv')

# Prepare a professional EDA report script

# Text Length Analysis for Jokes
def analyze_text_length(joke_df):
    """
    Analyzes the length of joke texts in a DataFrame and plots a histogram of the text lengths.
    Parameters:
    joke_df (pandas.DataFrame): DataFrame containing a column 'text' with joke texts.
    Returns:
    dict: A dictionary containing the average, minimum, and maximum lengths of the joke texts.
        - "average_length" (float): The average length of the joke texts.
        - "min_length" (int): The minimum length of the joke texts.
        - "max_length" (int): The maximum length of the joke texts.
    """
    joke_df['text_length'] = joke_df['text'].apply(len)
    stats = {
        "average_length": joke_df['text_length'].mean(),
        "min_length": joke_df['text_length'].min(),
        "max_length": joke_df['text_length'].max()
    }
    plt.hist(joke_df['text_length'], bins=20, edgecolor='black')
    plt.title('Distribution of Joke Lengths')
    plt.xlabel('Length of Joke Text')
    plt.ylabel('Frequency')
    plt.show()
    return stats

# Content Analysis for Jokes
def analyze_word_frequency(joke_df):
    """
    Analyzes the word frequency in a DataFrame containing jokes.
    This function takes a DataFrame with a column 'text' containing jokes,
    and computes the frequency of words in the jokes, excluding English stop words.
    It returns the 10 most common words and the 10 least common words.
    Parameters:
    joke_df (pandas.DataFrame): A DataFrame with a column 'text' containing jokes.
    Returns:
    tuple: A tuple containing two lists:
        - most_common_words (list): A list of tuples with the 10 most common words and their frequencies.
        - least_common_words (list): A list of tuples with the 10 least common words and their frequencies.
    """
    vectorizer = CountVectorizer(stop_words='english')
    word_counts = vectorizer.fit_transform(joke_df['text'])
    word_counts_sum = np.array(word_counts.sum(axis=0)).flatten()
    word_freq = dict(zip(vectorizer.get_feature_names_out(), word_counts_sum))
    most_common_words = Counter(word_freq).most_common(10)
    least_common_words = Counter(word_freq).most_common()[:-11:-1]
    return most_common_words, least_common_words

# Label Analysis
def analyze_labels(label_df):
    """
    Analyzes the labels in the given DataFrame and provides various statistics.
    Parameters:
    label_df (pd.DataFrame): A DataFrame containing labels with at least the following columns:
                             - 'joke_id': Identifier for each joke.
                             - 'no_punchline': Binary indicator if the joke has no punchline.
    Returns:
    dict: A dictionary containing the following keys and their corresponding values:
          - "total_labels": Total number of labels.
          - "average_labels_per_joke": Average number of labels per joke.
          - "most_labels_joke": A tuple containing the joke_id with the most labels and the number of labels.
          - "least_labels_joke": A tuple containing the joke_id with the least labels and the number of labels.
    """
    total_labels = label_df.shape[0]
    average_labels_per_joke = label_df.groupby('joke_id').size().mean()
    labels_per_joke = label_df.groupby('joke_id').size()
    most_labels_joke = labels_per_joke.idxmax()
    least_labels_joke = labels_per_joke.idxmin()
    no_punchline_counts = label_df['no_punchline'].value_counts()
    
    no_punchline_counts.plot(kind='bar')
    plt.title('Distribution of no_punchline Labels')
    plt.xlabel('no_punchline')
    plt.ylabel('Count')
    plt.show()

    return {
        "total_labels": total_labels,
        "average_labels_per_joke": average_labels_per_joke,
        "most_labels_joke": (most_labels_joke, labels_per_joke.max()),
        "least_labels_joke": (least_labels_joke, labels_per_joke.min())
    }

# Label Segment Analysis
def analyze_segments(label_segment_df):
    """
    Analyzes segments within a DataFrame containing labeled segments.
    This function calculates the length of each segment, plots a histogram of the segment lengths,
    computes the proportion of jokes with segments, and identifies overlaps and gaps between segments.
    Parameters:
    label_segment_df (pd.DataFrame): DataFrame containing labeled segments with columns 'label_id', 
                                     'start_index', and 'end_index'.
    Returns:
    dict: A dictionary with the following keys:
        - "proportion_with_segments" (float): The proportion of jokes that have segments.
        - "overlaps_gaps" (pd.DataFrame): DataFrame containing 'label_id', 'start_index', 'end_index', 
                                          and 'overlap_gap' which indicates the gap or overlap between 
                                          consecutive segments for each label.
    """
    label_segment_df['segment_length'] = label_segment_df['end_index'] - label_segment_df['start_index']
    plt.hist(label_segment_df['segment_length'], bins=20, edgecolor='black')
    plt.title('Distribution of Segment Lengths')
    plt.xlabel('Segment Length')
    plt.ylabel('Frequency')
    plt.show()

    jokes_with_segments = label_segment_df['label_id'].nunique()
    total_jokes = joke_df['id'].nunique()
    proportion_with_segments = jokes_with_segments / total_jokes

    overlaps_gaps = label_segment_df.groupby('label_id').apply(
        lambda x: x.sort_values('start_index').assign(
            overlap_gap=lambda df: df['start_index'].shift(-1) - df['end_index']
        )
    )

    return {
        "proportion_with_segments": proportion_with_segments,
        "overlaps_gaps": overlaps_gaps[['label_id', 'start_index', 'end_index', 'overlap_gap']]
    }

# Generate Report
def generate_eda_report(joke_df, label_df, label_segment_df):
    """
    Generates an exploratory data analysis (EDA) report for the given dataframes.
    Parameters:
    joke_df (pd.DataFrame): DataFrame containing jokes data.
    label_df (pd.DataFrame): DataFrame containing labels data.
    label_segment_df (pd.DataFrame): DataFrame containing label segments data.
    Returns:
    None: This function prints the analysis results to the console.
    The report includes:
    - Text Length Analysis: Statistics on the length of the text in jokes.
    - Word Frequency Analysis: Most and least common words in the jokes.
    - Label Analysis: Statistics on the labels.
    - Segment Analysis: Proportion of jokes with segments and details on overlaps or gaps in segments.
    """
    # Text Length Analysis
    text_length_stats = analyze_text_length(joke_df)
    print("Text Length Statistics:", text_length_stats)

    # Word Frequency Analysis
    most_common_words, least_common_words = analyze_word_frequency(joke_df)
    print("Most Common Words:", most_common_words)
    print("Least Common Words:", least_common_words)

    # Label Analysis
    label_stats = analyze_labels(label_df)
    print("Label Statistics:", label_stats)

    # Segment Analysis
    segment_stats = analyze_segments(label_segment_df)
    print("Segment Statistics:", segment_stats["proportion_with_segments"])
    print("Overlaps or Gaps in Segments:")
    print(segment_stats["overlaps_gaps"])

if __name__ == '__main__':
    generate_eda_report(joke_df, label_df, label_segment_df)
