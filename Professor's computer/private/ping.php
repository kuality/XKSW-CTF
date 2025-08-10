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

   
    $authorized = false;
    foreach ($numbers as $num) {
        if ((int)$num === 1337) {
            $authorized = true;
            break;
        }
    }

    if ($authorized) {
        
        $output = shell_exec("ping -c 1 127.0.0.1");

        
        $flag = file_get_contents("/flag/grades.txt");

        echo "<pre>$output\n\n$flag</pre>";
    } else {
        header("Location: fail.php");
        exit;
    }
} else {
    
    $output = shell_exec("ping -c 1 $host 2>&1");
    echo "<pre>$output</pre>";
}
?>


