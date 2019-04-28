<?php
    $username = "admin";
    $password = "admin123";
    $host = "localhost";
    $database = "pubg_dw";

    $server = mysql_connect($host, $user, $password);
    $connection = mysql_select_db($database, $server);

    $myquery = "
    SELECT t.time_from_beginning, k.player_name as killer_name, k.killer_pos_x, k.killer_pos_y, v.player_name as victim_name, v.victim_pos_x, v.victim_pos_y
    FROM death_fact d
    JOIN time_in_game_dimension t ON t.time_in_game_key = d.time_in_game_key
    JOIN killer_dimension k ON k.killer_key = d.killer_key
    JOIN victim_dimension v ON v.victim_key = d.victim_key
    WHERE d.match_id_key = 1
    ORDER BY 1;
    ";

    // $query = mysql_query($myquery);

    if ( ! $query ) {
        echo mysql_error();
        die;
    }

    $records = array();
    if ( $result=mysql_query($connection,$query) )
        while ( $obj=mysql_fetch_object($result) )
            $records[] = $obj;

    //echo in json format on screen       
    echo "[";
    $comma_1 = "";
    foreach($records as $obj)
    {
        echo $comma_1."{";
        $comma_2 = "";
        foreach($obj as $key => $value)
        {
            echo $comma_2.'"'.$key."\": \"". $value . "\"";
            $comma_2 = ", ";
        }
        echo "}";
        $comma_1 = ", \n";
    }    

    mysql_close($server);
?>
