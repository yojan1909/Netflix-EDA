import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import plotly.express as px

# Load dataset
df = pd.read_csv("netflix_titles.csv")

# Preview data
print(df.head())
print(df.info())

# --- Handling Missing Values ---
df.fillna({'country': 'Unknown', 'director': 'Unknown', 'cast': 'Unknown'}, inplace=True)

# Convert 'date_added' to datetime safely
df['date_added'] = pd.to_datetime(df['date_added'], errors='coerce')
df['year_added'] = df['date_added'].dt.year
df['month_added'] = df['date_added'].dt.month

# --- Genre Count ---
df['genre'] = df['listed_in'].str.split(', ')
genre_explode = df.explode('genre')
genre_count = genre_explode['genre'].value_counts().reset_index()
genre_count.columns = ['Genre', 'Count']

plt.figure(figsize=(10, 6))
sns.barplot(data=genre_count.head(10), x='Count', y='Genre', palette='Blues_d')
plt.title('Top 10 Genres on Netflix')
plt.tight_layout()
plt.show()

# --- Year-wise Trend of Content Added ---
yearly = df['release_year'].value_counts().sort_index()

plt.figure(figsize=(12, 5))
sns.lineplot(x=yearly.index, y=yearly.values)
plt.title("Trend of Netflix Content Releases Over Years")
plt.xlabel("Release Year")
plt.ylabel("Number of Titles")
plt.grid(True)
plt.tight_layout()
plt.show()

# --- Country-wise Distribution ---
top_countries = df['country'].value_counts().head(10).reset_index()
top_countries.columns = ['Country', 'Count']

fig = px.bar(top_countries, x='Country', y='Count', title='Top 10 Countries with Most Netflix Titles')
fig.show()

# --- Duration Analysis ---
# Split TV Shows and Movies
tv_shows = df[df['type'] == 'TV Show'].copy()
movies = df[df['type'] == 'Movie'].copy()

# Clean and convert movie durations
movies['duration'] = movies['duration'].str.replace(' min', '', regex=False)
movies['duration'] = pd.to_numeric(movies['duration'], errors='coerce')

plt.figure(figsize=(10, 4))
sns.histplot(movies['duration'].dropna(), bins=30, kde=True)
plt.title('Movie Duration Distribution')
plt.xlabel('Duration (minutes)')
plt.tight_layout()
plt.show()

# Clean and convert TV show durations
tv_shows['duration'] = tv_shows['duration'].str.replace(' Season', '', regex=False)
tv_shows['duration'] = tv_shows['duration'].str.replace('s', '', regex=False)
tv_shows['duration'] = pd.to_numeric(tv_shows['duration'], errors='coerce')

plt.figure(figsize=(10, 4))
sns.countplot(data=tv_shows, x='duration', order=tv_shows['duration'].value_counts().index[:10])
plt.title('TV Show Season Count Distribution')
plt.xlabel('Number of Seasons')
plt.tight_layout()
plt.show()

df.to_csv("netflix_cleaned.csv", index=False)
