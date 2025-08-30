import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import linear_kernel


df = pd.read_csv("steam.csv").fillna('')
df['content'] = df[['name','developer','publisher','release_date']].agg(' '.join, axis=1)

matrix = TfidfVectorizer(stop_words='english', max_features=5000).fit_transform(df['content'])
sim = linear_kernel(matrix, matrix)
indices = pd.Series(df.index, index=df['name']).drop_duplicates()


def recommend(name, top_n=10):
    if name not in indices: return ["Game not found"]
    idx = indices[name]
    scores = sorted(list(enumerate(sim[idx])), key=lambda x: x[1], reverse=True)[1:top_n+1]
    return df['name'].iloc[[i[0] for i in scores]].tolist()


if __name__ == "__main__":
    recommendations = recommend("Counter-Strike", 10)
    print("\n".join(recommendations))
