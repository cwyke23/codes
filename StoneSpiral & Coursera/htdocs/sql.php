<!DOCTYPE html5 >
<html>
<head><title> PDO and SQL </title> </head>

<body>
<?php
//echo "<pre>\n";
// log in to database and load in as database object, last 2 parameters
//are username and password set during GRANT, port 8889 for MAC, 3306 for windows
$pdo = new PDO('mysql:host=localhost;port=8889;dbname=php','cam','pass');
$pdo->setAttribute(PDO::ATTR_ERRMODE, PDO::ERRMODE_EXCEPTION);
//Add Users
if ( isset($_POST['name']) && isset($_POST['email'])) {
  // write sql statement with placeholder values
  $sql = "INSERT INTO users (name, email)
          VALUES (:name, :email)";
  // get sql to check command
  $stmt = $pdo->prepare($sql);
  // execute, replacing placeholders with POST variables
  $stmt->execute(array(
      ':name' => $_POST['name'],
      ':email' => $_POST['email']
  ));
}

// Deleting Users
if (isset($_POST['id'])) {
  $sql = "DELETE FROM users WHERE user_id = :id";
  $stmt= $pdo->prepare($sql);
  $stmt->execute(array(':id' => $_POST['id']));
}

if (isset($_POST['delete']) && isset($_POST['user_id'])) {
  $sql = "DELETE FROM users WHERE user_id = :id";
  $stmt= $pdo->prepare($sql);
  $stmt->execute(array(':id' => $_POST['user_id']));
}

?>

<!-- Create form for inputting data to be saved to database -->
<h2> Add a new User: </h2>
<form method = "post" >
  <p>Name:<input type="text" name="name" size="40"></p>
  <p>Email:<input type="text" name="email" size="40"></p>
  <p><input type="submit" value="Add New"/> </p>
</form>


<!-- print out data from database -->
<?php
// use query method and input SQL statements
$stmt = $pdo->query("SELECT * FROM users");
// print out each record
// $row becomes each row from selected data
//create table to put data in
echo '<table border="1">'."\n";
while ( $row = $stmt->fetch(PDO::FETCH_ASSOC)) {
  //print_r($row)
  // table row and table data
  echo "<tr><td>";
  echo($row['user_id']);
  echo ("</td><td>");
  echo($row['name']);
  echo ("</td><td>");
  echo($row['email']);
  echo ("</td><td>");
  echo ('<form method = "post"><input type="hidden" ');
  echo ('name ="user_id" value="'.$row['user_id'].'"/>'."\n");
  echo ('<input type="submit" value="Del" name="delete"');
  echo ("\n</form>\n");
  echo ("</td></tr>\n");
}
echo "</table>\n";
print_r($_POST);
//echo "</pre>\n";
?>
<h2> Delete a User </h2>
<form method = "post" >
  <p>ID to Delete:<input type="text" name="id" size="40"></p>
  <p><input type="submit" value="Delete"/></p>

</body>
</html>
