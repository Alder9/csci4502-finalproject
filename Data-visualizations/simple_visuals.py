import matplotlib.pyplot as plt
from matplotlib import colors
import numpy as np
import mysql.connector


def create_histogram(data, n_bins, x_tick_max, x_step, y_step, title, xlabel, ylabel):
    fig, ax = plt.subplots(1,1,figsize=(8,6))
    N, bins, patches = ax.hist(data, bins=n_bins)
    fracs = N / N.max()
    norm = colors.Normalize(fracs.min(), fracs.max())
    for thisfrac, thispatch in zip(fracs, patches):
        color = plt.cm.inferno(norm(thisfrac))
        thispatch.set_facecolor(color)
    x_ticks = [i for i in range(0, x_tick_max, x_step)]
    y_ticks = [i for i in range(0, 6001, y_step)]
    plt.xticks(x_ticks)
    plt.yticks(y_ticks)
    plt.title(title)
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.show()

def time_in_game_frequency_histogram(dwcursor):
    # Creating a histogram representing the frequency of time of deaths
    # Want to get all of the keys from the fact_table
    query = '''
    SELECT t.time_from_beginning
    FROM time_in_game_dimension t
    JOIN death_fact d ON t.time_in_game_key = d.time_in_game_key;
    '''
    times = [] # This will hold all of the time_in_game
    dwcursor.execute(query)
    sql_times = dwcursor.fetchall()
    for time in sql_times:
        times.append(time[0])
    create_histogram(times, 50, 2190, 150, 500, "Time of Deaths Across 792 Matches of PUBG", 
    "Time in game from beginning of death (seconds)", "Frequency")
    
    return 

def most_popular_killedby(dwcursor):
    # Get the top 10 reasons people are killed during the game
    query = '''
    SELECT v.killed_by, COUNT(*)
    FROM victim_dimension v
    JOIN death_fact d ON v.victim_key = d.victim_key
    GROUP BY v.killed_by
    ORDER BY 2 DESC LIMIT 10;
    '''
    killedby = [] # holds the top ten killed_by
    count = [] # holds the counts of them
    
    dwcursor.execute(query)
    results = dwcursor.fetchall()
    for result in results:
        killedby.append(result[0])
        count.append(int(result[1]))
    x = np.arange(len(killedby))
    fig, ax = plt.subplots(1,1,figsize=(8,6))
    ax.bar(x, count)
    plt.xticks(x, killedby)
    plt.setp(ax.get_xticklabels(), rotation=30)
    plt.title("Ways of Death Across 792 Matches")
    plt.xlabel("Way of death")
    plt.ylabel("Count")
    plt.show()
    return

def main():
    # Connect to local sql server which is the DW
    dw = mysql.connector.connect(
		host='localhost',
		user='admin',
		passwd='admin123',
		database='pubg_dw',
		auth_plugin='mysql_native_password'
	)

    dwcursor = dw.cursor()
    # First plotting where during the match the kills are the most frequent
    # time_in_game_frequency_histogram(dwcursor)
    most_popular_killedby(dwcursor)

    dwcursor.close()
    dw.close()
    return

if __name__ == "__main__":
    main()