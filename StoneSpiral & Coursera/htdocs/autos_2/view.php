<?php
session_start();
if ( ! isset($_SESSION['name'])) {
  die('Not logged in');
}
require_once "pdo.php";
?>

<html>
<head>
<?php require_once "bootstrap.php"; ?>
<title> Cameron Wyke Auto Database Table </title>
</head>
<pre>
<body>
  <div class="container">
    <h1> Tracking Autos for <?= htmlentities($_SESSION['name']) ?> </h1>
<h2> Automobiles </h2>
<?php
      // Note triple not equals and think how badly double
      // not equals would work here...
if ( isset($_SESSION['success']) ) {
          // Look closely at the use of single and double quotes
   echo('<p style="color: green;">'.htmlentities($_SESSION['success'])."</p>\n");
   unset($_SESSION['success']);
}
?>
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
<a href="add.php"> Add New </a>
<a href="logout.php"> Logout </a>
</pre>
</body>
</html>
