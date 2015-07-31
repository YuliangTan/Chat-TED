$redis = new Redis();
$redis->connect('10.9.21.212',5398);
$redis->auth('9145ef3c-9d30-43aa-b804-3aa66b79bf59');
$channel = $argv[1];  // channel
$msg = $argv[2];     // msg
$redis->publish('channel'.$channel, $msg);
