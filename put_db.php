<?php
$dbhandle = sqlite_open('/home/vcap/fs/2ad834759b976e6/tylchat.db');
$query = sqlite_query($dbhandle, 'SELECT' .  $_GET["content"] . 'FROM' 
 . $_GET["db"]);
$result = sqlite_fetch_all($query, SQLITE_ASSOC);
foreach ($result as $entry) {
    echo $entry;
}
?> 
