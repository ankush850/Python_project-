import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import linear_kernel


def load_data(path):
    df = pd.read_csv(path)
    df['developer'] = df['developer'].fillna('')
    df['publisher'] = df['publisher'].fillna('')
    df['release_date'] = df['release_date'].fillna('')
    df['content'] = (
        df['name'].astype(str) + " " +
        df['developer'] + " " +
        df['publisher'] + " " +
        df['release_date']
    )
    return df


def build_tfidf_matrix(df, max_features=5000):
    vectorizer = TfidfVectorizer(stop_words='english', max_features=max_features)
    tfidf_matrix = vectorizer.fit_transform(df['content'])
    return tfidf_matrix


def compute_similarity(matrix):
    return linear_kernel(matrix, matrix)


def build_indices(df):
    return pd.Series(df.index, index=df['name']).drop_duplicates()


def recommend(name, cosine_sim, indices, df, top_n=10):
    if name not in indices:
        return ["Game not found in dataset"]
    idx = indices[name]
    sim_scores = list(enumerate(cosine_sim[idx]))
    sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)
    sim_scores = sim_scores[1:top_n+1]
    game_indices = [i[0] for i in sim_scores]
    return df['name'].iloc[game_indices].tolist()


if __name__ == "__main__":
    data = load_data("steam.csv")
    tfidf_matrix = build_tfidf_matrix(data)
    cosine_sim = compute_similarity(tfidf_matrix)
    indices = build_indices(data)
    results = recommend("Counter-Strike", cosine_sim, indices, data, top_n=10)
    for r in results:
        print(r)
