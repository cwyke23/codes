<!DOCTYPE html5>
<?php
$pdo = new PDO('mysql:host=localhost;port=8889;dbname=misc','cam','zap');
// turn pdo errors on
$pdo->setAttribute(PDO::ATTR_ERRMODE, PDO::ERRMODE_EXCEPTION);
?>
