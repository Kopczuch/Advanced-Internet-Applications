<?php require_once 'functions.php'; ?>

<?php

if (isset($_POST["Name"], $_POST["Salary"], $_POST["Occupation"], $_POST["Hire_Date"]) and
    !empty($_POST["Name"]) and !empty($_POST["Salary"]) and !empty($_POST["Occupation"]) and !empty($_POST["Hire_Date"]) and
    is_numeric($_POST["Salary"]))
{
    insert_data($_POST["Name"], $_POST["Salary"], $_POST["Occupation"], $_POST["Hire_Date"]);
    header('Location: http://localhost:8080');
}
else
{
    if (empty($_POST["Name"]))
    {
        echo '<script>alert("Empty Name field!")</script>';
    }
    else if (empty($_POST["Salary"]))
    {
        echo '<script>alert("Empty Salary field!")</script>';
    }
    else if (empty($_POST["Occupation"]))
    {
        echo '<script>alert("Empty Occupation field!")</script>';
    }
    else if (empty($_POST["Hire_Date"]))
    {
        echo '<script>alert("Empty Hire Date field!")</script>';
    }
    ?>
        <div class="alert alert-danger" role="alert">
            <h3>
                Insertion failed!
            </h3>
        </div>
    <?php
}

?>