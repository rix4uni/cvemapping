# CVE-2024-53617: Stored XSS in LibrePhotos before version 2024w47

LibrePhotos before version 2024w47 has a stored XSS (Cross-site Scripting) allows attackers to takeover any account via uploading an HTML file on behalf of the admin user using IDOR in file upload.

References:
- https://github.com/LibrePhotos/librephotos/pull/1476
- https://github.com/LibrePhotos/librephotos/commit/32237ddc0b6293a69b983a07b5ad462fcdd6c929