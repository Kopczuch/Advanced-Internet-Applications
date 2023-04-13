<?php
require_once("functions.php");
include("inputheader.php");

if(isset($_POST['newrating'])) {
    $movieid = $_POST['form-id'];
    $userid = $_POST['user'];
    $rating = $_POST['rating'];
    $timestamp = time(); // set the current timestamp
    
    add_rating($movieid, $userid, $rating, $timestamp);

}else{
    $id = $_GET['id'];
    $users = get_all_users();
    ?>
    <div class="container">
      <div class="row justify-content-center align-items-center g-2">
        <div class="col-8"> 
                <form action="newrating.php" method="post">
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
                    <label for="" class="form-label">Rating</label>
                    <select class="form-control" name="rating" id="rating">
                    <?php for($i=2; $i<=10; $i++): ?>
                        <option value="<?php echo $i/2; ?>">
                        <?php echo $i/2; ?>
                        </option>
                    <?php endfor; ?>
                    </select>
                </div>
                <button type="submit" class="btn btn-primary" name="newrating">Add</button>
                </form>


        </div>
      </div>
<?php }
include("footer.php"); ?>