<?php
include 'filecache.php';
include 'config.php';
$cache->set($_GET["name"], $_GET["txt"], 3600); // key, value, expired
echo $cache->get('test');
#$cache->delete('test');
?>