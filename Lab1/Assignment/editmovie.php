<?php
require_once("functions.php");
include("inputheader.php");

if(isset($_POST['update'])) {
    $id = $_POST['form-id'];
    $title = $_POST['form-title'];
    $genres = $_POST['form-genres'];
    update_movie($id,$title,$genres);

}else{
    $id = $_GET['id'];
    $row = get_one_movie($id);

    
    ?>
    <div class="container">
      <div class="row justify-content-center align-items-center g-2">
        <div class="col-8"> 
          <form action="editmovie.php" method="post">
              <div class="mb-3">
                <label for="" class="form-label">MovieID</label>
                <input type="text" class="form-control" name="form-id" id="form-id" aria-describedby="helpId" placeholder="" value="<?php echo $row['movieId']; ?>" readonly>
              </div>
              <div class="mb-3">
                <label for="" class="form-label">Title</label>
                <input type="text" class="form-control" name="form-title" id="form-title" aria-describedby="helpId" placeholder="" value="<?php echo $row['title']; ?>">
              </div>
              <div class="mb-3">
                <label for="" class="form-label">Genres</label>
                <input type="text"
                  class="form-control" name="form-genres" id="form-genres" aria-describedby="helpId" placeholder=""
                  value="<?php echo $row['genres']; ?>" >
              </div>
              
              <a href="index.php" class="btn btn-secondary">Cancel</a>
              <button type="submit" class="btn btn-primary" name="update">Update</button>


          </form>

        </div>
      </div>
<?php }
include("footer.php"); ?>