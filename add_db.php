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
   if($_GET["text"]=="USER"){
   	$sql =<<<EOF
      	CREATE TABLE USER
      	(
      	NAME           TEXT    NOT NULL,
      	PASS           BLOB    NOT NULL        );
	EOF;
   }
   if($_GET["text"]=="FRIEND"){
        $sql =<<<EOF
        CREATE TABLE FRIEND
        (
        NAME           TEXT    NOT NULL,
        LIST           BLOB    NOT NULL        );
        EOF;
   }

   $ret = $db->exec($sql);
   if(!$ret){
      echo $db->lastErrorMsg();
   } else {
      echo "Table created successfully\n";
   }
   $db->close();
?>
