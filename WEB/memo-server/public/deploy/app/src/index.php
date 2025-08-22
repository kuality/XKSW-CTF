<!DOCTYPE html>
<html lang="ko">
<head>
    <meta charset="UTF-8">
    <meta http-equiv="X-UA-Compatible" content="IE=edge">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <link rel="stylesheet" type="text/css" href="/static/css/index.css">
    <title>Document</title>
</head>
<body>
    <a href="/viewer.php">viewer</a>

    <form method="GET" action="/viewer.php">
        title : <input type="text" name="title"><br>
        contents : <input type="text" name="contents"><br>
        by : <input type="text" name="by"><br>
        <input type="submit" name="submit">
    </form>

</body>
</html>