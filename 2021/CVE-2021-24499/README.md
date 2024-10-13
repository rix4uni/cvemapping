# CVE-2021-24499
Mass exploitation of CVE-2021-24499 unauthenticated upload leading to remote code execution in `Workreap` theme.

The AJAX actions `workreap_award_temp_file_uploader` and `workreap_temp_file_uploader` did not perform nonce checks, or validate that the request is from a valid user in any other way. The endpoints allowed for uploading arbitrary files to the `uploads/workreap-temp` directory. Uploaded files were neither sanitized nor validated, allowing an unauthenticated visitor to upload executable code such as php scripts.
