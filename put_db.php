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

   $sql =<<<EOF
      SELECT * from USER;
EOF;

   $ret = $db->query($sql);
   while($row = $ret->fetchArray(SQLITE3_ASSOC) ){
      echo "NAME = ". $row['NAME'] ."\n";
      echo "ID = ". $row['PASS'] . "\n";
   }
   echo "Operation done successfully\n";
   $db->close();
?>