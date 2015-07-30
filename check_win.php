<?php
include 'filecache.php';
$cache = new FileCache($path = "/home/vcap/fs/2ad834759b976e6", $max_path = 100, $max_file = 50000, $gc_probality = 100);
if $_GET["del"] == 'OK'{
    $cache->delete($_GET["name"]);
}
else
{
$cache->set($_GET["name"], $_GET["txt"], 3600); // key, value, expired
echo $cache->get('test');
#$cache->delete('test');
}
?>