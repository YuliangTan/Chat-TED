<?php
$file = "/home/vcap/fs/2ad834759b976e6/tylchat.db";
if (!unlink($file))
  {
  echo ("Error deleting $file");
  }
else
  {
  echo ("Deleted $file");
  }
?>
