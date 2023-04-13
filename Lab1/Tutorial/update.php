<?php
    require_once 'functions.php';
    $id = $_GET["id"];
?>

<!doctype html>
<html lang="en">
<head>
  <title>Update employee</title>
  <!-- Required meta tags -->
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1, shrink-to-fit=no">

  <!-- Bootstrap CSS v5.2.1 -->
  <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.2.1/dist/css/bootstrap.min.css" rel="stylesheet"
    integrity="sha384-iYQeCzEYFbKjA/T2uDLTpkwGzCiq6soy8tYaI1GyVh/UjpbCx/TYkiZhlZB6+fzT" crossorigin="anonymous">
</head>

<body>
    <div>
        <h3  style="text-align:center;">
            Update Employee #
            <?php
                echo $id;
            ?> 
        <h3>
    </div>

<?php
    global $conn;
    if ($result = $conn -> query("SELECT * FROM Employees WHERE id = $id"))
    {
        while ($row = mysqli_fetch_assoc($result))
        {
?>
            <div class="container">
                <div class="row justify-content-center align-items-center g-2">
                    <div class="col-8      ">
                    <form action="update.php?id=<?php echo($row["id"])?>" method="post">
                        <input type="hidden" name="id"  value=<?php echo $id ?>>
                        <div class="mb-3">
                            <label for="" class="form-label">Name</label>
                            <input type="text"
                                class="form-control" name="Name" id="nameInput" aria-describedby="helpId" placeholder="" value=<?php echo $row["name"]?>>
                            <small id="helpId" class="form-text text-muted"></small>
                        </div>
                        <div class="mb-3">
                            <label for="" class="form-label">Salary</label>
                            <input type="number"
                                class="form-control" name="Salary" id="salaryInput" aria-describedby="helpId" placeholder="" value=<?php echo $row["salary"]?>>
                            <small id="helpId" class="form-text text-muted"></small>
                        </div> 
                        <div class="mb-3">
                            <label for="" class="form-label">Occupation</label>
                            <input type="text"
                                class="form-control" name="Occupation" id="occupationInput" aria-describedby="helpId" placeholder="" value=<?php echo $row["occupation"]?>>
                            <small id="helpId" class="form-text text-muted"></small>
                        </div> 
                        <div class="mb-3">
                            <label for="" class="form-label">Hire Date</label>
                            <input type="date"
                                class="form-control" name="Hire_Date" id="hireDateInput" aria-describedby="helpId" placeholder="" value=<?php echo $row["hire_date"]?>>
                            <small id="helpId" class="form-text text-muted"></small>
                        </div>
                            <button type="submit" class="btn btn-primary">Submit</button>
                            <a name="" id="" class="btn btn-secondary" href="http://localhost:8080/" role="button">Cancel</a>
                        </form>
                    </div>
                </div>
            </div>
<?php
        }
        $result -> free_result();
    }

    if (isset($_POST["Name"], $_POST["Salary"], $_POST["Occupation"], $_POST["Hire_Date"]) and
    !empty($_POST["Name"]) and !empty($_POST["Salary"]) and !empty($_POST["Occupation"]) and !empty($_POST["Hire_Date"]) and
    is_numeric($_POST["Salary"]))
    {
        update_data($_POST['id'], $_POST['Name'], $_POST['Salary'], $_POST['Occupation'], $_POST['Hire_Date']);
        header('Location: http://localhost:8080');
    }

?>
    


<?php include ("footer.php")?>