<?php
session_start();
require_once 'pdo.php';
if ( ! isset($_SESSION['name'])) {
  die('ACCESS DENIED');
}
require_once "pdo.php";
if (isset($_POST['delete']) && isset($_POST['auto_id'])) {
  $sql = "DELETE FROM autos WHERE auto_id = :zip";
  $stmt = $pdo->prepare($sql);
  $stmt->execute(array(':zip'=> $_POST['auto_id']));
  $_SESSION['success'] = "Record deleted";
  header( 'Location: index.php');
  return;
}
// testing if id given in get request is valid to delete
$stmt = $pdo->prepare("SELECT make, model, auto_id FROM autos where auto_id = :zip ");
$stmt->execute(array(':zip' => $_GET['auto_id']));
$row = $stmt->fetch(PDO::FETCH_ASSOC);
if ( $row === false) {
  $_SESSION['error'] = 'Bad value for auto_id';
  header( 'Location: index.php');
  return;
}
?>
<html>
<head><title> Cameron Wyke Delete Page </title></head>
<body>
<p> Confirm Deleting <?= htmlentities($row['make']), htmlentities($row['model']) ?> </p>

<form method="post">
  <input type= "hidden" name="auto_id" value= "<?= $row['auto_id'] ?>"/>
  <input type="submit" name="delete" value="Delete"/>
  <a href="index.php"> Cancel </a>
</form>
</body></html>
