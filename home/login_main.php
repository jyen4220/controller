<?php
session_start();

$_SESSION[ 'session_login_Token' ] = md5( uniqid() );


?>

<!DOCTYPE HTML>
<!--
	Urban by TEMPLATED
	templated.co @templatedco
	Released for free under the Creative Commons Attribution 3.0 license (templated.co/license)
-->
<html>
	<head>
		<link rel="Shortcut Icon" type="image/x-icon" href="images/pic02.jpg" />
		<title>JNS Production</title>
		<meta charset="utf-8" />
		<meta name="viewport" content="width=device-width, initial-scale=1" />
		<link rel="stylesheet" href="assets/css/main.css" />

	</head>
	<body class="subpage">



		<!-- Header -->
			<header id="header">
				<div class="logo"><a href="index.html">JNS Production <span>by JYEN Chen</span></a></div>
				<a href="#menu">Menu</a>
			</header>

		<!-- Nav -->
			<nav id="menu">
<span style="color:write;"><?php

if($_SESSION['session_success']!="") echo "======\tWelcome !\t".$_SESSION['session_success']."\t======<br>";//.$_SESSION[ 'session_user_Token' ]."<br>";
									?></span>
				<ul class="links">
					<li><a href="index.php">Home</a></li>
					<li><a href="about.php">關於我們</a></li>
					<li><a href="gallery.php">展示</a></li>
					<li><a href="generic.php">註冊</a></li>

					<li><a href="login_main.php" id="mylink" onclick="f1()"><p id="userid">登入</p>
<script>
	function f1() {

		if(document.getElementById("userid").innerText=="登入"){
			return true;
			}else

    		document.getElementById("mylink").href="login_out.php"; 
    		return false;
  	};
    var jsuser = '<?php if($_SESSION['session_success']!=""){echo "登出";}else echo "登入"; ?>'; 
    
    document.getElementById("userid").innerText = jsuser;
     
</script></a></li>
					<li><a href="elements.html">Elements</a></li>

				</ul>
			</nav>

		<!-- Main -->
			<div id="main">

				<!-- Section -->
					<section class="wrapper">
						<div class="inner">
							<header class="align-center">
								<h1>登入頁面</h1>

							</header>
							<div class="flex flex-2">
								<div class="col col2">
									 

									<span style="color:red;"><?php

										echo $_SESSION['alert_login'];
 
										unset($_SESSION['alert_login']);
									?>
									</span>
									<form method="POST" action="http://www.jnsproduction.tw/login_page.php">

										Email<input type="text" name="content_10" size="16"><br><br>
										Password<input type="password" name="content_11" size="16"><br><br>
										<input type='hidden' name='user_token' value="<?php echo $_SESSION[ 'session_login_Token' ]; ?>" />
										<input type="submit" value="login" name="button_1">
								</div>
								
							</div>
 

						</div>
					</section>

				<!-- Section -->
					<section class="wrapper style1">
						<div class="inner">
							<header class="align-center">
								<h2>More Services</h2>
								<p>============================================================</p>
							</header>
							<div class="flex flex-3">
								<div class="col align-center">
									<div class="image round fit">
										<img src="images/pic03.jpg" alt="" />
									</div>
									<p>Test Your PC Now ! ! ! </p>
									<a href="http://www.jnsproduction.tw/index_pc.php" class="button" target=_blank>Learn More</a>
								</div>
								<div class="col align-center">
									<div class="image round fit">
										<img src="images/pic05.jpg" alt="" />
									</div>
									<p>Add our LINE Group to get more information </p>
									<a href="#main" class="button">Learn More</a>
								</div>
								<div class="col align-center">
									<div class="image round fit">
										<img src="images/pic04.jpg" alt="" />
									</div>
									<p>簡易詢問管道</p>
									<a href="https://docs.google.com/forms/d/e/1FAIpQLSdSohQWQAKKKDBnV6h8l4mtcojQY6coALIq0bWKdf-oS2aLAg/viewform?usp=sf_link" class="button" target=_blank>Learn More</a>
								</div>
							</div>
						</div>
					</section>

			</div>

		<!-- Footer -->
			<footer id="footer">
				<div class="copyright">
					<ul class="icons">
						<li><a href="#" class="icon fa-twitter"><span class="label">Twitter</span></a></li>
						<li><a href="#" class="icon fa-facebook"><span class="label">Facebook</span></a></li>
						<li><a href="#" class="icon fa-instagram"><span class="label">Instagram</span></a></li>
						<li><a href="#" class="icon fa-snapchat"><span class="label">Snapchat</span></a></li>
					</ul>
					<p>&copy; Untitled. All rights reserved. Design: <a href="https://templated.co">TEMPLATED</a>. Images: <a href="https://unsplash.com">Unsplash</a>.</p>
				</div>
			</footer>

		<!-- Scripts -->
			<script src="assets/js/jquery.min.js"></script>
			<script src="assets/js/jquery.scrolly.min.js"></script>
			<script src="assets/js/jquery.scrollex.min.js"></script>
			<script src="assets/js/skel.min.js"></script>
			<script src="assets/js/util.js"></script>
			<script src="assets/js/main.js"></script>

	</body>
</html>
