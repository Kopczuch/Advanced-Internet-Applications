<?php 
    include("functions.php");

    if (isset($_POST["user-name"]) 
        and !empty($_POST["user-name"])) {
  
            insert_new_user($_POST["user-name"]);
            
    } 
?>