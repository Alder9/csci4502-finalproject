from cubes import Workspace
from cubes import PointCut
from cubes import Cell
from cubes.compat import ConfigParser
import numpy as np
import math

def get_distance(x1, y1, x2, y2):
	return math.sqrt((x1 - x2)**2 + (y1 - y2)**2)

def compare_kill_distances(browser, cube):
	first_place_distances = np.array([])
	all_distances = np.array([])
	cuts = [
		PointCut("match_date_dimension", [2017])
	]
	cell = Cell(cube, cuts)
	result = browser.aggregate(drilldown=["killer_dimension","victim_dimension"])
	# print(result.summary["record_count"])
	for record in result:
		distance = 0
		x1 = record["killer_dimension.killer_pos_x"]
		x2 = record["victim_dimension.victim_pos_x"]
		y1 = record["killer_dimension.killer_pos_y"]
		y2 = record["victim_dimension.victim_pos_y"]
		if(y1 != None and y2 != None and x1 != None and x2 != None):
			distance = get_distance(x1, y1, x2, y2)
			if(record["killer_dimension.killer_placement"] == 1):
				first_place_distances = np.append(first_place_distances, distance)
			all_distances = np.append(all_distances, distance)
	
	first_place_average_kill_distance = np.mean(first_place_distances)
	average_kill_distance = np.mean(all_distances)

	print("First place averages a kill distance of: {}".format(first_place_average_kill_distance))
	print("Average kill distance in comparison: {}".format(average_kill_distance))

	return first_place_average_kill_distance - average_kill_distance

def count_match_deaths(browser, cube):
	deaths = np.array([])
	result = browser.aggregate(drilldown=["match_id_dimension"])
	for record in result:
		deaths = np.append(deaths, record['deaths'])

	average_deaths = np.mean(deaths)
	print("Average deaths per match: {}".format(average_deaths))

def main():
	settings = ConfigParser()
	settings.read("slicer.ini")
	# Creating workspace
	workspace = Workspace(config=settings)
	# Creating browser so that we can do actual aggregations and other data queries for the cube
	browser = workspace.browser('death_fact')
	cube = browser.cube
	# Pass browser in data_aggregate - this function will do all aggregations and queries
	compare_kill_distances(browser, cube)
	count_match_deaths(browser, cube)

if __name__ == '__main__':
	main() 