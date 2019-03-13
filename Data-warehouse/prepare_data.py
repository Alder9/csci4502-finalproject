import pandas as pd
import numpy as np
from sqlalchemy import create_engine


def create_table_from_csv(engine):
	print('Loading data set')
	# Reading the csv and putting into dataframe
	# note: change to dir. where your data set is
	df = pd.read_csv('F:\\Datasets\\pubg-match-deaths\\deaths\\kill_match_stats_final_0.csv')
	print('Data set loaded')
	print(df.head())

	# df.to_sql('agg_match_stats', engine, index=True, index_label='id')

def main():
	# Creating a local sql server for backend - this will be the store 
	# for the data warehouse
	print('Creating engine') 
	engine = create_engine('sqlite:///data.sqlite')
	print('Engine created')

	create_table_from_csv(engine)

if __name__ == '__main__':
	main()