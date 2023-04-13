<?php require_once 'db_connection.php';

function get_all_data()
{
    global $conn;
    if ($result = $conn -> query("SELECT * FROM employees"))
    {
        while($row = mysqli_fetch_assoc($result))
        {
            ?>
                <div class="col-4      ">
                    <div class="card border-primary">
                      <div class="card-body">
                        <h4 class="card-title">
                            <?php echo ($row["name"])?>
                        </h4>
                        <p class="card-text">
                            <?php echo ($row["occupation"])?>
                        </p>
                        <p class="card-text">
                            <?php echo ($row["salary"])?>
                        </p>
                        <p class="card-text">
                            <?php echo ($row["hire_date"])?>
                        </p>
                        <a name="" id="" class="btn btn-primary" href="update.php?id=<?php echo($row["id"])?>" role="button">Update</a>
                        <a name="" id="" class="btn btn-danger" href="delete.php?id=<?php echo($row["id"])?>" role="button">Delete</a>
                      </div>
                    </div>
                </div>
            <?php
        }
        $result -> free_result();
    }

    $conn -> close();
}

function insert_data($name, $salary, $occupation, $hire_date)
{
    global $conn;
    $sql = "INSERT INTO employees (name, occupation, hire_date, salary)
    VALUES ('$name', '$occupation', '$hire_date', '$salary')";
    if ($conn->query($sql) === TRUE)
    {
        echo "New record created successfully";
    }
    else
    {
        echo "Error: " . $sql . "<br>" . $conn->error;
    }
}

function update_data($id, $name, $salary, $occupation, $hire_date)
{
    global $conn;
    $sql = "UPDATE Employees SET
    name = '$name',
    salary = '$salary',
    occupation = '$occupation',
    hire_date = '$hire_date'
    WHERE id = '$id'";
    if ($conn->query($sql) === TRUE)
    {
        echo "Record updated successfully";
    }
    else
    {
        echo "Error: " . $sql . "<br>" . $conn->error;
    }
}

function delete_data($id)
{
    global $conn;
    $sql = "DELETE FROM Employees WHERE id = '$id'";
    if ($conn->query($sql) === TRUE)
    {
        echo "Record deleted successfully";
    }
    else
    {
        echo "Error: " . $sql . "<br>" . $conn->error;
    }
}

?>