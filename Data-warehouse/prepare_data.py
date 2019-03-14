import pandas as pd
import numpy as np
from sqlalchemy import create_engine


def create_table_from_csv(engine):
	print('Loading data set')
	# Reading the csv and putting into dataframe
	# note: change to dir. where your data set is
	dfKills = pd.read_csv('F:\\Datasets\\pubg-match-deaths\\deaths\\kill_match_stats_final_0.csv')
	dfAgg = pd.read_csv('F:\\Datasets\\pubg-match-deaths\\aggregate\\agg_match_stats_0.csv')
	print('Data set loaded')
	print(dfKills.head())
	print('-------------------')
	print(dfAgg.head())

	dfAgg.to_sql('player', engine)
	dfKills.to_sql('death', engine)
	print('Sql tables created')

def aggregate():
	browser = workspace.browser("match")
	result = browser.aggregate()
	print(result.summary["record_count"])
	

def main():
	# Creating a local sql server for backend - this will be the store 
	# for the data warehouse
	print('Creating engine') 
	engine = create_engine('sqlite:///data.sqlite')
	print('Engine created')

	create_table_from_csv(engine)
	aggregate()

if __name__ == '__main__':
	main()