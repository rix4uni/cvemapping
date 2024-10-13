<?php
	/**
	 * Yes this code is not brilliant, don't tell me about it.
	 */
	
	class VulnStatus
	{
		const FAIL        = 0;
		const VULN        = 1;
		const VULN_NOT_MS = 2;
		const PATCHED     = 3;
		const NOT_VULN    = 4;
		const NOT_VULN_MS = 5;
		const NOT_VULN_CF = 6;
		
		public static function AsString( $status, $host )
		{
			switch( $status )
			{
				case self::FAIL       : return '<div class="alert alert-warning">Couldn\'t connect to <b>' . $host . '</b> to test the vulnerability.</div>';
				case self::VULN       : return '<div class="alert alert-danger"><b>' . $host . '</b> is vulnerable.</div>';
				case self::VULN_NOT_MS: return '<div class="alert alert-warning"><b>' . $host . '</b> could be vulnerable, but it doesn\'t appear to be using IIS.</div>';
				case self::PATCHED    : return '<div class="alert alert-success"><b>' . $host . '</b> is patched.</div>';
				case self::NOT_VULN   : return '<div class="alert alert-info">Cannot discern patch status of <b>' . $host . '</b>, and it doesn\'t appear to be using IIS. This most likely means it is not vulnerable.</div>';
				case self::NOT_VULN_MS: return '<div class="alert alert-info">Cannot discern patch status of <b>' . $host . '</b>. This most likely means it is not vulnerable.</div>';
				case self::NOT_VULN_CF: return '<div class="alert alert-success"><b>' . $host . '</b> is using CloudFlare and is not vulnerable. <a href="https://blog.cloudflare.com/cloudflare-is-protected-against-cve-2015-1635/" target="_blank">See their blog post for more details.</a></div>';
			}
			
			return 'it broke, yo';
		}
	}
	
	$host = false;
	$status = false;
	$url = filter_input( INPUT_GET, 'host', FILTER_SANITIZE_URL );
	
	if( !empty( $url ) && parse_url( $url, PHP_URL_SCHEME ) === null )
	{
		$url = 'http://' . $url;
	}
	
	$port = parse_url( $url, PHP_URL_PORT );
	
	if( $port === null )
	{
		$port = 80;
	}
	
	$url = parse_url( $url, PHP_URL_HOST );
	
	if( $url !== null )
	{
		$cachekey = 'ms15034_' . $url . '_' . $port;
		$cachetime = 300; // 5 minutes
		
		$host = htmlspecialchars( $url, ENT_HTML5 );
		
		if( $port !== 80 )
		{
			$host .= ':' . $port;
		}
		
		$memcached = new Memcached( );
		$memcached->addServer( '/var/run/memcached/memcached.sock', 0 );
		
		$status = $memcached->get( $cachekey );
		
		if( $status === false )
		{
			$fp = @fsockopen( $url, $port, $errno, $errstr, 5 );
			
			if( $fp === false )
			{
				$status = VulnStatus::FAIL;
			}
			else
			{
				stream_set_timeout( $fp, 5 );
				
				$header = "GET / HTTP/1.1\r\n";
				$header .= "Host: stuff\r\n";
				$header .= "Range: bytes=0-18446744073709551615\r\n";
				$header .= "User-Agent: HTTPsys online check\r\n";
				$header .= "Connection: close\r\n\r\n";
				
				fwrite( $fp, $header );
				
				$response = fread( $fp, 1024 );
				
				fclose( $fp );
				
				if( strpos( $response, 'Requested Range Not Satisfiable' ) !== false )
				{
					$status = strpos( $response, 'Microsoft' ) === false ? VulnStatus::VULN_NOT_MS : VulnStatus::VULN;
				}
				else if( strpos( $response, 'The request has an invalid header name' ) !== false )
				{
					$cachetime = 3600; // cache patched servers for 1 hour
					$status = VulnStatus::PATCHED;
				}
				else if( strpos( $response, 'Microsoft' ) === false )
				{
					if( strpos( $response, '403 Forbidden' ) !== false && strpos( $response, 'cloudflare-nginx' ) !== false )
					{
						$status = VulnStatus::NOT_VULN_CF;
					}
					else
					{
						$status = VulnStatus::NOT_VULN;
					}
				}
				else
				{
					$status = VulnStatus::NOT_VULN_MS;
				}
			}
			
			unset( $fp, $header, $response );
			
			$memcached->set( $cachekey, $status, $cachetime );
		}
		
		$status = VulnStatus::AsString( $status, $host );
	}
