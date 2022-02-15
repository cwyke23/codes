<!DOCTYPE = html5>
<html>
<head> <title> Forms and POST </title> </head>

<body>
  <!-- defaut is get -->
<form method = "post">
<!-- text around box -->
<p><label for="thin">Input </label>
<!-- type of form box, key name that value
is going to be passed to on submission,
id for css -->
<input type = "text" name="thing" id="thing"/></p>
<!-- create button -->
<input type="submit" />

</form>
<?php
// ternary operator, if post value set, copy value into variable
 $old_user = isset($_POST['user']) ? $_POST['user'] : '';
 $old_pw = isset($_POST['pw']) ? $_POST['pw'] : '';
 // variables printed under value in form text upon submission
 //html entities use to prevent injection
 ?>
<form method = "post">
  <p><label for = "i1"> Username: </label>
  <input type="text" name="user" id="i1" value = "<?= htmlentities($old_user) ?>" size="20"/></p>
  <!-- 2nd box -->
  <p><label for="i2"> Password: </label>
  <input type="password" name="pw" id="i2" value="<?= htmlentities($old_pw) ?>" size="40"/></p>
  <!-- Other html5 inputs -->
  <p><label for="i2"> Colour: </label>
  <input type="color" name="colour" id="i2" size="40"/></p>
  <p><label for="i2"> Date of Birth: </label>
  <input type="date" name="dob" id="i2" size="40"/></p>
  <p><label for="i2"> Email: </label>
  <input type="email" name="email" id="i2" size="40"/></p>
  <p><label for="i2"> Quantity (between 1 and 5): </label>
  <input type="number" name="q" min = "1" max = "5" id="i2" size="40"/></p>
  <!-- radio button, same names so only 1 can be chosen
  different values for name key if chosen -->
  <p><label for="i3"> Seating? :</label><br>
    <input type="radio" name="seat" value="in"/> Inside<br>
    <input type="radio" name="seat" value="out"/> Outside </p>

  <!-- checkbox, multiple can be chosen, different names/keys -->
  <p><label for="i4"> Extras? : </label><br>
    <input type="checkbox" name="check1" value="smoke"/> Smoking <br>
    <input type="checkbox" name="check2" value="wine"/> Wine <br>
    <input type="checkbox" name="check3" value="donate"/> Donation <br>
 <!-- drop-box, multiple values for one key, select tag! -->
 <label for="i5" > Drink: </label>
 <select name="drink" id="i5">
   <option value="0">--Please Select--</option>
   <option value = "1"> Wine </option>
   <option value="2" selected> Beer </option>
   <option value="3"> Cider </option>
 </select><br>
<!-- Text area, separate tag, all text is value -->
<label for="i6"> Anything Else: </label><br>
<textarea rows="5" cols="50" id="i6" name="extras">
 Write any extras in this box
</textarea>
</p>
<!-- submit button, value is what is written on button -->
  <input type="submit" name="dopost" value="Submit Choices"/>
<!-- other buttons, href for location when clicked
return false means form not submitted -->
  <input type="button"
    onclick="location.href='index.php'; return false;"
    value="Return to Home"/>
</form>
<?php
// see parameter in url, useful for bookmarks
echo "GET";
print_r($_GET);
// don't see parameter, data being changed, e.g. bank
echo "POST";
print_r($_POST);

if (isset($_POST['user'])) {
  echo $_POST['user'];
}
?>
</body>
</html>
