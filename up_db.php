<?php
   class MyDB extends SQLite3
   {
      function __construct()
      {
         $this->open('/home/vcap/fs/2ad834759b976e6/tylchat.db');
      }
   }
   $db = new MyDB();
   if(!$db){
      echo $db->lastErrorMsg();
   } else {
      echo "Opened database successfully\n";
   }
   $sql ="UPDATE USER set " . $_GET['label'] . "=" . "'" . 
$_GET['content'] . "'" . 
"where " . 
$_GET['name'] 
. "=" . "'" . $GET['ch'] . "'" 
. 
";";
   $ret = $db->exec($sql);
   if(!$ret){
      echo $db->lastErrorMsg();
   } else {
      echo $db->changes(), " Record updated successfully\n";
   }
   echo "Operation done successfully\n";
   $db->close();
?>
