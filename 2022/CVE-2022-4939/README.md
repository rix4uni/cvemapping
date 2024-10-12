# PoC-CVE-2022-4939

The attacker sends a specially crafted request to the wp_ajax_nopriv_wcfm_ajax_controller AJAX action to modify the membership registration form and set the registration role to that of an administrator. Then, the plugin processes the request and modifies the membership registration form to allow users to register with the role of an administrator. 
The attacker can register as a new user with the administrator role by submitting the modified membership registration form.
