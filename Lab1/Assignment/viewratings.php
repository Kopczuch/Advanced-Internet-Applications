<?php
require_once("functions.php");
include("inputheader.php");
$id = $_GET['id'];
$result = get_movie_ratings($id);

?>

<div class="container">
  <div class="row">
    <?php while($row = mysqli_fetch_assoc($result)): ?>
      <div class="col-md-4 mb-4">
        <div class="card">
          <div class="card-body">
            <h5 class="card-title"><?= $row['nickname'] ?></h5>
            <p class="card-text"><strong><?= $row['title'] ?></strong></p>
            <p class="card-text">Rating: <?= $row['rating'] ?></p>
            <p class="card-text"><small class="text-muted">Date: <?php echo date('Y-m-d H:i:s', $row['timestamp']); ?></small></p>
          </div>
          <div class="card-footer">
            <small class="text-muted">Submitted by <?= $row['nickname'] ?></small>
          </div>
        </div>
      </div>
    <?php endwhile; ?>
  </div>
  <div class="row">
    <div class="col text-center">
      <a href="index.php" class="btn btn-secondary">Back to Home</a>
      <a href="newrating.php?id=<?php echo $id; ?>" class="btn btn-primary">Add Rating</a>
      <br/>
      <br/>
    </div>
  </div>
</div>

<?php include("footer.php") ?>