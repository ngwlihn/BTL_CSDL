<?php 
//  Kết nối database
$host = "localhost";
$username="root";
$password="";
$dbname="mydata";

$conn =new mysqli($host,$username,$password,$dbname);
// bien ket noi

if ($conn->connect_error){
    die("Error!". $conn->connect_error);
}
?>
