<?php require_once 'functions.php'; ?>
<?php include 'header.php'; ?>

<?php

    if (isset($_POST["title"], $_POST["genres"]) and !empty($_POST["title"]) and !empty($_POST["genres"]))
    {
        add_movie($_POST["title"], $_POST["genres"]);
        header('Location: http://localhost:8080/index.php');
    }
    else
    {
        if (empty($_POST["title"]))
        {
            echo '<scrpit>alert("Empty Title field!")</scrpit>';
        }
        else if (empty($_POST["genres"]))
        {
            echo '<scrpit>alert("Empty Genres field!")</scrpit>';
        }
    }

?>

<?php include("footer.php"); ?> 