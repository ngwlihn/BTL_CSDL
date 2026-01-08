<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Document</title>
</head>

<body>
    <h1>Đăng nhập</h1>
    <form action="login.php" method="POST">
        Tên đăng nhập: <input type="text" name="user" required> <br>
        Mật khẩu: <input type="password" name="pass" required> <br>
        <button type="submit" name="login">Đăng nhập</button>
    </form>
<br>
<form action="regis.php" method="get">
    <button type="submit">Đăng ký ngay</button>
</form>
</body>
</html>
