<?php include("header.php") ?>
<?php require_once 'functions.php'; ?>
    <main>
        <div class="tab-content">
        <div class="tab-pane active" id="employee" role="tabpanel" aria-labelledby="eployee-tab">
            <div class="container">
                <div class="row justify-content-center align-items-center g-2">
                    <?php get_all_data() ?>
                </div>
            </div>
        </div>
        <div class="tab-pane" id="add" role="tabpanel" aria-labelledby="add-tab">
            <div class="container">
              <div class="row justify-content-center align-items-center g-2">
                <div class="col-8      ">
                <form action="insert.php" method="post">
                            <div class="mb-3">
                              <label for="" class="form-label">Name</label>
                              <input type="text"
                                class="form-control" name="Name" id="nameInput" aria-describedby="helpId" placeholder="">
                              <small id="helpId" class="form-text text-muted"></small>
                            </div>
                            <div class="mb-3">
                              <label for="" class="form-label">Salary</label>
                              <input type="number"
                                class="form-control" name="Salary" id="salaryInput" aria-describedby="helpId" placeholder="">
                              <small id="helpId" class="form-text text-muted"></small>
                            </div> 
                            <div class="mb-3">
                              <label for="" class="form-label">Occupation</label>
                              <input type="text"
                                class="form-control" name="Occupation" id="occupationInput" aria-describedby="helpId" placeholder="">
                              <small id="helpId" class="form-text text-muted"></small>
                            </div> 
                            <div class="mb-3">
                              <label for="" class="form-label">Hire Date</label>
                              <input type="date"
                                class="form-control" name="Hire_Date" id="hireDateInput" aria-describedby="helpId" placeholder="">
                              <small id="helpId" class="form-text text-muted"></small>
                            </div>
                            <button type="submit" class="btn btn-primary">Submit</button>
                        </form>
                </div>
              </div>
            </div>
        </div>
        <!-- <div class="tab-pane" id="messages" role="tabpanel" aria-labelledby="messages-tab"> messages </div> -->
        </div>
    </main>
<?php include("footer.php") ?>