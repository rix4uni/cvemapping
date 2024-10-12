# CVE-2023-1874

## Disclaimer

THIS SCRIPT IS DESIGNED FOR WHITE HAT AND EDUCATIONAL PURPOSES ONLY. ANY USE OF THIS AGAINST A DEVICE YOU ARE NOT AUTHORIZED TO TEST ON OR DO NOT OWN IS YOUR OWN RESPONSIBILITY. THE AUTHOR OF THIS SCRIPT TAKES NO RESPONSIBILITY FOR ANYTHING YOU DO WITH THIS SCRIPT. YOUR ACTIONS ARE YOUR OWN.

## Description

CVE-2023-1874 is a vulnerability in the WP Data Access plugin versions 5.3.7 and earlier. An attacker can supply the `wpda_role[]` option when updating a profile to escalate privileges.

From NIST:

```
The WP Data Access plugin for WordPress is vulnerable to privilege escalation in versions up to, and including, 5.3.7. This is due to a lack of authorization checks on the multiple_roles_update function. This makes it possible for authenticated attackers, with minimal permissions such as a subscriber, to modify their user role by supplying the 'wpda_role[]' parameter during a profile update. This requires the 'Enable role management' setting to be enabled for the site.
```

## References

- [WPScan.com](https://wpscan.com/vulnerability/7871b890-5172-40aa-88f2-a1b95e240ad4/)
- [NIST](https://nvd.nist.gov/vuln/detail/CVE-2023-1874)

## Script Execution

```bash
# not necessary.
#
# these can be manually input as arguments to the script.
#
# theses exports are for ease-of-use.
export TARGETIP=localhost
export TARGETPORT=80
export WPPATH=wordpress
export WPUSERNAME=myuser
export WPPASSWORD=mypass

python3 cve20231874.py $TARGETIP $TARGETPORT -u $WPUSERNAME -p $WPPASSWORD --path $WPPATH
```
