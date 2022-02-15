<?php
session_start();
 if ( ! isset($_SESSION['name'])) {
  die('ACCESS DENIED');
}
require_once "pdo.php";

$fail = false;
$pass = false;
if (isset($_POST['make']) && isset($_POST['model']) && isset($_POST['year']) && isset($_POST['mileage'])) {
  if (strlen($_POST['make']) < 1 || strlen($_POST['model']) < 1 || strlen($_POST['year']) < 1 || strlen($_POST['mileage']) < 1) {
    $fail = "All fields are required";
    $_SESSION['fail'] = $fail;
    header('Location: add.php');
    return;
  }
  elseif (is_numeric($_POST['year']) === false || is_numeric($_POST['mileage']) === false ){
    $fail = "Mileage and year must be numeric";
    $_SESSION['fail'] = $fail;
    header('Location: add.php');
    return;
  }
  else {
    $sql = "INSERT INTO autos( make, model, year, mileage)
            VALUES (:make, :model, :year, :mileage)";
    $stmt = $pdo->prepare($sql);
    $stmt->execute(array(
      ":make" => $_POST['make'],
      ":model" => $_POST['model'],
      ":year" => $_POST['year'],
      ":mileage" => $_POST['mileage']
    ));
    $pass = "Record added";
    $_SESSION['success'] = $pass;
    header('Location: index.php');
    return;

  }
}
?>

<html>
<head>
<?php require_once "bootstrap.php"; ?>
<title> Cameron Wyke Auto Database Add </title>
</head>

<body>
  <div class="container">
    <h1> Tracking Autos for <?= htmlentities($_SESSION['name']) ?> </h1>

    <a href="login.php">Please Log In</a>
    <form method="post">
      <p> <label for="make"> Make: </label>
        <input type="text" name="make" id="make" size="40"/> </p>
      <p> <label for="model"> Model: </label>
        <input type="text" name="model" id="model" size="40"/> </p>
      <p> <label for="yr"> Year: </label>
        <input type="text" name="year" id="yr" size="40"/> </p>
      <p> <label for="mile"> Mileage: </label>
        <input type="text" name="mileage" id="mile" size="40"/> </p>
      <input type="submit" name="dopost" value="Add"/>
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
