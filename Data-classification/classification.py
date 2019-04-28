import numpy as np
import pandas as pd
from sklearn.naive_bayes import GaussianNB, BernoulliNB, MultinomialNB

# Import first two csvs as training set
matthew_path = r'C:/Users/matt-/Desktop/Data Mining/pubg-match-deaths/aggregate/'
thomas_path = r'F:/Datasets/pubg-match-deaths/aggregate/'

path = thomas_path

# Training data will be agg_match_stats_0
# Testing data will be agg_match_stats_3


print("Loading dataframe")
training_dfs = []
testing_dfs = []


train_data = pd.read_csv(path + r'agg_match_stats_0.csv', index_col=None, header=0)
test_data = pd.read_csv(path + r'agg_match_stats_3.csv', index_col=None, header=0)

print("Datasets loaded, starting cleaning")

train_data["team_placement_cleaned"]=np.where(train_data["team_placement"]==1, 0, 1)
test_data["team_placement_cleaned"]=np.where(test_data["team_placement"]==1, 0, 1)

train_data=train_data[[
    "party_size",
    "player_assists",
    "player_dbno",
    "player_dist_ride",
    "player_dist_walk",
    "player_dmg",
    "player_kills",
    "player_survive_time",
    "team_placement_cleaned"
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
    "team_placement_cleaned"
]].dropna(axis=0, how='any')

print("Cleaning finished, starting fitting")

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

bnb.fit(
    train_data[used_features].values,
    train_data["team_placement_cleaned"]
)

print("Fitting done, starting predictions")

y_pred = bnb.predict(test_data[used_features])

print("Number of mislabeled points out of a total {} points : {}, performance {:05.2f}%"
      .format(
          test_data.shape[0],
          (test_data["team_placement_cleaned"] != y_pred).sum(),
          100*(1-(test_data["team_placement_cleaned"] != y_pred).sum()/test_data.shape[0])
))

mean_assists = np.mean(train_data[train_data["team_placement_cleaned"]==0]["player_assists"])
std_assists = np.std(train_data[train_data["team_placement_cleaned"]==0]["player_assists"])
mean_kills = np.mean(train_data[train_data["team_placement_cleaned"]==0]["player_kills"])
std_kills = np.std(train_data[train_data["team_placement_cleaned"]==0]["player_kills"])
mean_dbno = np.mean(train_data[train_data["team_placement_cleaned"]==0]["player_dbno"])
std_dbno = np.std(train_data[train_data["team_placement_cleaned"]==0]["player_dbno"])
mean_dist_walk = np.mean(train_data[train_data["team_placement_cleaned"]==0]["player_dist_walk"])
std_dist_walk =  np.std(train_data[train_data["team_placement_cleaned"]==0]["player_dist_walk"])
mean_dist_ride = np.mean(train_data[train_data["team_placement_cleaned"]==0]["player_dist_ride"])
std_dist_ride = np.std(train_data[train_data["team_placement_cleaned"]==0]["player_dist_ride"])
mean_dmg = np.mean(train_data[train_data["team_placement_cleaned"]==0]["player_dmg"])
std_dmg = np.std(train_data[train_data["team_placement_cleaned"]==0]["player_dmg"])
mean_survive_time = np.mean(train_data[train_data["team_placement_cleaned"]==0]["player_survive_time"])
std_survive_time = np.std(train_data[train_data["team_placement_cleaned"]==0]["player_survive_time"])

print("Mean assists = {}".format(mean_assists))
print("Std assists = {}".format(std_assists))
print("Mean kills = {}".format(mean_kills))
print("Std kills = {}".format(std_kills))
print("Mean dbno = {}".format(mean_dbno))
print("Std dbno = {}".format(std_dbno))
print("Mean dist_walk = {}".format(mean_dist_walk))
print("Std dist_walk = {}".format(std_dist_walk))
print("Mean dist_ride = {}".format(mean_dist_ride))
print("Std dist_ride = {}".format(std_dist_ride))
print("Mean dmg = {}".format(std_dmg))
print("Std dmg = {}".format(std_assists))
print("Mean survive_time = {}".format(mean_survive_time))
print("Std survive_time = {}".format(std_survive_time))