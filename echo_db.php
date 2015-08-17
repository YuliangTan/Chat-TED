<?php
$myfile = fopen("/home/vcap/fs/2ad834759b976e6/tylchat.db", "r") or 
die("Unable to open 
file!");
echo 
fread($myfile,filesize("/home/vcap/fs/2ad834759b976e6/tylchat.db"));
fclose($myfile);
?>
