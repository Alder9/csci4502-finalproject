import numpy as np
import pandas as pd
from matplotlib import pyplot as plt
from sklearn.naive_bayes import GaussianNB, BernoulliNB, MultinomialNB


# Import first two csvs as training set

path = r'F:/Datasets/pubg-match-deaths/aggregate/'

# Training data will be agg_match_stats_0 to 2
# Testing data will be agg_match_stats_3 and 4
training_paths = [path + r'agg_match_stats_' + str(i) + '.csv' for i in range(0,2)]
# testing_path = [path + r'agg_match_stats_' + str(i) + '.csv' for i in range(3,4)]

training_dfs = []
testing_dfs = []
print("Loading dataframe")
# for i in range(0,len(training_paths)):
#     df = pd.read_csv(training_paths[i], index_col=None, header=0)
#     training_dfs.append(df)

    # if(i < len(testing_path)):
    #     df2 = pd.read_csv(testing_path[i], index_col=None, header=0)
    #     testing_dfs.append(df)

train_data = pd.read_csv(path + r'agg_match_stats_0.csv', index_col=None, header=0)
# train_data = pd.concat(training_dfs, axis=0, ignore_index=True)
test_data = pd.read_csv(path + r'agg_match_stats_3.csv', index_col=None, header=0)
# test_data = pd.concat(testing_dfs, axis=0, ignore_index=True)

print("Datasets loaded")

# train_data["team_placement_cleaned"]=np.where(train_data["team_placement"]>1,2,1)
# test_data["team_placement_cleaned"]=np.where(test_data["team_placement"]>1,2,1)

train_data=train_data[[
    "party_size",
    "player_assists",
    "player_dbno",
    "player_dist_ride",
    "player_dist_walk",
    "player_dmg",
    "player_kills",
    "player_survive_time",
    "team_placement"
]].dropna(axis=0, how='any')

test_data=test_data[[
    "party_size",
    "player_assists",
    "player_dbno",
    "player_dist_ride",
    "player_dist_walk",
    "player_dmg",
    "player_kills",
    "player_survive_time",
    "team_placement"
]].dropna(axis=0, how='any')

print("Dropnas completed, starting fitting")

gnb = GaussianNB()
bnb = BernoulliNB()
mnb = MultinomialNB()

used_features = [
    "party_size",
    "player_assists",
    "player_dbno",
    "player_dist_ride",
    "player_dist_walk",
    "player_dmg",
    "player_kills",
    "player_survive_time"
]

mnb.fit(
    train_data[used_features].values,
    train_data["team_placement"]
)

print("Fitting done, starting predict")

y_pred = mnb.predict(test_data[used_features])

print("Number of mislabeled points out of a total {} points : {}, performance {:05.2f}%"
      .format(
          test_data.shape[0],
          (test_data["team_placement"] != y_pred).sum(),
          100*(1-(test_data["team_placement"] != y_pred).sum()/test_data.shape[0])
))