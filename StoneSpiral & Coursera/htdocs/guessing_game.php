<!DOCTYPE html5>
<html>
<head>
<title> Cameron Wyke f904670e </title>
</head>
<body>
<p>
<h1>
<?php
 if ( ! isset($_GET['guess'])) {
   echo("Missing guess parameter");
 } elseif (strlen($_GET['guess'])< 1) {
   echo("Your guess is too short");
 } elseif( ! is_numeric($_GET['guess'])) {
   echo("Your guess is not a number");
 } elseif( $_GET['guess']>44) {
   echo("Your guess is too high");
 } else if( $_GET['guess']< 44) {
   echo("Your guess is too low");
 } else {
   echo('Congratulations - You are right');
 }
?>
</h1>
<!-- checking if value exists and printing no.-->

 <pre> <!-- undoes previous formatting so not everything on same line -->
<?php
// ternary operator
 echo isset($_GET['guess']) ? "Name is set \n" : "Name not set\n";
// null coalescing
 echo isset($_GET['guess']) ?? 'Not set';
 if(isset($_GET['guess'])) {
    echo("This is your number:\n"),
    //prints recursively all items in list
    print_r($_GET),
    //more detail, prints type
    var_dump($_GET);}
// making array
$stuff = array("name" => "Cam",
               "guess" => $_GET["guess"]);
// adding html tags within php
echo("<h2>\n");
print_r($stuff);
echo("</h2>\n");
// adding new item
$stuff["new_item"] = "I'm new";
var_dump($stuff);
//sorting

//by key
echo("Sorted by key\n");
ksort($stuff);
print_r($stuff);
//by value (awesome)
echo("Sorted by value\n");
asort($stuff);
print_r($stuff);
//by number (deletes string key)
echo("Sorted by number\n");
sort($stuff);
print_r($stuff);

?>
</pre>
</p>
</body>
</html>
