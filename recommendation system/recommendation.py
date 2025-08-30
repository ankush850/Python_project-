import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import linear_kernel

# Load dataset
df = pd.read_csv("steam.csv")

# --- Step 1: Preprocess ---
# Create a text field combining useful metadata
df['content'] = (
    df['developer'].fillna('') + " " +
    df['publisher'].fillna('') + " " +
    df['release_date'].fillna('')
)

# --- Step 2: Vectorize ---
vectorizer = TfidfVectorizer(stop_words='english', max_features=5000)
tfidf_matrix = vectorizer.fit_transform(df['content'])

# --- Step 3: Compute similarity ---
cosine_sim = linear_kernel(tfidf_matrix, tfidf_matrix)

# --- Step 4: Recommendation function ---
indices = pd.Series(df.index, index=df['name']).drop_duplicates()

def recommend(game_name, top_n=5):
    if game_name not in indices:
        return f"⚠️ Game '{game_name}' not found in dataset."

    idx = indices[game_name]
    sim_scores = list(enumerate(cosine_sim[idx]))
    sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)
    sim_scores = sim_scores[1:top_n+1]  # exclude the game itself

    game_indices = [i[0] for i in sim_scores]
    recommendations = df['name'].iloc[game_indices].tolist()

    # Format the output
    result = f"\n🎮 Recommended games similar to **{game_name}**:\n"
    for i, rec in enumerate(recommendations, start=1):
        result += f"{i}. {rec}\n"

    return result

# --- Example usage ---
print(recommend("Counter-Strike", top_n=10))
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import linear_kernel

# =====================
# GAME RECOMMENDER
# =====================
# Load game dataset
games_df = pd.read_csv("steam.csv")

# Preprocess games
games_df['content'] = (
    games_df['developer'].fillna('') + " " +
    games_df['publisher'].fillna('') + " " +
    games_df['release_date'].fillna('')
)

# Vectorize games
games_vectorizer = TfidfVectorizer(stop_words='english', max_features=5000)
games_tfidf_matrix = games_vectorizer.fit_transform(games_df['content'])

# Similarity for games
games_cosine_sim = linear_kernel(games_tfidf_matrix, games_tfidf_matrix)
games_indices = pd.Series(games_df.index, index=games_df['name']).drop_duplicates()

def recommend_game(game_name, top_n=5):
    if game_name not in games_indices:
        return f"⚠️ Game '{game_name}' not found in dataset."

    idx = games_indices[game_name]
    sim_scores = list(enumerate(games_cosine_sim[idx]))
    sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)
    sim_scores = sim_scores[1:top_n+1]

    game_indices = [i[0] for i in sim_scores]
    recommendations = games_df['name'].iloc[game_indices].tolist()

    result = f"\n🎮 Recommended games similar to **{game_name}**:\n"
    for i, rec in enumerate(recommendations, start=1):
        result += f"{i}. {rec}\n"
    return result

# =====================
# MOVIE RECOMMENDER
# =====================
# Load movie dataset
movies_df = pd.read_csv("netflix_titles.csv")

# Preprocess movies
movies_df['content'] = (
    movies_df['director'].fillna('') + " " +
    movies_df['cast'].fillna('') + " " +
    movies_df['listed_in'].fillna('') + " " +
    movies_df['description'].fillna('')
)

# Vectorize movies
movies_vectorizer = TfidfVectorizer(stop_words='english', max_features=5000)
movies_tfidf_matrix = movies_vectorizer.fit_transform(movies_df['content'])

# Similarity for movies
movies_cosine_sim = linear_kernel(movies_tfidf_matrix, movies_tfidf_matrix)
movies_indices = pd.Series(movies_df.index, index=movies_df['title']).drop_duplicates()

def recommend_movie(movie_title, top_n=5):
    if movie_title not in movies_indices:
        return f"⚠️ Movie '{movie_title}' not found in dataset."

    idx = movies_indices[movie_title]
    sim_scores = list(enumerate(movies_cosine_sim[idx]))
    sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)
    sim_scores = sim_scores[1:top_n+1]

    movie_indices = [i[0] for i in sim_scores]
    recommendations = movies_df['title'].iloc[movie_indices].tolist()

    result = f"\n🎬 Recommended movies similar to **{movie_title}**:\n"
    for i, rec in enumerate(recommendations, start=1):
        result += f"{i}. {rec}\n"
    return result

# =====================
# EXAMPLE USAGE
# =====================
print(recommend_game("Counter-Strike", top_n=10))
print(recommend_movie("Inception", top_n=10))
