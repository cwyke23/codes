<!DOCTYPE html5>
<html>
<head>
<title> Cameron Wyke 4 digit MD5 Cracker </title>
</head>

<body>
<h1> MD5 Cracker </h1>
<div> This application takes an MD5 hash of a four digit pin and check all 10,000 possible four digit PINs to determine the PIN.
</div>
<pre>
Debug Output
<?php
$goodtext = 'Not Found';

if (isset($_GET['md5'])) {
  $md5 = $_GET['md5'];
  $pre_time = microtime(true);
  // alphabet
  $txt = "0123456789";
  $show = 15;

  //1st loop, 1st digit
  for ($i=0; $i<strlen($txt); $i++ ) {
    $ch1 = $txt[$i];
    for($j=0; $j<strlen($txt); $j++) {
      $ch2 = $txt[$j];
      for($k=0; $k<strlen($txt); $k++) {
        $ch3 = $txt[$k];
        for($l=0; $l<strlen($txt); $l++) {
          $ch4 = $txt[$l];
          // concat the 4 digits to make code guess
          $try = $ch1.$ch2.$ch3.$ch4;
          // run hash and compare with input
          $check = hash('md5', $try);
          if ($check == $md5) {
            $goodtext = $try;
            break;
          }
          if ($show > 0) {
            print "md5 : $check code: $try \n";
            $show = $show - 1;
          }
        }
      }
    }
  }
}
else {
  echo "No md5 input";
}
// elapsed time
$post_time = microtime(true);
print "Elapsed time: ";
print $post_time - $pre_time;
print "\n";
echo "<h2>\n";
print "The code is: \n";
print $goodtext;
echo "</h2>\n";
 ?>
</pre>

</html>
