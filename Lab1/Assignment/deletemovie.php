<?php
    require_once 'functions.php';
    $id = $_GET["id"];
    delete_movie($id);
    header('Location: http://localhost:8080');
?>