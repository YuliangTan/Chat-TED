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
      "INSERT INTO " . $_POST["db"] . "(NAME,PASS,FRIEND,AVATAR,INFO) 
      VALUES (" . "'" . $_POST["name"]  . "'" . "," . "'" . $_POST["pass"] 
.  "'" . "," . "'" . $_POST["friend"] . "'" . "," . "'" . $_POST["avatar"] 
. "'" . "," . "'" . $_POST["info"] . "'" . 
");";
   echo $sql
   $ret = $db->exec($sql);
   if(!$ret){
      echo $db->lastErrorMsg();
   } else {
      echo "Records created successfully\n";
   }
   $db->close();
?>
