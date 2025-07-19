import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# Title
st.title(" Netflix Titles EDA Dashboard (Matplotlib Version)")

# Load dataset
@st.cache_data
def load_data():
    df = pd.read_csv("netflix_cleaned.csv")
    df.fillna({'country': 'Unknown', 'director': 'Unknown', 'cast': 'Unknown'}, inplace=True)
    df['date_added'] = pd.to_datetime(df['date_added'], errors='coerce')
    df['year_added'] = df['date_added'].dt.year
    df['month_added'] = df['date_added'].dt.month
    df['genre'] = df['listed_in'].str.split(', ')
    return df

df = load_data()

# Sidebar Filter
st.sidebar.header(" Filter")
selected_type = st.sidebar.selectbox("Select Content Type", ["All", "Movie", "TV Show"])
filtered_df = df if selected_type == "All" else df[df['type'] == selected_type]

# Top 10 Genres
st.subheader(" Top 10 Genres")
genre_explode = filtered_df.explode('genre')
genre_count = genre_explode['genre'].value_counts().head(10)

fig1, ax1 = plt.subplots()
genre_count.sort_values().plot(kind='barh', ax=ax1, color='skyblue')
ax1.set_xlabel("Count")
ax1.set_ylabel("Genre")
ax1.set_title("Top 10 Genres")
st.pyplot(fig1)

# Yearly Trend
st.subheader("Yearly Trend of Content Release")
yearly = filtered_df['release_year'].value_counts().sort_index()

fig2, ax2 = plt.subplots()
ax2.plot(yearly.index, yearly.values, marker='o', linestyle='-')
ax2.set_xlabel("Release Year")
ax2.set_ylabel("Number of Titles")
ax2.set_title("Year-wise Release Trend")
st.pyplot(fig2)

# Country-wise Content
st.subheader(" Top 10 Countries")
top_countries = filtered_df['country'].value_counts().head(10)

fig3, ax3 = plt.subplots()
top_countries.plot(kind='bar', ax=ax3, color='orange')
ax3.set_xlabel("Country")
ax3.set_ylabel("Count")
ax3.set_title("Top Countries by Content")
ax3.set_xticklabels(top_countries.index, rotation=45)
st.pyplot(fig3)

# Duration Analysis
st.subheader("Duration Analysis")
if selected_type == "Movie":
    filtered_df['duration_min'] = filtered_df['duration'].str.extract('(\d+)').astype(float)
    fig4, ax4 = plt.subplots()
    ax4.hist(filtered_df['duration_min'].dropna(), bins=30, color='green', edgecolor='black')
    ax4.set_xlabel("Duration (minutes)")
    ax4.set_ylabel("Count")
    ax4.set_title("Movie Duration Distribution")
    st.pyplot(fig4)

elif selected_type == "TV Show":
    filtered_df['num_seasons'] = filtered_df['duration'].str.extract('(\d+)').astype(float)
    fig5, ax5 = plt.subplots()
    ax5.hist(filtered_df['num_seasons'].dropna(), bins=10, color='purple', edgecolor='black')
    ax5.set_xlabel("Number of Seasons")
    ax5.set_ylabel("Count")
    ax5.set_title("TV Show Season Distribution")
    st.pyplot(fig5)

else:
    st.markdown("_Select Movie or TV Show to see duration distribution._")
