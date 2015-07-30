<?php
include 'filecache.php';
include 'config.php';
$cache->delete($_GET["name"]);
?>