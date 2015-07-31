$redis = new Redis();
$redis->connect('127.0.0.1',6379);
$channel = $argv[1];  // channel
$redis->subscribe(array('channel'.$channel), 'callback');
function callback($instance, $channelName, $message) {
  print $channelName, "==>", $message,PHP_EOL;
}
