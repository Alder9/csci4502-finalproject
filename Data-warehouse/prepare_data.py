import pandas as pd
import numpy as np
from sqlalchemy import create_engine
import pymysql
import mysql.connector


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

def check_match_ids(cursor):
	deaths_query = "SELECT DISTINCT match_id FROM deaths WHERE map = %s"
	cursor.execute(deaths_query, ("ERANGEL", ))
	death_matchids = cursor.fetchall()

	cursor.execute("SELECT DISTINCT match_id FROM aggregate")
	aggregate_matchids = cursor.fetchall()

	# print("sizes of each:")
	# print("death_matchids: {}".format(len(death_matchids)))
	# print("aggregate_matchids: {}".format(len(aggregate_matchids)))

	# if(death_matchids == aggregate_matchids):
	# 	print('All match_ids accounted for')
	# else:
	# 	print('Mismatching match_ids - not all are in each')

	matching_match_ids = list(set(death_matchids).intersection(aggregate_matchids))

	# print("matching_match_ids: {}".format(len(matching_match_ids)))

	return matching_match_ids

def populate_tables(engine, cursor, match_ids):
	# Two ways tables can be populated:
	# Use dataframes for everything, one match at a time insert into tables
	# Query into MySQL server which has raw csv data in it
	first_match_id = match_ids[0][0]
	print(first_match_id)

	aggregate_query = "SELECT * FROM aggregate WHERE match_id = %s"
	cursor.execute(aggregate_query, (first_match_id,))
	aggregates_in_match = cursor.fetchall()
	for aggregate in aggregates_in_match:
		print(aggregate)


	deaths_query = "SELECT * FROM deaths WHERE match_id = %s"
	cursor.execute(deaths_query, (first_match_id,))
	deaths_in_match = cursor.fetchall()
	for death in deaths_in_match:
		print(death)

	return

def main():
	# Connecting to local sql server for backend - this will be the store 
	# for the data warehouse

	print('Creating engine') 
	# MySQL server on localhost:3306 with user admin
	engine = create_engine('mysql+pymysql://admin:admin123@localhost:3306/pubg')
	print('Engine created')

	db = mysql.connector.connect(
		host='localhost',
		user='admin',
		passwd='admin123',
		database='pubg',
		auth_plugin='mysql_native_password'
	)

	mycursor = db.cursor()

	match_ids = check_match_ids(mycursor)
	populate_tables(engine, mycursor, match_ids)

	# create_table_from_csv(engine)
	mycursor.close()
	db.close()

if __name__ == '__main__':
	main()