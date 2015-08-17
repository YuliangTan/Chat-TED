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

   $sql =
      "INSERT INTO " . $_GET["db"] . "(NAME,PASS,FRIEND,AVATAR,INFO) 
      VALUES (" . "'" . $_GET["name"]  . "'" . "," . "'" . $_GET["pass"] 
.  "'" . "," . "'" . $_GET["friend"] . "'" . "," . "'" . $_GET["avatar"] 
. "'" . "," . $_GET["info"] . "'" . 
");";

   $ret = $db->exec($sql);
   if(!$ret){
      echo $db->lastErrorMsg();
   } else {
      echo "Records created successfully\n";
   }
   $db->close();
?>
