<?php
$dbconn3 = pg_connect("host=c3.east1.stormdb.us port=5432 dbname=k1382186238 user=admin password=baconPancakes#12345") or die ("No se pudo conectar a PostGres --> " . pg_last_error($dbconn3)); 
$result=pg_exec("INSERT INTO question_info Values ('cuantas patas tiene el gato', 4)"); // Sample of SQL QUERY 
//$fetch = pg_fetch_row($query_st); // Sample of SQL QUERY 

pg_close($dbconn3);
?>
