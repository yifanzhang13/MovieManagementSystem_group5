import os

import pandas as pd
import numpy as np

DATA_PATH = "./data/ratings.csv"

dtype = {"userId": np.int32, "movieId": np.int32, "rating": np.float32}
# load data
ratings_df = pd.read_csv(DATA_PATH, dtype=dtype, usecols=range(3))
userId_list = ratings_df["userId"].values
movieId_list = ratings_df["movieId"].values
rating_list = ratings_df["rating"].values


user_info = {}
for i in range(len(userId_list)):
    if userId_list[i] not in user_info.keys():
        user_info[userId_list[i]] = [rating_list[i]]
    else:
        user_info[userId_list[i]].append(rating_list[i])

ratings_values = []
for k ,v in user_info.items():
    t = np.sum(v) / len(v)
    ratings_values.append(t)
    if t >= 3.0:
        user_info[k] = "positive"
    else :
        user_info[k] = "negative"

item = {"userID": user_info.keys(), "lable": user_info.values(), "ratings_ave":ratings_values}
label_df = pd.DataFrame(item)

print(label_df.head(20))
