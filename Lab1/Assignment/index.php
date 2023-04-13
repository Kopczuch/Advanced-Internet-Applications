<?php include("header.php");
session_start(); ?>
<?php require_once 'functions.php'; ?>
    <main>
        <div class="tab-content">
        <?php
                        
        if (isset($_SESSION['error_message'])) {
            echo '<div class="alert alert-danger" role="alert">' . $_SESSION['error_message'] . '</div>';
             unset($_SESSION['error_message']);
                        }
        ?>
        <div class="tab-pane active" id="movies" role="tabpanel" aria-labelledby="movies-tab">
            <div class="container">
                <div class="row justify-content-center align-items-center g-2">
                    <?php get_all_movies() ?>
                </div>
            </div>
        </div>
        
        <div class="tab-pane" id="new-movie" role="tabpanel" aria-labelledby="new-movie-tab">
            <div class="container mt-3">
                <form action="addmovie.php" method="post">
                    <div class="mb-3">
                        <label for="title" class="form-label">Title</label>
                        <input type="text"
                            class="form-control" name="title" id="title" aria-describedby="titleId" placeholder="" required>
                    </div>

                    <div class="mb-3">
                        <label for="genres" class="form-label">Genres</label>
                        <input type="text"
                            class="form-control" name="genres" id="genres" aria-describedby="genresId" placeholder="" required>
                    </div>

                    <button type="submit" class="btn btn-primary">Submit</button> 
                </form>
            </div>
        </div>
        
        <div class="tab-pane" id="users" role="tabpanel" aria-labelledby="users-tab">
            <div class="container mt-3">
                <form action="newuser.php" method="post">
                    <div class="mb-3">
                        <label for="user-name" class="form-label">User Name</label>
                        <input type="text"
                            class="form-control" name="user-name" id="user-name" aria-describedby="user-nameId" placeholder="" required>
                        <small id="user-nameId" class="form-text text-muted">Nickname</small>
                    </div>
                    <button type="submit" class="btn btn-primary">Submit</button>
                </form>
            </div>
        </div>
        </div>
    </main>
<?php include("footer.php") ?>