<?php
session_start();
require_once 'pdo.php';
if ( ! isset($_SESSION['name'])) {
  die('ACCESS DENIED');
}
require_once "pdo.php";

if (isset($_POST['make']) && isset($_POST['model']) && isset($_POST['year']) && isset($_POST['mileage'])) {
  if (strlen($_POST['make']) < 1 || strlen($_POST['model']) < 1 || strlen($_POST['year']) < 1 || strlen($_POST['mileage']) < 1) {
    $fail = "Make is required";
    $_SESSION['fail'] = $fail;
    header('Location: edit.php');
    return;
  }
  elseif (is_numeric($_POST['year']) === false || is_numeric($_POST['mileage']) === false ){
    $fail = "Mileage and year must be numeric";
    $_SESSION['fail'] = $fail;
    header('Location: edit.php');
    return;
  }
  else {
    $sql = "UPDATE autos SET make = :make,
     model = :model, year= :year, mileage = :mileage
     WHERE auto_id = :auto_id";
    $stmt = $pdo->prepare($sql);
    $stmt->execute(array(
      ":make" => $_POST['make'],
      ":model" => $_POST['model'],
      ":year" => $_POST['year'],
      ":mileage" => $_POST['mileage'],
      ":auto_id" => $_POST['auto_id']
    ));
    $pass = "Record updated";
    $_SESSION['success'] = $pass;
    header('Location: index.php');
    return;

  }
}

// testing if id given in get request is valid to delete
$stmt = $pdo->prepare("SELECT make, model, year,mileage, auto_id FROM autos where auto_id = :zip ");
$stmt->execute(array(':zip' => $_GET['auto_id']));
$row = $stmt->fetch(PDO::FETCH_ASSOC);
if ( $row === false) {
  $_SESSION['error'] = 'Bad value for auto_id';
  header( 'Location: index.php');
  return;
}
?>

<html>
<head>
<?php require_once "bootstrap.php"; ?>
<title> Cameron Wyke Auto Database Edit</title>
</head>

<body>
  <div class="container">
    <h1> Edit Auto </h1>

    <a href="login.php">Please Log In</a>
    <form method="post">
      <p> <label for="make"> Make: </label>
        <input type="text" name="make" id="make" size="40" value="<?= htmlentities($row['make']) ?>"/> </p>
      <p> <label for="model"> Model: </label>
        <input type="text" name="model" id="model" size="40" value="<?= htmlentities($row['model']) ?>"/> </p>
      <p> <label for="yr"> Year: </label>
        <input type="text" name="year" id="yr" size="40" value="<?= htmlentities($row['year']) ?>"/> </p>
      <p> <label for="mile"> Mileage: </label>
        <input type="text" name="mileage" id="mile" size="40" value="<?= htmlentities($row['mileage']) ?>"/> </p>
      <input type= "hidden" name="auto_id" value= "<?= $row['auto_id'] ?>"/>
      <input type="submit" name="dopost" value="Save"/>
      <!-- other buttons, href for location when clicked
      return false means form not submitted -->
      <input type="button"
          onclick="location.href='index.php'; return false;"
          value="Cancel"/> </br>
          <?php
                // Note triple not equals and think how badly double
                // not equals would work here...
          if ( isset($_SESSION['fail'])) {
                    // Look closely at the use of single and double quotes
             echo('<p style="color: red;">'.htmlentities($_SESSION['fail'])."</p>\n");
             unset($_SESSION['fail']);
          }
          ?>
</body>
</html>
