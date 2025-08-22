<?php  

$PATH = $_SERVER["PHP_SELF"];

if(substr($PATH, strlen($PATH)-1) == '/'){
	exit("no hack");
}

function security($msg, $level = 1){
	if($level == 1){
		if(preg_match('/frame|on|script/i', $msg)){
			exit("no hack!");
		}else{
			return $msg;
		}
	}elseif($level == 2){
		return preg_replace("/<|>/i", "", $msg);
	}else{
		return $msg;
	}
}

?>