<?php require_once 'db_connection.php';

function get_all_movies()
{
    global $conn;
    if ($result = $conn -> query("SELECT * FROM Movies ORDER BY movieId DESC LIMIT 21"))
    {
        while($row = mysqli_fetch_assoc($result))
        {
            ?>
                <div class="col-4      ">
                    <div class="card border-primary">
                      <div class="card-body">
                        <h5 class="card-title">
                            <?php echo ($row["title"])?>
                        </h5>
                        <p class="card-text">
                            <?php echo ($row["genres"])?>
                        </p>
                        <a name="" id="" class="btn btn-success" href="viewratings.php?id=<?php echo($row["movieId"]) ?>" role="button">Ratings</a>
                        <a name="" id="" class="btn btn-secondary ml-auto" data-bs-toggle="collapse" href="#collapseTags-<?php echo $row["movieId"] ?>" role="button" aria-expanded="false" aria-controls="collapseTags-<?php echo $row["movieId"] ?>">Tags</a>
                        <a name="" id="" class="btn btn-primary" href="editmovie.php?id=<?php echo($row["movieId"]) ?>" role="button">Update</a>
                        <a name="" id="" class="btn btn-danger" href="deletemovie.php?id=<?php echo($row["movieId"]) ?>" role="button">Delete</a>

                                <div class="collapse mt-2" id="collapseTags-<?php echo $row["movieId"] ?>">
                                    <div class='d-flex gap-1 flex-wrap '>
                                        <?php echo get_tags($row["movieId"])?>
                                    </div>
                                </div> 
                      </div>
                    </div>
                </div>
            <?php
        }
        $result -> free_result();
    }
    $conn -> close();
}

function get_one_movie($id){
    global $conn;
    $sql = "SELECT * FROM movies WHERE movieId=$id";
    $result = mysqli_query($conn,$sql);
    $row = mysqli_fetch_assoc($result);
    return $row;
}

function add_movie($title, $genres)
{
    global $conn;
    $sql = "INSERT INTO Movies (title, genres)
    VALUES ('$title', '$genres')";
    if ($conn -> query($sql) === TRUE)
    {
        echo "New movie successfully added";
    }
    else
    {
        echo "Error: " . $sql . "<br>" . $conn->error;
    }
}


function update_movie($id, $title, $genres){
    global $conn;
    $sql = "UPDATE movies SET title='$title', genres='$genres' WHERE movieId='$id'";
    mysqli_query($conn,$sql);
    header('Location: http://localhost:8080/index.php');
}

function delete_movie($id)
{
    global $conn;
    $sql = "DELETE FROM Movies WHERE movieId = '$id'";
    if ($conn->query($sql) === TRUE)
    {
        echo "Movie deleted successfully";
    }
    else
    {
        echo "Error: " . $sql . "<br>" . $conn->error;
    }
    $sql = "DELETE FROM Ratings WHERE movieId = '$id'";
    mysqli_query($conn, $sql);

    $sql = "DELETE FROM Tags WHERE movieId = '$id'";
    mysqli_query($conn, $sql);
}

function get_tags($id){
    global $conn;
    $sql = "SELECT userId, movieId, tag FROM tags WHERE movieId = '$id'";
    $result = mysqli_query($conn,$sql);
    
    while($row = mysqli_fetch_assoc($result)){
        ?>
                <button type="button" class="btn btn-info"><?php echo($row["tag"]) ?></button>
        <?php
    }
    ?>
            <a name="" id="" class="btn btn-success" href="managetags.php?id=<?php echo $id ?>" role="button">Manage tags</a>
    <?php
}

function add_tag($userId, $movieId, $tag, $timestamp)
{
    global $conn;
    $sql = "INSERT INTO Tags (userId, movieId, tag, timestamp)
    VALUES ('$userId', '$movieId', '$tag', '$timestamp')";
    if ($conn -> query($sql) === TRUE)
    {
        echo "New tag successfully added";
    }
    else
    {
        echo "Error: " . $sql . "<br>" . $conn->error;
    }
}

function delete_tag($userId, $movieId, $tag)
{
    global $conn;
    $sql = "DELETE FROM Tags WHERE userId = '$userId' AND movieId = '$movieId' AND tag = '$tag'";
    if ($conn->query($sql) === TRUE)
    {
        echo "Tag deleted successfully";
    }
    else
    {
        echo "Error: " . $sql . "<br>" . $conn->error;
    }
} 

function view_tags($id)
{
    global $conn;
    $sql = "SELECT tags.*, users.nickname, movies.title FROM tags
        INNER JOIN users ON users.userid = tags.userId
        INNER JOIN movies ON tags.movieId = movies.movieId
        WHERE tags.movieId = $id";
    $result = mysqli_query($conn, $sql);
    return $result;
}

function insert_new_user($name) {
    global $conn;

    $sql = "SELECT * FROM users WHERE nickname = '$name'";
    $result = mysqli_query($conn, $sql);

    if (mysqli_num_rows($result) > 0) {
        session_start();
        $_SESSION['error_message'] = "Nickname already exists in the database.";
    } else {
        $sql = "INSERT INTO users (nickname) VALUES ('$name')";
        mysqli_query($conn, $sql);
    }
    header('Location: http://localhost:8080/index.php#users');
    exit();
}

function get_movie_ratings($id){
    global $conn;
    $sql = " SELECT ratings.*, users.nickname, movies.title
    FROM ratings
    INNER JOIN users ON ratings.userId = users.userid
    INNER JOIN movies ON ratings.movieId = movies.movieId
    WHERE ratings.movieId = $id ";
    $result = mysqli_query($conn, $sql);
    return $result;
}

function get_all_users(){
    global $conn;
    $sql = " SELECT * FROM users";
    $result = mysqli_query($conn, $sql);
    return $result;
}
function add_rating($movieid, $userid, $rating, $timestamp){
    global $conn;
    $sql = "INSERT INTO ratings (movieid, userid, rating, timestamp) VALUES ('$movieid', '$userid', '$rating', '$timestamp')";
    mysqli_query($conn, $sql);
    header('Location: http://localhost:8080/index.php');
}

?>