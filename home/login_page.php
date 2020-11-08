<?php

session_start();


//remove keywords
$substitutions = array(//111
        '&'  => '',
        '| ' => '',
        '-'  => '',
        '$'  => '',
        '`'  => '',
        '||' => '',
	"'"  => '',
    );

$dbhost = 'localhost';  // mysql server
$dbuser = 'root';            // mysql user
$dbpass = 'jyen';          // mysq password


$conn = mysqli_connect($dbhost, $dbuser, $dbpass) or die("Connect Fail");
mysqli_query($conn , "set names utf8");


$EMAIL_LOGIN = $_POST["content_10"];
$PASSWD_LOGIN   = $_POST["content_11"];

$EMAIL_LOGIN   = mysqli_real_escape_string($conn,$EMAIL_LOGIN);
$PASSWD_LOGIN   = mysqli_real_escape_string($conn,$PASSWD_LOGIN);

$EMAIL_LOGIN = str_replace( array_keys( $substitutions ), $substitutions, $EMAIL_LOGIN );
$PASSWD_LOGIN = str_replace( array_keys( $substitutions ), $substitutions, $PASSWD_LOGIN );

if($EMAIL_LOGIN == "" || $PASSWD_LOGIN=="" ){

	$_SESSION['session_success']="";
	unset($_SESSION['session_success']);

	$_SESSION['session_user_Token']="";
	unset($_SESSION['session_user_Token']);
	
	backPage("Please fill all field and try again");
}

checkToken($_SESSION[ 'session_login_Token' ],$_REQUEST['user_token']);

function backPage($input){

	$_SESSION['alert_login']=$input;

	mysql_close($conn);

        header("Location: http://www.jnsproduction.tw/login_main.php");
	exit;
}


//fix me
function checkUser($input,$email,$passwd){

	$sql="select * from list where email='$email';";
	mysqli_query($input , "set names utf8");
	mysqli_select_db( $input, 'userinfo' );
	$result = mysqli_query( $input, $sql );

	while($row=mysqli_fetch_assoc($result)){
        	if($row['email']==$email && $row['passwd']==$passwd){

			//if success login
			$_SESSION['session_success']=$row['username'];
			$_SESSION[ 'session_user_Token' ] = md5( uniqid() );
			header("Location: http://www.jnsproduction.tw/index.php");
			exit;
			return True;
        	}
	}

	return False;	
}




//authenticate user SQL
if(!checkUser($conn,$EMAIL_LOGIN ,$PASSWD_LOGIN)){

	$_SESSION['session_success']="";
	unset($_SESSION['session_success']);

	$_SESSION['session_user_Token']="";
	unset($_SESSION['session_user_Token']);

	backPage("Email or Password Error, please try again !");
}

//check $_SESSION[ 'session_login_Token' ] token
function checkToken($session_token,$user_token){
if($user_token !== $session_token || !isset($session_token) || $_SERVER['HTTP_REFERER']!=="http://www.jnsproduction.tw/login_main.php" ){

        backPage('CSRF token error');
}
else echo "CSRF token match"."<br><br>";
}



//default close session login
unset($_SESSION[ 'session_login_Token' ]);




?>

