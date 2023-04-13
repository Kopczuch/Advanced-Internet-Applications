
<?php
    require_once 'functions.php';
    include 'inputheader.php';

    

    if (isset($_POST['user'], $_POST['tag']) and
        !empty($_POST['user']) and !empty($_POST['tag']))
    {
        $userId = $_POST['user'];
        $movieId = $_POST['form-id'];
        $tag = $_POST['tag'];
        $timestamp = time(); // set the current timestamp

        add_tag($userId, $movieId, $tag, $timestamp);
        header('Location: http://localhost:8080/index.php');
    }
    else
    {
        $id = $_GET['id'];
        $users = get_all_users(); ?>
        
        <div class="container">
            <div class="row justify-content-center align-items-center g-2">
                <div class="col-8"> 
                        <form action="addtag.php" method="post">
                        <div class="mb-3">
                            <label for="" class="form-label">MovieID</label>
                            <input type="text" class="form-control" name="form-id" id="form-id" aria-describedby="helpId" placeholder="" value="<?php echo $id ?>" readonly>
                        </div>
                        <div class="mb-3">
                            <label for="" class="form-label">User</label>
                            <select class="form-control" name="user" id="user">
                            <?php while($user = mysqli_fetch_assoc($users)): ?>
                                <option value="<?php echo $user['userid']; ?>">
                                <?php echo $user['nickname']; ?>
                                </option>
                            <?php endwhile; ?>
                            </select>
                        </div>
                        <div class="mb-3">
                            <label for="" class="form-label">Tag</label>
                            <input type="text"
                            class="form-control" name="tag" id="tag" aria-describedby="tagId" placeholder="" required>
                        </div>
                        <button type="submit" class="btn btn-primary" name="addtag">Add</button>
                        </form>
                </div>
            </div>
        </div>
        <?php
    }

    include("footer.php");
?>