<?php
session_start();
//echo  session_id();
require 'db.php';
if (isset($_POST['login'])) { // nếu nhấn đăng nhập
$user = ($_POST['user']); // gán
$pass = ($_POST['pass']); //  htmlspecialchars : encode input tu user

$sql = "SELECT * FROM user WHERE user = '$user' AND pass = '$pass'"; // lấy dữ liệu
//print_r($sql);
echo "<br>";
$result = $conn->query($sql);
if ($result->num_rows > 0) {
	$_SESSION['user']=$user;
	header("Location: edit.php");
	exit();
	}
else {
 echo "Tên đăng nhập hoặc mật khẩu không đúng!";
  }
?>