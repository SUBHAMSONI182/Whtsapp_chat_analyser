
from urlextract import URLExtract
from wordcloud import WordCloud
import pandas as pd
from collections import Counter
import emoji

extract = URLExtract()


def fetch_stats(selected_user, df):
    if selected_user == 'Overall':
        # 1. Fetch total number of messages
        num_messages = df.shape[0]

        # 2. Count the total number of words
        words = []
        for message in df["message"]:
            words.extend(message.split())
        #3.number od media shared
        num_media_messages = df[df['message']=='<Media omitted>\n'].shape[0]
        #4.extract link
        links = []
        for message in df["message"]:
            links.extend(extract.find_urls(message))




        return num_messages, len(words),num_media_messages,len(links)
    else:
        # Filter the DataFrame for the selected user
        new_df = df[df['user'] == selected_user]

        # 1. Fetch the number of messages for the user
        num_messages = new_df.shape[0]

        # 2. Count the words in the user's messages
        words = []
        for message in new_df["message"]:
            words.extend(message.split())

    return num_messages, len(words)



def most_busy_users(df):
    x = df['user'].value_counts().head()
    df = round((df['user'].value_counts()/df.shape[0])*100,2).reset_index().rename(columns={'user':'name','count':'percent'})
    return x,df




def most_common_word(selected_user, df):
    # Read the stop words
    with open('hinglish.txt', 'r', encoding='utf-8') as f:
        stop_words = f.read().splitlines()  # Store stop words as a list

    # Filter the DataFrame based on the selected user
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    # Remove unwanted messages
    temp = df[df["user"] != 'group_notification']
    temp = temp[temp['message'] != '<Media omitted>\n']

    words = []
    # Extract and filter words
    for message in temp['message'].dropna():
        for word in message.lower().split():
            if word not in stop_words:
                words.append(word)

    # Create a DataFrame with the 20 most common words
    most_common_df = pd.DataFrame(Counter(words).most_common(20),
                                  columns=['Word', 'Count'])
    return most_common_df



def emoji_helper(selected_user, df):
    # Filter by user if a specific user is selected
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    emojis = []
    for message in df["message"].dropna():
        # Use is_emoji to detect emojis (for the latest emoji library)
        emojis.extend([c for c in message if emoji.is_emoji(c)])

    # Create DataFrame of most common emojis
    emoji_df = pd.DataFrame(Counter(emojis).most_common(), columns=['emoji', 'count'])
    return emoji_df


def monthly_timeline(selected_user,df):
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]
    timeline = df.groupby(['year', 'month_num', 'month']).count()['message'].reset_index()

    time = []
    for i in range(timeline.shape[0]):
        time.append(timeline['month'][i] + '-' + str(timeline['year'][i]))

    timeline["time"] = time



    return timeline


def daily_timeline(selected_user,df):
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    daily_timeline = df.groupby("only_date").count()['message'].reset_index()
    return daily_timeline


def week_activity_map(selected_user,df):
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    return df['day_name'].value_counts()


def month_activity_map(selected_user,df):
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    return df['month'].value_counts()

def activity_heatmap(selected_user,df):

    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    user_heatmap = df.pivot_table(index='day_name', columns='period', values='message', aggfunc='count').fillna(0)

    return user_heatmap