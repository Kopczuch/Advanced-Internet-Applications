<?php
    require_once("functions.php");
    include("inputheader.php");
    $id = $_GET['id'];
    $result = view_tags($id);

?>

<div class="container">
  <div class="row">
    <?php while($row = mysqli_fetch_assoc($result)): ?>
      <div class="col-md-4 mb-4">
        <div class="card">
          <div class="card-body">
            <h5 class="card-title"><?= $row['nickname'] ?></h5>
            <p class="card-text"><strong><?= $row['title'] ?></strong></p>
            <p class="card-text">Tag: <?= $row['tag'] ?></p>
            <p class="card-text"><small class="text-muted">Date: <?php echo date('Y-m-d H:i:s', $row['timestamp']); ?></small></p>
          </div>
          <div class="card-footer">
            <a href="deletetag.php?user=<?php echo $row['userId']; ?>&movie=<?php echo $row['movieId']; ?>&tag=<?php echo $row['tag']; ?>" class="btn btn-danger">Delete Tag</a>
          </div>
        </div>
      </div>
    <?php endwhile; ?>
  </div>
  <div class="row">
    <div class="col text-center">
        <a href="index.php" class="btn btn-secondary">Back to Home</a>
        <a href="addtag.php?id=<?php echo $id; ?>" class="btn btn-primary">Add Tag</a>
        <br/>
        <br/>
    </div>
  </div>
</div>

<?php include("footer.php") ?>