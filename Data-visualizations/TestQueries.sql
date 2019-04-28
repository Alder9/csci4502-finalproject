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

SELECT t.time_from_beginning, k.player_name as killer_name, k.killer_pos_x, k.killer_pos_y, v.player_name, v.victim_pos_x, v.victim_pos_y
FROM death_fact d
JOIN time_in_game_dimension t ON t.time_in_game_key = d.time_in_game_key
JOIN killer_dimension k ON k.killer_key = d.killer_key
JOIN victim_dimension v ON v.victim_key = d.victim_key
WHERE d.match_id_key = 1
ORDER BY 1;