<?php
include 'filecache.php';
$cache = new FileCache($path = "/home/vcap/fs/2ad834759b976e6", $max_path = 100, $max_file = 50000, $gc_probality = 100);

//数据缓存
$cache->set('test', 'file cache test', 3600); // key, value, expired
$cache->get('test');
#$cache->delete('test');

//片段缓存
if($cache->startCache('html', 3600)) // key, expired
{

  $cache->endCache();
}
?>