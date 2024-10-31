import streamlit as st

import preprocessor, helper
import matplotlib.pyplot as plt
import seaborn as sns

st.sidebar.title("Whatsapp Chat Analyzer")

uploaded_file = st.sidebar.file_uploader("Choose a file")
if uploaded_file is not None:
    bytes_data = uploaded_file.getvalue()
    data = bytes_data.decode("utf-8")
    df = preprocessor.preprocess(data)

    st.dataframe(df)

    #fetch unique user
    user_list = df["user"].unique().tolist()
    user_list.remove("group_notification")
    user_list.sort()
    user_list.insert(0, "Overall")
    selected_user = st.sidebar.selectbox("Show analysis wrt", user_list)

    if st.sidebar.button("Show analysis"):
        #stat area
        num_messages, words, num_media_message,num_links = helper.fetch_stats(selected_user, df)

        col1, col2, col3, col4 = st.columns(4)

        with col1:
            st.header("Total Messages")
            st.title(num_messages)
        with col2:
            st.header("Total Words")
            st.title(words)
        with col3:
            st.header("Total media")
            st.title(num_media_message)

        with col4:
            st.header("Total Links")
            st.title(num_links)

        #monthly timeline
        st.title("Monthly Timeline")
        timeline = helper.monthly_timeline(selected_user,df)
        fig,ax = plt.subplots()
        ax.plot(timeline['time'],timeline['message'],color='green')
        plt.xticks(rotation='vertical')
        st.pyplot(fig)

        #daily timeline
        st.title("Daily Timeline")
        daily_timeline = helper.daily_timeline(selected_user, df)
        fig, ax = plt.subplots()
        ax.plot(daily_timeline['only_date'], daily_timeline['message'], color='black')
        plt.xticks(rotation='vertical')
        st.pyplot(fig)

        #Activity map
        st.title("Activity Map")
        col1,col2 = st.columns(2)


        with col1:
            st.header("Most Busy Day")
            busy_day = helper.week_activity_map(selected_user, df)
            fig, ax = plt.subplots()
            ax.plot(busy_day.index, busy_day.values, color='red')
            plt.xticks(rotation='vertical')
            st.pyplot(fig)

        with col2:
            st.header("Most Busy month")
            busy_month = helper.month_activity_map(selected_user, df)
            fig, ax = plt.subplots()
            ax.plot(busy_month.index, busy_month.values, color='blue')
            plt.xticks(rotation='vertical')
            st.pyplot(fig)

        #heatmap

        st.title("Weekly Activity Map")
        user_heatmap = helper.activity_heatmap(selected_user, df)
        fig, ax = plt.subplots()
        ax = sns.heatmap(user_heatmap)
        st.pyplot(fig)










        #finding the busiest user in group(group level)
        if selected_user == "Overall":
            st.title("Most Active User")
            x,new_df = helper.most_busy_users(df)
            fig,ax = plt.subplots()


            col1,col2 = st.columns(2)
            with col1:
                ax.plot(x.index, x.values,color='skyblue')
                plt.xticks(rotation='vertical')
                st.pyplot(fig)
            with col2:
                st.dataframe(new_df)





        #most common word
        st.header("Most Common Words")
        most_common_df = helper.most_common_word(selected_user, df)



        st.dataframe(most_common_df)



        #emoji analysis
        st.header("Emoji Analysis")

        # Get the emoji analysis DataFrame
        emoji_df = helper.emoji_helper(selected_user, df)

        # Create two columns for layout
        col1, col2 = st.columns(2)

        with col1:
            st.dataframe(emoji_df)  # Display the emoji frequency DataFrame

        with col2:
            # Create a pie chart for the most common emojis
            fig, ax = plt.subplots()
            ax.pie(
                emoji_df['count'],  # Pie values from 'count' column
                labels=emoji_df['emoji'],  # Labels from 'emoji' column
                autopct='%1.1f%%',  # Show percentage on the chart
                startangle=90  # Start angle for better display
            )
            ax.axis('equal')  # Ensure pie chart is a circle
            st.pyplot(fig)  # Display the chart





