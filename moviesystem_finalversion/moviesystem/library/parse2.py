import os

import pandas as pd
import numpy as np

DATA_PATH = "./data/ratings.csv"
MOVIE_PATH = "./data/movies.csv"
# load data
print("loading data...")
dtype = {"userId": np.int32, "movieId": np.int32, "rating": np.float32}
ratings_df = pd.read_csv(DATA_PATH, dtype=dtype, usecols=range(3))
# movies_df = pd.read_csv(MOVIE_PATH)

print(ratings_df.head())
# convert the User-Movie matrix
print("to convert the User-Movie matrix...")
ratings_matrix = ratings_df.pivot_table(index=["userId"], columns=["movieId"], values="rating")
# print(ratings_matrix)
# compute User-User similary matrix
print("compute User-User similary matrix...")
user_similar = ratings_matrix.T.corr()
# print(user_similar)

# compute Movie-Movie similary matrix
print("compute Movie-Movie similary matrix...")
movie_similar = ratings_matrix.corr()
# print(movie_similar)

# assume let userID=1 to watch movie list as movieID=[5, 22, 15, 79, 55]
test_userID = 1
test_movieID_list = [5, 22, 15, 11, 18]
print("test user and pre to watch movie list has been set...")

# function: convert movieName to movieID
def movieToID(movies_df, name):
    id = list(movies_df.loc[movies_df["title"] == name]["movieId"].values)[0]
    return id

# get movie similar list base on test movie has been given.
final_result = []
for movie in test_movieID_list:
    print("current preccess movieID is %d" % movie)
    similar_movie = movie_similar[movie].drop([movie]).dropna()
    similar_movie = similar_movie.where(similar_movie>0).dropna()
    if similar_movie.empty is True:
        raise Exception("no similar movie base on <%d>" % movie)

    # match the test userID' info
    print("match the test userID' info...")
    ids = set(ratings_matrix.loc[test_userID].dropna().index)&set(similar_movie.index)
    similar_movie = similar_movie.loc[list(ids)]

    # Sort by similarity, from high to low
    # print(type(similar_movie))
    # print(similar_movie.index)
    # print(similar_movie.loc[list(similar_movie.index)[0]])

    print("Sort by similarity...")
    similar_values = []
    for i in similar_movie.index:
        similar_values.append(similar_movie.loc[i])

    similar_movie_data = {"movieID":similar_movie.index,"similar":similar_values}
    similar_movie_df = pd.DataFrame(similar_movie_data).sort_values(by="similar",ascending=False)
    print(similar_movie_df.head())


    # Collect statistics on the top 10 movies with the highest similarity to obtain the average score.
    def getMeanRating(movie_id):
        rating = list(ratings_df.loc[ratings_df["movieId"] == movie_id]["rating"].values)
        rating_ave = np.mean(rating)
        return rating_ave

    def getTopKMovie(similar_movie_df):
        return similar_movie_df[:20]

    similar_movie_df = getTopKMovie(similar_movie_df)

    print("Collect statistics on the top 10 movies with the highest similarity to obtain the average score...")
    top_similar_movie_av_list = []
    for id in list(similar_movie_df["movieID"]):
        top_similar_movie_av_list.append(getMeanRating(id))

    top_similar_movie_avg = np.mean(top_similar_movie_av_list)
    final_result.append(top_similar_movie_avg)
print("predict ratings on new movie is : %d" % np.mean(final_result))
