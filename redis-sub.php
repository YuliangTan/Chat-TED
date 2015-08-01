<?php
header(“Refresh: 1″);
$redis = new Redis();
$redis->connect('10.9.21.212',5398);
$redis->auth('9145ef3c-9d30-43aa-b804-3aa66b79bf59');
$channel = $argv[1];  // channel
$redis->subscribe(array('channel'.$channel), 'callback');
function callback($instance, $channelName, $message) {
  print $channelName, "==>", $message,PHP_EOL;
}
?>