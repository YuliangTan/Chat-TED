<?php
include 'filecache.php';
$cache = new FileCache($path = "/home/vcap/fs/2ad834759b976e6",$max_path = 9999999, $max_file = 9999999, $gc_probality = 100);
if ($_GET["del"]=='OK'){
    $cache->delete($_GET["name"]);
}
elseif ($_GET["check"]=='OK'){
echo $cache->get($_GET["name"]);
} else {
$cache->set($_GET["name"], $_GET["txt"], 3600); // key, value, expired
}
?>