USE pubg_dw;

SELECT DISTINCT match_id_key FROM death_fact;

SELECT time_in_game_key, COUNT(*) FROM death_fact
GROUP BY time_in_game_key;

SELECT t.time_from_beginning, COUNT(*)
FROM time_in_game_dimension t
JOIN death_fact d ON t.time_in_game_key = d.time_in_game_key
GROUP BY t.time_from_beginning
ORDER BY 1 DESC LIMIT 100;

SELECT t.time_from_beginning
FROM time_in_game_dimension t
JOIN death_fact d ON t.time_in_game_key = d.time_in_game_key;

SELECT v.killed_by, COUNT(*)
FROM victim_dimension v
JOIN death_fact d ON v.victim_key = d.victim_key
GROUP BY v.killed_by
ORDER BY 2 DESC LIMIT 10;

SELECT DISTINCT killer_key FROM death_fact;