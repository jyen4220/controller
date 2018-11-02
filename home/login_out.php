<?php 

session_start();

$_SESSION['session_success']="";
unset($_SESSION['session_success']);

$_SESSION['session_user_Token']="";
unset($_SESSION['session_user_Token']);

header("Location: http://www.jnsproduction.tw/index.php");
exit;


?>
