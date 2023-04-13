<?php
    $serverAddr = "localhost";
    $username = "root";
    $password = "";
    $dbName = "MovieLens";

    $conn = mysqli_connect($serverAddr, $username, $password, $dbName);

    if (!$conn)
    {
        die("Connection error".mysqli_connect_error());
    }
?>