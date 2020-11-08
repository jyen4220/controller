<?php
session_start();

$dbhost = 'localhost';  // mysql server
$dbuser = 'root';            // mysql user
$dbpass = 'jyen';          // mysq password
$conn = mysqli_connect($dbhost, $dbuser, $dbpass) or die("Connect Fail");

function dBug($input){
	
	echo $input."<br>";
}
 
function checkToken($session_token,$user_token){
if($user_token !== $session_token || !isset($session_token)){

        backPage('CSRF token error');
}
else echo "CSRF token match"."<br><br>";
}

function backPage($input){
	$_SESSION['alert']=$input;
        unset($_SESSION['session_token']);
        unset($_SESSION['user_token']);
	mysql_close($conn);

//	header('Location: ' . $_SERVER['HTTP_REFERER']);
        header("Location:index.php");

	exit;
}

function checkUser($input,$name_1){

	$sql="select * from list where name='$name_1';";

	mysqli_select_db( $input, 'registers' );
	$result = mysqli_query( $input, $sql );

	while($row=mysqli_fetch_assoc($result)){
        	if($row['name']==$name_1){
                	echo $name_1." is already use"."<br>";
			return False;
                	break;
        	}
	}
	return True;	
}

function readData($input){
	mysqli_select_db( $input, 'registers' );

	$sql="select * from list;";

	$q = mysqli_query( $input, $sql );


	while($row=mysqli_fetch_assoc($q)){

        	echo "<tr><td>".$row['id']."</td>"."<td>".$row['name']."</td>"."<td>".$row['ip']."</td></tr>";

        	echo "<br>";

	}
}


function writeData($input,$name_1,$ip_2){
	$sql = "INSERT INTO list ".
        	"(name,ip) ".
        	"VALUES ".
        	"('$name_1','$ip_2')";

	mysqli_select_db( $input, 'registers' );

	$retval = mysqli_query( $input, $sql );
	if(! $retval ){
  		die('Mysql INSERT Fail: ' . mysqli_error($input));
	}

	echo "Mysql INSERT Success"."<br>";
}



/*if(! $conn )
{
  die('Connect Fail: ' . mysqli_error($conn));
}
*/
dBug(' Mysql Connect Success');
echo "<br>";
dBug($_SESSION['session_token']);
dBug($_REQUEST['user_token']);
echo "<br>";

//222
checkToken($_SESSION['session_token'],$_REQUEST['user_token']);


mysqli_query($conn , "set names utf8");
 
#$name = 'JYEN Chen';
#$ip = '140.123.92.128';

//remove keywords
$substitutions = array(//111
        '&'  => '',
        ';'  => '',
        '| ' => '',
        '-'  => '',
        '$'  => '',
        '('  => '',
        ')'  => '',
        '`'  => '',
        '||' => '',
	"'"  => '',
    );

$name = $_POST["content_1"];
$ip   = $_POST["content_2"];

$name = mysqli_real_escape_string($conn, $name);
$ip = mysqli_real_escape_string($conn, $ip);

$name = str_replace( array_keys( $substitutions ), $substitutions, $name );
$ip = str_replace( array_keys( $substitutions ), $substitutions, $ip ); 

if (stripos ($name, "<script") !== false) {

	backPage("match attack keywords:script!");
    } 

if($name == "" || $ip==""){

	backPage("need both input!!");
	
}
else{
	echo "Login Success:"."<br>";
	echo $name."<br>";
	echo $ip."<br><br>";

}




checkUser($conn,$name);

if(!$check = checkUser($conn,$name)){
        backPage("username is already used");
}
else{
	echo "OK DUKE , ";
	writeData($conn,$name,$ip);
	echo "=================================="."<br>";
//	readData($conn);
}

//testme
$cmd = shell_exec('ping -c 2 '.$ip);
echo "test your ip address:{$cmd}"."<br><br>";
//testme


//End anything
mysql_close($conn);
unset($_SESSION['session_token']);
?>

<html>
 <head><title>Login Page</title>
     <table border="1" style="color:purple;font-family:Microsoft JhengHei;">
         <tr>
      <?php
                readData($conn);
     ?>
         </tr>
      </table>

    </head>
</html>
