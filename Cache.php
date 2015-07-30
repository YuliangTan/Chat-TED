<?php
include 'filecache.php';
$cache = new FileCache();

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