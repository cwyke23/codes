
<?php
// inserting cookies
if  (! isset($_COOKIE['hi'])) {
  // set cookie (key, value, time it exists)
  setcookie('hi', '1', time()+3600);
}
echo "<pre>";


// starting a session
session_start();
// creates session with session_id as cookie and empty $_SESSION  array
if ( ! isset($_SESSION['hi'])) {
  echo( "<p> session is empty </p> \n" );
  $_SESSION['hi'] = 0;
}
elseif  ($_SESSION['hi'] < 3) {
  // session array doesn't refresh upon new request so can be modified
  $_SESSION['hi']= $_SESSION['hi'] +1;
  echo ("<p> added one to session value </p> \n");
}
else {
  //gets rid of all info in session, doesn't delete sess id
  session_destroy();
  session_start();
  echo "<p> Restarted session </p> \n";
}

?>
<!DOCTYPE html5>
<html>
<head><title> Sessions and Cookies </title> </head>
<body>
<h1> Sessions and Cookies example </h1>
<?php
echo "Cookie array \n";
print_r($_COOKIE);
echo "Session array \n";
print_r($_SESSION);
?>
<p> <a href="cookie_sessions.php"> Click to refresh Page</a>
  <br> Note how cookies do not change unike post and get, look here they are stored in browser </p>
</pre>
</body>
</html>
