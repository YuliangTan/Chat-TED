<?php
function writeLog($msg){
$logFile = 'userlogin.log';
$msg = date('Y-m-d H:i:s').' >>> '.$msg."\r\n";
file_put_contents($logFile,$msg,FILE_APPEND );
}
writeLog( $_POST["info"])
?>