?>
<!DOCTYPE HTML>
<html lang="en">
<head>
	<meta charset="utf-8">
	<meta name="theme-color" content="#424242">
	<meta http-equiv="X-UA-Compatible" content="IE=edge,chrome=1">
	<meta name="viewport" content="width=device-width, initial-scale=1.0">
	
	<title>MS15-034 Test</title>
	
	<link rel="author" href="https://plus.google.com/+thexpaw">
	<link href="//maxcdn.bootstrapcdn.com/bootstrap/3.3.4/css/bootstrap.min.css" rel="stylesheet">
	
	<style type="text/css">
		.container {
			max-width: 900px;
		}
		
		.masthead {
			position: relative;
			padding: 20px 0;
			text-align: center;
			color: #fff;
			background-color: #424242;
			margin-bottom: 20px;
		}
		
		.masthead a {
			color: #fff;
		}
		
		.footer {
			text-align: center;
			padding: 15px;
			color: #555;
		}
		
		.footer span {
			color: #FA5994;
		}
		
		.form-inline {
			text-align: center;
			margin-bottom: 20px;
		}
		
		.github {
			position: absolute;
			top: 0;
			right: 0;
		}
	</style>
</head>
<body>
	<div class="masthead">
		<div class="container">
			<h1>HTTP.sys vulnerability test</h1>
			<h3>Enter a URL or a hostname to test the server for <a href="https://technet.microsoft.com/en-us/library/security/ms15-034.aspx" target="_blank">MS15-034</a> / <a href="http://www.cve.mitre.org/cgi-bin/cvename.cgi?name=CVE-2015-1635" target="_blank">CVE-2015-1635</a>.</h3>
		</div>
	</div>
	
	<a href="https://github.com/xPaw/HTTPsys">
		<img class="github" src="https://camo.githubusercontent.com/38ef81f8aca64bb9a64448d0d70f1308ef5341ab/68747470733a2f2f73332e616d617a6f6e6177732e636f6d2f6769746875622f726962626f6e732f666f726b6d655f72696768745f6461726b626c75655f3132313632312e706e67" alt="Fork me on GitHub">
	</a>
	
	<div class="container">
		<blockquote>
			<p>A remote code execution vulnerability exists in the HTTP protocol stack (HTTP.sys) that is caused when HTTP.sys improperly parses specially crafted HTTP requests. An attacker who successfully exploited this vulnerability could execute arbitrary code in the context of the System account.</p>
			<p>To exploit this vulnerability, an attacker would have to send a specially crafted HTTP request to the affected system. The update addresses the vulnerability by modifying how the Windows HTTP stack handles requests.</p>
		</blockquote>
		
		<form class="form-inline" id="js-form" method="GET">
			<div class="form-group">
				<input type="text" class="form-control input-lg" id="js-input" placeholder="bing.com" name="host" autofocus<?php if( $host !== false ) { echo ' value="' . $host . '"'; } ?>>
				<button type="submit" class="btn btn-primary btn-lg">Check</button>
			</div>
		</form>
		
		<?php if( $status !== false ) { echo $status; } ?>
		
		<div class="footer">Made with <span>♥</span> by <a href="http://xpaw.me" target="_blank">xPaw</a> (<a href="https://twitter.com/thexpaw" target="_blank">@thexpaw</a>) | All results are cached for five minutes</div>
	</div>
</body>
</html>
