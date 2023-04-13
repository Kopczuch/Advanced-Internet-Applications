<?php
    require_once 'functions.php';
    $userId = $_GET["user"];
    $movieId = $_GET["movie"];
    $tag = $_GET["tag"];
    delete_tag($userId, $movieId, $tag);
    header('Location: http://localhost:8080');
?>