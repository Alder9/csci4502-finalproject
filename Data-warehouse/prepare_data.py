import pandas as pd
import numpy as np
from sqlalchemy import create_engine
import pymysql
import mysql.connector
import time
from datetime import datetime


def load_from_csv(engine):
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
	for chunk in pd.read_csv('F:\\Datasets\\pubg-match-deaths\\aggregate\\agg_match_stats_1.csv', chunksize=100):
		chunk.to_sql('aggregate', con=engine, if_exists='append', index=False)
		chunk_count += 100
		print(chunk.iloc[0,0])
		print('{} rows loaded'.format(chunk_count))

	# print('Data set loaded')
	# print(dfKills.head())
	# print('-------------------')
	# print(dfAgg.head())

def check_match_ids(cursor):
	print("Checking match ids")
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
	with open("MatchesInDW.txt") as f:
		lines = f.read().splitlines()
	match_ids_to_insert = list(set(matching_match_ids).difference(lines))
	
	# print("matching_match_ids: {}".format(len(matching_match_ids)))

	return match_ids_to_insert

def insert_row(dwcursor, dimension_dict, table):
	print("inserting row")
	placeholders = ', '.join(['%s'] * len(dimension_dict))
	columns = ', '.join(dimension_dict.keys())
	insert_statement = """INSERT INTO %s (%s)
				VALUES (%s)""" % (table, columns, placeholders)
	dwcursor.execute(insert_statement, list(dimension_dict.values()))

	id = dwcursor.lastrowid
	# return the id of the recently inserted row
	return id

def select_dw_row(dwcursor, dimension_dict, table, table_key):
	print("selecting from datawarehouse")
	conditionals = []
	for key, value in dimension_dict.items():
		conditionals.append("{} = '{}'".format(key, value))
	where_statement = ' AND '.join(conditionals)
	dw_query = """SELECT %s FROM %s WHERE %s """ % (table_key, table, where_statement)
	print(dw_query)
	dwcursor.execute(dw_query)
	row = dwcursor.fetchall()

	return row

def sort_and_insert_match(match_id, aggregates_in_match, deaths_in_match, dbcursor, dwcursor, dw):
	print('Sorting and inserting: {}'.format(match_id))
	players = {}
	# Get all of the players in aggregate
	for aggregate in aggregates_in_match:
		name = aggregate[11]
		game_size = aggregate[1]
		date = aggregate[0]
		match_id = aggregate[2]
		match_mode = aggregate[3]
		stats = {
			"party_size": aggregate[4],
			"player_assists": aggregate[5],
			"player_dbno": aggregate[6],
			"player_dist_ride": aggregate[7],
			"player_dist_walk": aggregate[8],
			"player_dmg": aggregate[9],
			"player_kills": aggregate[10],
			"player_survive_time": aggregate[12],
			"team_id": aggregate[13],
			"team_placement": aggregate[14]
		}

		players[name] = stats

	print('game_size: {}'.format(game_size))
	print('length of players: {}'.format(len(players)))

	# for key, value in players.items():
		# print (key) 

	# Convert the date to datetime for date dimension
	match_datetime = datetime.strptime(date, "%Y-%m-%dT%H:%M:%S+0000")
	if match_datetime.weekday() > 5:
		weekend = 1
	else:
		weekend = 0
	print(date)
	print(match_datetime)

	death_count = 0

	# Sort items into dictionary for each dimension - do for all dimensions/
	# attributes before inserting

	# These dimensions outside of death for loop only need one per match
	match_mode_dimension = {
		"match_mode": match_mode
	}

	match_id_dimension = {
		"match_id": match_id
	}

	match_date_dimension = {
		"match_date": match_datetime,
		"match_day": match_datetime.day,
		"match_month": match_datetime.month,
		"match_year": match_datetime.year,
		"weekend": weekend,
		"match_hour": match_datetime.hour,
		"match_minute": match_datetime.minute,
		"match_second": match_datetime.second
	}

	# Insert match_mode, match_id, match_date into tables - get the id
	# So we can insert into fact tables
	# ONLY NEED TO INSERT ONE PER MATCH
	match_mode_key = insert_row(dwcursor, match_mode_dimension, "MATCH_MODE_DIMENSION")
	match_id_key = insert_row(dwcursor, match_id_dimension, "MATCH_ID_DIMENSION")
	match_date_key = insert_row(dwcursor, match_date_dimension, "MATCH_DATE_DIMENSION")
	print("Inserted match_date, match_id, match_date")
	print("Keys: {},{},{}".format(match_mode_key, match_id_key, match_date_key))
	total_deaths = len(deaths_in_match)
	# print('total death: {}'.format(len(deaths_in_match)))
	for death in deaths_in_match:
		death_count += 1
		killer_name = death[1]
		victim_name = death[8]

		# NEED TO MAKE SURE NOT ADDING DUPLICATE PLAYERS IN KILLERS AND
		# VICTIM DIMENSIONS
		if killer_name != None and killer_name in players.keys():
			killer = players[killer_name]
			# populate dimension dictionary
			killer_dimension = {
				"player_name": killer_name,
				"killer_placement": death[2],
				"killer_pos_x": death[3],
				"killer_pos_y": death[4],
				"killer_match_kills": killer["player_kills"],
				"killer_survive_time": killer["player_survive_time"],
				"killer_team_id": killer["team_id"],
				"killer_team_placement": killer["team_placement"],
				"killer_dist_ride": killer["player_dist_ride"],
				"killer_dist_walk": killer["player_dist_walk"],
				"killer_match_dmg": killer["player_dmg"],
				"killer_match_assists": killer["player_assists"],
				"killer_match_dbno": killer["player_dbno"],
				"party_size": killer["party_size"]
			}
		else:
			# will end up here if Bluezone or fell to death
			killer_dimension = {
				"player_name": death[0]
			}
		# Ensure that its not in datawarehouse
		# add if not, get id if so
		killer_row = select_dw_row(dwcursor, killer_dimension, "KILLER_DIMENSION", "killer_key")
		# If the row is an empty list this means that killer is not in dimension table
		if not killer_row:
			killer_key = insert_row(dwcursor, killer_dimension, "KILLER_DIMENSION")
		else:
			# row is not empty, get the key
			killer_key = killer_row[0][0]
		print('Killer_key: {}'.format(killer_key))

		if victim_name in players.keys():
			victim = players[victim_name]
			victim_dimension = {
				"player_name": victim_name,
				"victim_placement": death[9],
				"victim_pos_x": death[10],
				"victim_pos_y": death[11],
				"victim_match_kills": victim["player_kills"],
				"victim_survive_time": victim["player_survive_time"],
				"victim_team_id": victim["team_id"],
				"victim_team_placement": victim["team_placement"],
				"victim_dist_ride": victim["player_dist_ride"],
				"victim_dist_walk": victim["player_dist_walk"],
				"victim_match_dmg": victim["player_dmg"],
				"victim_match_assists": victim["player_assists"],
				"victim_match_dbno": victim["player_dbno"],
				"party_size": victim["party_size"],
				"killed_by": death[0]
			}
		else:
			victim_dimension = {
				"player_name": victim_name
			}

		# check if in data warehouse - add or get id
		victim_row = select_dw_row(dwcursor, victim_dimension, "VICTIM_DIMENSION", "victim_key")
		if not victim_row:
			print("inserting victim")
			victim_key = insert_row(dwcursor, victim_dimension, "VICTIM_DIMENSION")
		else:
			victim_key = victim_row[0][0]

		print('victim_key: {}'.format(victim_key))		

		time_in_game_dimension = {
			"time_from_beginning": death[7]
		}
		time_in_game_row = select_dw_row(dwcursor, time_in_game_dimension, "TIME_IN_GAME_DIMENSION", "time_in_game_key")
		if not time_in_game_row:
			time_in_game_key = insert_row(dwcursor, time_in_game_dimension, "TIME_IN_GAME_DIMENSION")
		else:
			time_in_game_key = time_in_game_row[0][0]
		print("time_in_game key: {}".format(time_in_game_key))
		
		fact_table = {
			"kill_count": total_deaths,
			"match_date_key": match_date_key,
			"match_id_key": match_id_key,
			"match_mode_key": match_mode_key,
			"time_in_game_key": time_in_game_key,
			"killer_key": killer_key,
			"victim_key": victim_key,
			"game_size": game_size
		}

		print('DEATH_FACT entry: {}'.format(fact_table))
		
		insert_row(dwcursor, fact_table, "DEATH_FACT")

		dw.commit()

	# Add match_id to file to keep track of matches we have
	f = open("MatchesInDW.txt", "a")
	f.write(match_id)
	f.close()

