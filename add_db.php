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
   $sql ="
   CREATE TABLE " . $_GET['db'] . "
   (
   NAME           TEXT    NOT NULL," . "'" .
   $_GET['name'] . "'" .         "BLOB    NOT NULL        );";

   $ret = $db->exec($sql);
   if(!$ret){
      echo $db->lastErrorMsg();
   } else {
      echo "Table created successfully\n";
   }
   $db->close();
?>
