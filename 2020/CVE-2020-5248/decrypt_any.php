<?php
function decrypt($string) {
    $result = '';
    $key="GLPI£i'snarss'ç";
    $string = base64_decode($string);
    for ($i=0; $i<strlen($string); $i++) {
        $char    = substr($string, $i, 1);
        $keychar = substr($key, ($i % strlen($key))-1, 1);
        $char    = chr(ord($char)-ord($keychar));
        $result .= $char;
    }
    echo $result;
}
decrypt("INSERT_COIN");
