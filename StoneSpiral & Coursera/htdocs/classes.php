<!DOCTYPE html5>
<html>
<head><title> Cam's first objects in PHP </title></head>

<body>
<?php
// create class
class Pet{
  // create some variables, can be called by $this->
  protected $greet = "Hello"; // can be called/changed in subclass but not outside
  public $amount = 1; // can be called/ changed anywhere
  private $species; // can't be called / changed outside class or in subclasses
  // constructor function same as __init__
  function __construct( string $species = "Dog") {
    // $this akin to self, refers to name of object created
    // -> is akin to . , defines method
    $this->species = $species;
  }
  function greet() {
    if ($this->species == "Dog") return 'Woof'."<br>";
    if ($this->species == "Cat") return 'Meow';
  }
  // static functions don't require $this and can be called directly from the class name
  static function info() {
    print('This class creates a Pet object that can greet you, subclass is talking pets');
  }

}
// inherits from Pet via extends keyword
class talking_pet extends Pet{
  function __construct( string $species = "Dog") {
    // $this akin to self, refers to name of object created
    // -> is akin to . , defines method
    $this->species = $species;
  }
  function talk() {
    if ( $this->species == "Dog") return "<br>".$this->greet." I'm a talking Dog \n";
    if ( $this->species == "Cat") return "<br>".$this->greet." I'm a talking Cat \n";
}
}
//creating instances of objects
$hank = new Pet();
$simba = new Pet("Cat");
$sparky = new talking_pet("Cat");
//calling object functions
echo $hank->greet()."\n";
echo $simba->greet()."\n";
// inherited class has talk method aswell
echo $sparky->greet()."\n";
echo $sparky->talk()."<br>";
//call public object variable
echo $simba->amount;
// calling private/ protected causes error:
//echo $simba->greet;
//calling static method with ::
echo Pet::info();
//can't call dynamic methods like this
//echo Pet::greet();

?>
</body>
</html>
