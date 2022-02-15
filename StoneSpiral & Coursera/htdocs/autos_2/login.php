<?php // Do not put any HTML above this line
session_start();
if ( isset($_POST['cancel'] ) ) {
    // Redirect the browser to index.php
    header("Location: index.php");
    return;
}

$salt = 'XyZzy12*_';
$stored_hash = '1a52e17fa899cf40fb04cfc42e6352f1'; //pw is php123
//$stored_hash = 'a8609e8d62c043243c4e201cbb342862';  // Pw is meow123

$failure = false;  // If we have no POST data

// Check to see if we have some POST data, if we do process it
if ( isset($_POST['email']) && isset($_POST['pass']) ) {
    if ( strlen($_POST['email']) < 1 || strlen($_POST['pass']) < 1 ) {
        $failure = "Email and password are required";
        // pass values to session and redirect to get rid of post
        $_SESSION['failure'] = $failure;
        header("Location: login.php");
        return;
    }
    // check if email contains @
    elseif (strpos($_POST['email'],'@') === false) {
       $failure ="Email must have an at-sign (@)";
       $_SESSION['failure'] = $failure;
       header("Location: login.php");
       return;
    }
      else {
        $check = hash('md5', $salt.$_POST['pass']);
        if ( $check == $stored_hash ) {
            // Redirect the browser to game.php
            //url encode allows variable to be submitted as part of URL
            error_log("Login success ".$_POST['email']);
            $_SESSION['name'] = $_POST['email'];
            header("Location: view.php");
            return;
        } else {
            $failure = "Incorrect password";
            $_SESSION['failure'] = $failure;

            // submit to developer error log
            error_log("Login fail ".$_POST['email']." $check");
            header("Location: login.php");
            return;
        }
    }
}

// Fall through into the View
?>
<!DOCTYPE html>
<html>
<head>
<?php require_once "bootstrap.php"; ?>
<title>Cameron Wyke's 070ef5b8 Login Page</title>
</head>
<body>
<div class="container">
<h1>Please Log In</h1>
<?php
// Note triple not equals and think how badly double
// not equals would work here...
if ( isset($_SESSION['failure'])) {
    // Look closely at the use of single and double quotes
    echo('<p style="color: red;">'.htmlentities($_SESSION['failure'])."</p>\n");
    unset($_SESSION['failure']);
}
?>
<form method="post">
<label for="nam">Email</label>
<input type="text" name="email" id="nam"><br/>
<label for="id_1723">Password</label>
<input type="text" name="pass" id="id_1723"><br/>
<input type="submit" value="Log In">
<input type="submit" name="cancel" value="Cancel">
</form>
<p>
For a password hint, view source and find a password hint
in the HTML comments.
<!-- Hint: The password is the program used in the course
 (all lower case) followed by 123. -->
</p>
</div>
</body>
