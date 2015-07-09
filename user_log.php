<?php
function writeLog(){
$logFile = 'userlogin.log';
$msg = date('Y-m-d H:i:s').' >>> '.$_GET["info"]."\r\n";
file_put_contents($logFile,$msg,FILE_APPEND );
}
writeLog();
echo $_GET["info"];
?>