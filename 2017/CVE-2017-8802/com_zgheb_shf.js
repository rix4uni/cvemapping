function com_zgheb_shf_HandlerObject() {
};
com_zgheb_shf_HandlerObject.prototype = new ZmZimletBase();
com_zgheb_shf_HandlerObject.prototype.constructor = com_zgheb_shf_HandlerObject;
var SHFZimlet = com_zgheb_shf_HandlerObject;

SHFZimlet.prototype.init = function() {
  console.log("Initializing SHF Zimlet");
  ZmKeyMap.SHOW_FRAGMENT="INVALID";
};
