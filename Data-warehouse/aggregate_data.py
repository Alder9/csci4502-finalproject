from cubes import Workspace

def data_aggregate(browser):
	result = browser.aggregate()
	print(result.summary["record_count"])

def main():
	# Creating workspace
	workspace = Workspace(config='slicer.ini')
	# Creating browser so that we can do actual aggregations and other data queries for the cube
	browser = workspace.browser('match')

	# Pass browser in data_aggregate - this function will do all aggregations and queries
	data_aggregate(browser)

if __name__ == '__main__':
	main()