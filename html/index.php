<?php
session_start();

$_SESSION[ 'session_token' ] = md5( uniqid() );



?>





<html>

<head>

<meta http-equiv="Content-Type" content="text/html; charset=big5">

<title>Register Your Information</title>

</head>

<body>



<form method="POST" action="1_index.php">




Name<input type="text" name="content_1" size="16"><br><br>

IP Address<input type="text" name="content_2" size="10">

<input type="submit" value="send" name="button_1">


<input type='hidden' name='user_token' value="<?php echo $_SESSION['session_token'] ?>" />


</form>

</body>
</html>
<?php
echo  $_SESSION['alert'];
unset($_SESSION['alert']);
?>

