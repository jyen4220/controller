<?php 

session_start();

$_SESSION['session_token']= md5( uniqid() );


echo $_SESSION['session_token'];

echo'<p><a href="index.html">back</a></p>';
	
?>
