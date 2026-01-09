<form action="regis.php" method="post">
    Họ và tên: <input type="text" name="name"required> <br>
    Tên đăng nhập: <input type="text" name="user"required> <br>
    Mật khẩu: <input type="password" name="pass"required> <br>
    <button type="submit"name ="regis">Đăng ký</button>
</form>
<?php
    require 'db.php'; // Thực hiện các thao tác với cơ sở dữ liệu
    // lay du lieu tu form
   
    if (isset($_POST['regis'])) {
    // echo "helo";
    $user= $_POST['user'];
    $pass= $_POST['pass'];
    $name = $_POST['name'];
    $sm="SELECT user FROM user WHERE user='$user'";
    $check= $conn->query($sm);
    if ($check->num_rows>0){
        echo "Tên đăng nhập đã tồn tại vui lòng đăng kí lại.";
    }
    // 
    else {
        $sql = "INSERT INTO user (user,pass,name) VALUES ('$user','$pass','$name')";
        if ($conn->query($sql)) { // ktra xem insert ok ch
            echo "Đăng kí thành công!<br>";
    }
        else 
            echo "Đăng kí không thành công";
    }
}
?>
<br>
<form action="index.php" method="post" >
    <button type="submit" >Đăng nhập</button>
</form>
