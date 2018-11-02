<?php
session_start();


//if login or register success, we get username with sesion_token(to access other service)--in body




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
	<body>
		<!-- <span style="color:write;"><?php

if($_SESSION['session_success']!="") echo "Welcome !\t".$_SESSION['session_success']."<br>";//.$_SESSION[ 'session_user_Token' ]."<br>";
									?></span> -->
		<!-- Header -->
			<header id="header" class="alt">
				
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

		<!-- Banner -->
			<section id="banner">
				<div class="inner">
					<header>
						<h1>JNS Production</h1>
						<p>去想像 跟著闖</p>
					</header>
					<a href="#main" class="button big scrolly">Learn More</a>
				</div>
			</section>

		<!-- Main -->
			<div id="main">

				<!-- Section -->
					<section class="wrapper style1">
						<div class="inner">
							<!-- 2 Columns -->
								<div class="flex flex-2">
									<div class="col col1">
										<div class="image round fit">
											<a href="https://www.youtube.com/watch?v=HE9gHHvpIoU" class="link" target=_blank><img src="images/pic01.jpg" alt="" /></a>
										</div>
									</div>
									<div class="col col2">
										<h3>5分鐘教你網站攻擊和防禦 ! ! !</h3>
										<p>藉由apache網站平台，讓你了解什麼是 CSRF / MySQL Injection / XSS 網站攻擊，並透過 PHP 程式碼讓你的網站獲得最基本且有效的防禦。</p>
										<a href="https://www.youtube.com/watch?v=HE9gHHvpIoU" class="button" target=_blank>前往觀看影片</a>
									</div>
								</div>
						</div>
					</section>

				<!-- Section -->
					<section class="wrapper style2">
						<div class="inner">
							<div class="flex flex-2">
								<div class="col col2">
									<h3>加入我們</h3>
									<p>了解更多相關資訊，註冊以回覆您的寶貴意見與問題。</p>
									<a href="http://www.jnsproduction.tw/generic.php" class="button">免費會員註冊</a>
								</div>
								<div class="col col1 first">
									<div class="image round fit">
										<a href="http://www.jnsproduction.tw/generic.php" class="link"><img src="images/pic02.jpg" alt="" /></a>
									</div>
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
