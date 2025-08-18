<?php include("security.php"); ?>
<!DOCTYPE html>
<html>
<head>
	<meta charset="utf-8">
	<meta name="viewport" content="width=device-width, initial-scale=1">
	<script type="text/javascript" src="static/js/browser.js"></script>
	<link rel="stylesheet" type="text/css" href="static/css/view.css">
	<title>viewer</title>
</head>
<body>

	<?php 

		$GET_METHOD = (isset($_GET["title"]) && isset($_GET["contents"]) && isset($_GET["by"]) && isset($_GET["submit"]));

		if($GET_METHOD){

	?>

	<div class="card">

		<center>
			<h1><?php echo security($_GET["title"], $level=2); ?></h1>
		</center>

		<center>
			<p><?php echo security($_GET["contents"]); ?></p>
		</center>

		<span class="by">by : <?php echo security($_GET["by"], $level=2); ?></span>

	</div>
	<?php 

		}else{
			?><a href="/index.php">bad request.</a><?php
		}
	 

	?>

	<script type="text/javascript">
		
		if(window.browser.useragent && window.browser.useragent.toString().indexOf("Trident") != -1){
			window.location.href = window.browser.ChromeDownloadURL
		}


	</script>
</body>
</html>