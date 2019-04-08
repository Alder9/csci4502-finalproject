import pandas as pd
import numpy as np
from sqlalchemy import create_engine
import pymysql


def create_table_from_csv(engine):
	print('Loading data set')
	# Reading the csv and putting into dataframe
	# note: change to dir. where your data set is
	# chunk_count = 0
	# for chunk in pd.read_csv('F:\\Datasets\\pubg-match-deaths\\deaths\\kill_match_stats_final_0.csv', chunksize=10):
	# 	chunk.to_sql('deaths', con=engine, if_exists='append', index=False)
	# 	chunk_count += 10
	# 	# print(chunk.iloc[0,0])
	# 	print('{} rows loaded'.format(chunk_count))

	chunk_count = 0
	for chunk in pd.read_csv('F:\\Datasets\\pubg-match-deaths\\aggregate\\agg_match_stats_0.csv', chunksize=100):
		chunk.to_sql('aggregate', con=engine, if_exists='append', index=False)
		chunk_count += 100
		print(chunk.iloc[0,0])
		print('{} rows loaded'.format(chunk_count))

	# print('Data set loaded')
	# print(dfKills.head())
	# print('-------------------')
	# print(dfAgg.head())

	# Turn dataframes to SQL tables and insert into MySQL connection
	# If the table exists, for the time being, replace it
	print('Sql table created')
	

def main():
	# Connecting to local sql server for backend - this will be the store 
	# for the data warehouse

	print('Creating engine') 
	# MySQL server on localhost:3306 with user admin
	engine = create_engine('mysql+pymysql://admin:admin123@localhost:3306/pubg')
	print('Engine created')

	create_table_from_csv(engine)

if __name__ == '__main__':
	main()