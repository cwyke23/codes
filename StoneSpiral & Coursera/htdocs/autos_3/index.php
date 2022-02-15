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
  <div>
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
if ( isset($_SESSION['error']) ) {
          // Look closely at the use of single and double quotes
   echo('<p style="color: red;">'.htmlentities($_SESSION['error'])."</p>\n");
   unset($_SESSION['error']);
}
?>
<?php
$stmt = $pdo->query("SELECT * FROM autos ");
$row = $stmt->fetch(PDO::FETCH_ASSOC);
if ( $row === false) {
  echo ("No rows found </br>");

}
else {
$stmt = $pdo->query("SELECT * FROM autos ");
echo '<table border="1">'."\n";
while ( $row = $stmt->fetch(PDO::FETCH_ASSOC)) {
  echo '<tr><td>';
  echo (htmlentities($row['make']));
  echo '</td><td>';
  echo (htmlentities($row['model']));
  echo '</td><td>';
  echo (htmlentities($row['year']));
  echo '</td><td>';
  echo (htmlentities($row['mileage']));
  echo '</td><td>';
  echo ('<a href="edit.php?auto_id='.$row['auto_id'].'"> Edit</a> / ');
  echo ("<a href='delete.php?auto_id=".$row['auto_id']."'> Delete</a>");
  echo '</td></tr>'."\n";
}
echo '</table>';
}
?>
<a href="add.php"> Add New Entry</a>
<a href="logout.php"> Logout </a>
</pre>
</body>
</html>
