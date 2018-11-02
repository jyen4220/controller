<?php
header("Content-Type:text/html; charset=utf-8");


session_start();

//echo "hello register"."<br>";
echo $_SESSION[ 'session_register_Token' ]."<br>";

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


$USERNAME = $_POST["content_3"];
$PASSWD   = $_POST["content_4"];
$REPASSWD   = $_POST["content_5"];
$REALUSER   = $_POST["content_6"];
$NICKUSER   = $_POST["content_7"];
$PHONEN  = $_POST["content_8"];
$EMAILN   = $_POST["content_9"];
$CLIENT = $_SERVER['REMOTE_ADDR']."";

if($USERNAME=="" || $PASSWD=="" || $REPASSWD==""||$REALUSER==""||$PHONEN==""||$EMAILN==""){
	backPage("Please fill all request!");
}

checkToken($_SESSION[ 'session_register_Token' ],$_REQUEST['user_token']);

function writeData($input,$_3,$_4,$_6,$_7,$_8,$_9,$CLIENT){
	$_10=date('Y-m-d H:i:s');
	mysqli_query($input , "set names utf8");
	$sql = "INSERT INTO list ".
        	"(username,passwd,realname,nickname,phone,email,signup_date,IP_ADDR) ".
        	"VALUES ".
        	"('$_3','$_4','$_6','$_7','$_8','$_9','$_10','$CLIENT');";

	mysqli_select_db( $input, 'userinfo' );

	$retval = mysqli_query( $input, $sql );
	if(! $retval ){
  		die('Mysql INSERT Fail: ' . mysqli_error($input));
	}

	echo "Register Success ! "."<br>".$_3."<br>";
	return True;
}

function dBug($input){
	
	echo $input."<br>";
}

function backPage($input){
	$_SESSION['alert']=':'.$input;

	mysql_close($conn);

        header("Location: http://www.jnsproduction.tw/generic.php");
	exit;
}

function checkToken($session_token,$user_token){
if($user_token !== $session_token || !isset($session_token) || $_SERVER['HTTP_REFERER']!=="http://www.jnsproduction.tw/generic.php" ){

        backPage('CSRF token error');
}
else echo "CSRF token match"."<br><br>";
}

function checkUser($input,$EMAILN){

	$sql="select * from list where email='$EMAILN';";
	mysqli_query($input , "set names utf8");
	mysqli_select_db( $input, 'userinfo' );
	$result = mysqli_query( $input, $sql );

	while($row=mysqli_fetch_assoc($result)){
        	if($row['email']==$EMAILN){
                	echo $EMAIL." is already been use"."<br>";
			return False;
                	break;
        	}
	}
	return True;	
}

$dbhost = 'localhost';  // mysql server
$dbuser = 'root';            // mysql user
$dbpass = 'jyen';          // mysq password


$conn = mysqli_connect($dbhost, $dbuser, $dbpass) or die("Connect Fail");
mysqli_query($conn , "set names utf8");


if($PASSWD !== $REPASSWD || $PASSWD=="" || $REPASSWD=="" ){
		backPage("password not correct, please try again");
}

//check input
$USERNAME = mysqli_real_escape_string($conn,$USERNAME);
$PASSWD   = mysqli_real_escape_string($conn,$PASSWD);
$REPASSWD = mysqli_real_escape_string($conn,$REPASSWD);
$REALUSER = mysqli_real_escape_string($conn,$REALUSER);
$NICKUSER = mysqli_real_escape_string($conn,$NICKUSER);
$PHONEN   = mysqli_real_escape_string($conn,$PHONEN);
$EMAILN   = mysqli_real_escape_string($conn,$EMAILN);
$CLIENT   = mysqli_real_escape_string($conn,$CLIENT);

$USERNAME = str_replace( array_keys( $substitutions ), $substitutions, $USERNAME );
$PASSWD = str_replace( array_keys( $substitutions ), $substitutions, $PASSWD );
$REPASSWD = str_replace( array_keys( $substitutions ), $substitutions, $REPASSWD );
$REALUSER = str_replace( array_keys( $substitutions ), $substitutions, $REALUSER );
$NICKUSER = str_replace( array_keys( $substitutions ), $substitutions, $NICKUSER );
$PHONEN = str_replace( array_keys( $substitutions ), $substitutions, $PHONEN );
$EMAILN = str_replace( array_keys( $substitutions ), $substitutions, $EMAILN );
$CLIENT = str_replace( array_keys( $substitutions ), $substitutions, $CLIENT );

if(!checkUser($conn,$EMAILN)){
		backPage("EMAIL is already been use");
}
if (stripos ($EMAILN, "@") == false) {

	backPage("Please fill correct Email");
}


if (stripos ($USERNAME, "<script") !== false || stripos ($PASSWD, "<script") !== false || stripos ($REPASSWD, "<script") !== false ||stripos ($REALUSER, "<script") !== false || stripos ($NICKUSER, "<script") !== false || stripos ($PHONEN, "<script") !== false || stripos ($EMAILN, "<script") !== false || stripos ($CLIENT, "<script") !== false ){

	backPage("match attack keywords:script!");
    } 




//check $_SESSION[ 'session_register_Token' ] token

//write
if(writeData($conn,$USERNAME,$PASSWD,$REALUSER,$NICKUSER,$PHONEN,$EMAILN,$CLIENT)){
	$_SESSION['session_success']=$USERNAME;
	$_SESSION[ 'session_user_Token' ] = md5( uniqid() );
	//feed back home
	header("Location: http://www.jnsproduction.tw/index.php");
	exit;
}

//close register session
unset($_SESSION[ 'session_register_Token' ]);

?>