def populate_tables(dbcursor, dwcursor, match_ids, dw):
	# Two ways tables can be populated:
	# Use dataframes for everything, one match at a time insert into tables
	# Query into MySQL server which has raw csv data in it
	total_matches = len(match_ids)
	# print('total matches: {}'.format(len(match_ids)))
	match_count = 0
	for match_id_row in match_ids:
		match_id = match_id_row[0]
		
		aggregate_query = "SELECT * FROM aggregate WHERE match_id = %s"
		dbcursor.execute(aggregate_query, (match_id,))
		aggregates_in_match = dbcursor.fetchall()
		
		deaths_query = "SELECT * FROM deaths WHERE match_id = %s"
		dbcursor.execute(deaths_query, (match_id,))
		deaths_in_match = dbcursor.fetchall()

		sort_and_insert_match(match_id, aggregates_in_match, deaths_in_match, dbcursor, dwcursor, dw)
		match_count += 1
		print("match {} entered out of {}".format(match_count, total_matches))

	return

def main():
	# Connecting to local sql server for backend - this will be the store 
	# for the data warehouse

	# print('Creating engine') 
	# MySQL server on localhost:3306 with user admin
	# engine = create_engine('mysql+pymysql://admin:admin123@localhost:3306/pubg')
	# print('Engine created')

	db = mysql.connector.connect(
		host='localhost',
		user='admin',
		passwd='admin123',
		database='pubg',
		auth_plugin='mysql_native_password'
	)

	dw = mysql.connector.connect(
		host='localhost',
		user='admin',
		passwd='admin123',
		database='pubg_dw',
		auth_plugin='mysql_native_password'
	)

	dbcursor = db.cursor()
	dwcursor = dw.cursor()

	# load_from_csv(engine)

	match_ids = check_match_ids(dbcursor)
	populate_tables(dbcursor, dwcursor, match_ids, dw)
	

	# create_table_from_csv(engine)
	dbcursor.close()
	dwcursor.close()
	db.close()
	dw.close()

if __name__ == '__main__':
	main()