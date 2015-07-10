<?php * F2 ?. s1 N* }  f
  
$filename  = dirname(__FILE__).'data.txt';
  7 |. T7 h; Z2 [5 Z7 a' E7 C
// store new message in the file
$msg = isset($_GET['msg']) ? $_GET['msg'] : ''; / f- B% X* z# D9 `6 J
if ($msg != '') $ s& t  E! V0 x/ \! X: ?
{
  file_put_contents($filename,$msg); : ?  u7 ~* K/ P- x- i
  die(); 6 p9 o# G. P1 Q5 j0 d  @' F
}
  
// infinite loop until the data file is not modified
$lastmodif    = isset($_GET['timestamp']) ? $_GET['timestamp'] : 0; / C# f* M$ O8 N1 N7 P- y, T! X: T
$currentmodif = filemtime($filename);
while ($currentmodif <= $lastmodif) // check if the data file has been modified , c7 O& k9 ?: G- |2 P, e# F4 n
{   Z" v& I$ r7 i( s
  usleep(10000); // sleep 10ms to unload the CPU 2 r5 h  Z1 w8 a# g
  clearstatcache();
  $currentmodif = filemtime($filename); / a. C/ U4 X7 v5 y% _2 P  d5 ^
}   L' R2 T7 x5 C# e- e
  
// return a json array / {7 [, k3 a3 g' H$ s. ]
$response = array();
$response['msg']       = file_get_contents($filename); 6 _1 T: `  P0 a3 V
$response['timestamp'] = $currentmodif;
echo json_encode($response); 8 g7 N6 ]/ O3 E* e- [
flush(); " f+ {( \# \% a) F6 c4 B
  6 z* q0 b( B2 K
?>, b9 b) V: ?& G