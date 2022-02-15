<!DOCTYPE html5>
<?php
require_once "pdo.php";

if (!isset($_GET['name'])) {
  die("Name parameter missing");
}
$fail = false;
$pass = false;
if (isset($_POST['make']) && isset($_POST['year']) && isset($_POST['mileage'])) {
  if (strlen($_POST['make']) < 1 || strlen($_POST['year']) < 1 || strlen($_POST['mileage']) < 1) {
    $fail = "Make is required";
  }
  elseif (is_numeric($_POST['year']) === false || is_numeric($_POST['mileage']) === false ){
    $fail = "Mileage and year must be numeric";
  }
  else {
    $sql = "INSERT INTO autos( make, year, mileage)
            VALUES (:make, :year, :mileage)";
    $stmt = $pdo->prepare($sql);
    $stmt->execute(array(
      ":make" => $_POST['make'],
      ":year" => $_POST['year'],
      ":mileage" => $_POST['mileage']
    ));
    $pass = true;

  }
}
?>
<html>
<head>
<?php require_once "bootstrap.php"; ?>
<title> Cameron Wyke Auto Database </title>
</head>

<body>
  <div class="container">
    <h1> Tracking Autos for <?= htmlentities($_GET['name']) ?> </h1>
    <?php
          // Note triple not equals and think how badly double
          // not equals would work here...
    if ( $pass !== false ) {
              // Look closely at the use of single and double quotes
       echo('<p style="color: green;">'."Record inserted"."</p>\n");
    }
    ?>
    <a href="login.php">Please Log In</a>
    <form method="post">
      <p> <label for="make"> Make: </label>
        <input type="text" name="make" id="make" size="40"/> </p>
      <p> <label for="yr"> Year: </label>
        <input type="text" name="year" id="yr" size="40"/> </p>
      <p> <label for="mile"> Mileage: </label>
        <input type="text" name="mileage" id="mile" size="40"/> </p>
      <input type="submit" name="dopost" value="Add"/>
      <!-- other buttons, href for location when clicked
      return false means form not submitted -->
      <input type="button"
          onclick="location.href='index.php'; return false;"
          value="logout"/> </br>

    <?php
          // Note triple not equals and think how badly double
          // not equals would work here...
    if ( $fail !== false ) {
              // Look closely at the use of single and double quotes
       echo('<p style="color: red;">'.htmlentities($fail)."</p>\n");
    }
    ?>
  </br>
     <h2> Automobiles </h2>
     <?php
     $stmt = $pdo->query("SELECT * FROM autos ");
     echo '<ul>'."\n";
     while ( $row = $stmt->fetch(PDO::FETCH_ASSOC)) {
       echo '<li>';
       echo (htmlentities($row['year'])." ".htmlentities($row['make']).", Mileage: ".htmlentities($row['mileage']));
       echo '</li>'."\n";
     }
     echo '</ul>'
    ?>
</body>
</html>
