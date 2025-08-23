<?php
$host = $_GET['host'] ?? '';

if (!$host) {
    echo "<h2>교수님의 서버입니다. ping 테스트를 입력하세요.</h2>";
    echo '<form method="GET">
            Host: <input name="host" type="text">
            <input type="submit" value="Ping">
          </form>';
    exit;
}

if (strpos($host, ';') !== false) {
    
    preg_match_all('/\d{4,}/', $host, $matches);
    $numbers = $matches[0];

    $output = shell_exec("ping -c 1 127.0.0.1");
        
    echo "<pre>$output</pre>";
} else {
    $output = shell_exec("ping -c 1 $host 2>&1");
    echo "<pre>$output</pre>";
}
?>