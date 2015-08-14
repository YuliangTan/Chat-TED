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
   }

   $sql ="SELECT " . "'" . $_GET["content"] . "'" . " from " . 
"'" . $_GET["db"] . "'" . 
";";

   $ret = $db->query($sql);
   while($row = $ret->fetchArray(SQLITE3_ASSOC) ){
      echo $row;
   }
   $db->close();
?>
