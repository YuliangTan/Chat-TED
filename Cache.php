<?php
$fck    = md5('cache');//缓存名
FileCache::get($fck,'./');//获取缓存
FileCache::set($fck,$data,3600,'./'); //缓存写到某个目录
?>