USE pubg_dw;

SELECT * FROM KILLER_DIMENSION
INTO OUTFILE 'F:/Datasets/Data-warehouse/killer_dimension.csv'
FIELDS TERMINATED BY ','
OPTIONALLY ENCLOSED BY '"'
ESCAPED BY ""
LINES TERMINATED BY '\n';

SELECT * FROM VICTIM_DIMENSION
INTO OUTFILE 'F:/Datasets/Data-warehouse/victim_dimension.csv'
FIELDS TERMINATED BY ','
OPTIONALLY ENCLOSED BY '"'
ESCAPED BY ""
LINES TERMINATED BY '\n';

SELECT * FROM MATCH_DATE_DIMENSION
INTO OUTFILE 'F:/Datasets/Data-warehouse/match_date_dimension.csv'
FIELDS TERMINATED BY ','
OPTIONALLY ENCLOSED BY '"'
ESCAPED BY ""
LINES TERMINATED BY '\n';

SELECT * FROM MATCH_ID_DIMENSION
INTO OUTFILE 'F:/Datasets/Data-warehouse/match_id_dimension.csv'
FIELDS TERMINATED BY ','
OPTIONALLY ENCLOSED BY '"'
ESCAPED BY ""
LINES TERMINATED BY '\n';

SELECT * FROM TIME_IN_GAME_DIMENSION
INTO OUTFILE 'F:/Datasets/Data-warehouse/time_in_game_dimension.csv'
FIELDS TERMINATED BY ','
OPTIONALLY ENCLOSED BY '"'
ESCAPED BY ""
LINES TERMINATED BY '\n';

SELECT * FROM MATCH_MODE_DIMENSION
INTO OUTFILE 'F:/Datasets/Data-warehouse/match_mode_dimension.csv'
FIELDS TERMINATED BY ','
OPTIONALLY ENCLOSED BY '"'
ESCAPED BY ""
LINES TERMINATED BY '\n';

SELECT * FROM DEATH_FACT
INTO OUTFILE 'F:/Datasets/Data-warehouse/death_fact.csv'
FIELDS TERMINATED BY ','
OPTIONALLY ENCLOSED BY '"'
ESCAPED BY ""
LINES TERMINATED BY '\n';