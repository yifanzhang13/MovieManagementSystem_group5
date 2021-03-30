from .models import Movies, Users, Ratings, Links, Tags
import pandas as pd
import numpy as np

def predicting_personality_traits(userID, ratings_df, tags_df):
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

    # assume let test_userID=1, to predict he's personality traits
    test_userID = int(userID)
    print("assume let test_userID=%d, to predict he's personality traits..." % test_userID)

    # get user similar list base on test movie has been given.
    similar_user = user_similar[test_userID].drop([test_userID]).dropna()
    similar_user = similar_user.where(similar_user > 0).dropna()
    if similar_user.empty is True:
        raise Exception("no similar user base on <%d>" % test_userID)

    print("Sort by similarity...")
    similar_values = []
    for i in similar_user.index:
        similar_values.append(similar_user.loc[i])

    similar_user_data = {"userID": similar_user.index, "similar": similar_values}
    similar_user_df = pd.DataFrame(similar_user_data).sort_values(by="similar", ascending=False)

    # get the top 20 user's tag base on the similar rank
    def getTopKUserTag(similar_user_df):
        tags_list = set()
        userID_list = similar_user_df["userID"][:20]
        for user in userID_list:
            if list(tags_df.loc[tags_df["userId"] == user]["tag"].values) != []:
                tags = list(tags_df.loc[tags_df["userId"] == user]["tag"].values)[0]
                tags_list.add(tags)
        return set(tags_list)

    tags_list = list(getTopKUserTag(similar_user_df))[:5]

    print("the user personality traits are %s" % tags_list)
    return str(tags_list)
