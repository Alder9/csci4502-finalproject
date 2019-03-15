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

	# Turn dataframes to SQL tables and insert into MySQL connection
	# If the table exists, for the time being, replace it
	dfAgg.to_sql('player', con=engine, if_exists='replace')
	dfKills.to_sql('death', con=engine, if_exists='replace')
	print('Sql tables created')
	

def main():
	# Connecting to local sql server for backend - this will be the store 
	# for the data warehouse
	print('Creating engine') 
	# MySQL server on localhost:3306 with user admin
	engine = create_engine('mysql://admin:admin123@localhost:3306/pubg')
	print('Engine created')

	# create_table_from_csv(engine)
	# aggregate()

if __name__ == '__main__':
	main()