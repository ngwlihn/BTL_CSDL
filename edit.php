<?php
session_start();
//echo  session_id();
echo $_SESSION['user'];
?>
<h1> Chào mừng bạn đến với trang web của chúng tôi </h1> <br>

<form action="edit.php" method="post">
    <h3>Chỉnh sửa thông tin</h3><br>
    Mật khẩu hiện tại: <input type="password" name="pass" require><br>
    Mật khẩu mới: <input type="password" name="newpass" require><br>
    Họ tên mới: <input type="text" name="name" require><br>
    <button type="submit" name ="edit">Xác nhận</button><br>
</form>

<form action="edit.php" method ="post" enctype="multipart/form-data">
    <input type="file" name="img" >
    <button type="submit" name="upload">Gửi</button>
</form>

<form action="edit.php" method ="post" >
    <button type="submit" name="logout"> Đăng xuất </button>
</form>

<?php
require 'db.php';
if (isset($_SESSION['user'])){
	
if (isset($_POST['edit'])){
    $user=$_SESSION['user'];
    $pass=$_POST['pass'];
    $newpass=$_POST['newpass'];
    $name=$_POST['name'];
	echo "$user <br>";
	//echo  session_id();
    $sql= "SELECT * FROM user WHERE user='$user' AND pass= '$pass'";
    $r=$conn->query($sql);
    if ($r->num_rows >0){
        $new="UPDATE user SET pass='$newpass', name='$name' WHERE user='$user' ";
        $conn->query($new);
        echo "Chỉnh sửa thành công! <br>";
    }
    else {
        echo "Mật khẩu không đúng";
    }
}

// Tai anh
$target_dir ="./uploads/";// thu muc luu anh
$target_file = $target_dir . basename($_FILES["img"]["name"]); // duong dan cua anh dc tai len

$image = strtolower(pathinfo($target_file,PATHINFO_EXTENSION)); // chuyen phan mo rong cua anh ve chu thuong

if (isset($_POST['upload'])) {
	// Kiem tra xem file upload cp phai anh khong
    $check = getimagesize($_FILES["img"]["tmp_name"]);
  //  print_r ($check);
    if($check !== false) {
		if(move_uploaded_file($_FILES['img']["tmp_name"], $target_file)){
			echo "Tai len thanh cong";
			echo  $target_file; }
		else {
			echo "Loi roi";
		}
    }
    else {
    	echo "Ảnh không hợp lệ!";
    }
}
if (isset($_POST['logout'])){
	header("Location: index.php");
	exit();
}
}
//else {
//	header("Location:index.php");
//	exit();
//}
?>
