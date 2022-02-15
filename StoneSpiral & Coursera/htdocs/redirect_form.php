<?php
session_start();

if ( isset($_POST['guess'])) {
  $guess = $_POST['guess'] + 0;
  $_SESSION['guess'] = $guess;
  if ( $guess == 42) {
    $_SESSION['message'] = 'You got it!';
  }
  else if ( $guess < 42) {
    $_SESSION['message'] = 'Too Low';
  }
  else {
    $_SESSION['message'] = 'Too high';
  }
  // redirects back to same page, so POST data lost to avoid double POST
  // Variables saved in SESSION which doesn't change between requests
  header("Location: redirect_form.php");
  // immediately redirects, nothing done in view 302
  return;
}
?>



<html>
<head><title> Guessing Game mk2 </title></head>
<body style="font-family: sans-serif;">
<?php
  $guess = isset($_SESSION['guess']) ? $_SESSION['guess'] : '';
  $message = isset($_SESSION['message']) ? $_SESSION['message'] : '';
?>
<pre>
<h1> Guessing Game </h1>
<p> <?php
if ($message !== false) {
  echo("$message");
  //unset value so it is not printed upon refresh
  //flash message
  unset($_SESSION['message']);
}?>
</p>
<form method="post">
<p><label for="i1"> Enter Guess: </label>
<!-- value gives shown input after submission -->
<input type="text" name="guess" id="i1" size="20" value="<?= htmlentities($guess) ?>"/>
<br> <input type="submit" value="Submit"/> </p>
<?php unset($_SESSION['guess']); ?>
</pre>
</body>
</html>
