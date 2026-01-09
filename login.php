<?php
session_start();
require 'db.php';

if (isset($_POST['login'])) { 
    $user = $_POST['user']; 
    $pass = $_POST['pass']; 

    $sql = "SELECT * FROM user WHERE user = '$user' AND pass = '$pass'"; 
    
    // ĐÃ XÓA DÒNG ECHO <BR> Ở ĐÂY ĐỂ TRÁNH LỖI HEADER
    
    $result = $conn->query($sql);

    if ($result && $result->num_rows > 0) {
        $_SESSION['user'] = $user;
        header("Location: edit.php");
        exit(); // Luôn dùng exit sau header chuyển hướng
    } else {
        echo "Tên đăng nhập hoặc mật khẩu không đúng!";
    }
} // ĐÂY LÀ DẤU ĐÓNG NGOẶC BỊ THIẾU
?>