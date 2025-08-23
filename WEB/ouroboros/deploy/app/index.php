<?php 

require_once("config.php");

if(isset($_GET['pw'])){
    $id = $_GET['id'];
    $pw = $_GET['pw'];

    if ( !preg_match("/^[A-Za-z_]+$/is", $id) ){ die("hack!"); }
    if ( preg_match("/,/is", $pw) ){ die("hack!"); }
    if ( $_GET['id'] == '' || $_GET['pw'] == '' ) { die("empty value"); }

    $query = $conn->query("SELECT upw FROM users WHERE uid='$id' and upw='$pw';");
    $result = $query->fetch_assoc();

    if($pw === $result['upw']) { echo $flag; }
    else { echo "empty!"; }
}

highlight_file(__FILE__);

?>

