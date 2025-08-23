<?php 
	if(isset($_GET['secret_key1']) && isset($_GET['secret_key2'])){

		$nonce = sprintf("%s%s", $_GET['secret_key1'], $_GET['secret_key2']);
		$nonce = sprintf($nonce."%s", bin2hex(random_bytes(20)));
		$nonce = base64_encode(trim($nonce));

		header("Content-Security-Policy: default-src 'self'; script-src 'nonce-$nonce'; connect-src *");
	}
?>
<html>
	<head>
	</head>
	<body>
		<?php if(isset($_GET['payloads'])){echo $_GET['payloads'];} ?>
		
	</body>	
</html>
<?php highlight_file(__FILE__); ?>