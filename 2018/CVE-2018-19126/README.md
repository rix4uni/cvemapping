# PrestaShop Back Office Remote Code Execution (CVE-2018-19126)

This is the PoC for CVE-2018-19126, chaining multiple vulnerabilities in PrestaShop Back Office to trigger deserialization via phar to achieve remote code execution. 

Prerequisite:
- PrestaShop 1.6.x before 1.6.1.23 or 1.7.x before 1.7.4.4.
- Back Office account (logistician, translator, salesman, etc.).

![](demo.gif)

PrestaShop release note: http://build.prestashop.com/news/prestashop-1-7-4-4-1-6-1-23-maintenance-releases/

Vulnerable package link: https://assets.prestashop2.com/en/system/files/ps_releases/prestashop_1.7.4.3.zip

## WARNING

FOR EDUCATIONAL PURPOSES ONLY. DO NOT USE THIS SCRIPT FOR ILLEGAL ACTIVITIES. THE AUTHOR IS NOT RESPONSIBLE FOR ANY MISUSE OR DAMAGE.

## Example

You need `php` with curl extension and set `phar.readonly = Off` in `php.ini` to run the exploit.

```
# Download repository
wget https://github.com/farisv/PrestaShop-CVE-2018-19126/archive/master.zip -O PrestaShop-CVE-2018-19126.zip
unzip PrestaShop-CVE-2018-19126.zip
cd PrestaShop-CVE-2018-19126-master

# Run the exploit
# Usage: php exploit.php back-office-url email password func param
php exploit.php http://127.0.0.1/admin-dev/ salesman@shop.com 54l35m4n123 system 'cat /etc/passwd'
```

Note that the upload directory will be renamed and you can't upload the malicious phar file again if the folder name is not reverted. You might want to execute reverse shell to gain persistence RCE or include the command to rename the folder again in your payload (you need to know the path to the upload directory).

## Explanation

We can achieve [implicit deserialization with phar wrapper](https://cdn2.hubspot.net/hubfs/3853213/us-18-Thomas-It%27s-A-PHP-Unserialization-Vulnerability-Jim-But-Not-As-We-....pdf) via `getimagesize()` function in `[back-office-path]/filemanager/ajax_calls.php`.

https://github.com/PrestaShop/PrestaShop/commit/4c6958f40cf7faa58207a203f3a5523cc8015148#diff-0f03d65f71cdd8eeb12913a97a6b8945

```php
case 'image_size':
    if (realpath(dirname(_PS_ROOT_DIR_.$_POST['path'])) != realpath(_PS_ROOT_DIR_.$upload_dir)) {
        die();
    }
    $pos = strpos($_POST['path'], $upload_dir);
    if ($pos !== false) {
        $info = getimagesize(substr_replace($_POST['path'], $current_path, $pos, strlen($upload_dir)));
        echo json_encode($info);
    }
```

We need to find the way so `getimagesize()` is called with phar wrapper URL as parameter by bypassing certain checks.

First check with `realpath()` is quite strict.

```php
if (realpath(dirname(_PS_ROOT_DIR_.$_POST['path'])) != realpath(_PS_ROOT_DIR_.$upload_dir)) {
    die();
}
```

The `$upload_dir` variable is come from `config.php`, which is set with `$upload_dir = Context::getContext()->shop->getBaseURI().'img/cms/';` by default. We can't use `phar://[string]` in `$_POST['path']` because `realpath(dirname(_PS_ROOT_DIR_.$_POST['path']))` will return `false` because it's not exist.

There is exist another vulnerability (CVE-2018-19125) which allows user to delete or rename `$upload_dir`. If `$upload_dir` directory is not exist, `realpath(_PS_ROOT_DIR_.$upload_dir)` will return `false` and we can bypass this check because `realpath(dirname(_PS_ROOT_DIR_.$_POST['path']))` is also `false`. This vulnerability is discovered during code review when trying to find the way to bypass :).

In short, CVE-2018-19125 allows the `path` parameter in call to `delete_folder` or `rename_folder` action in `execute.php` to be empty so the application will delete/rename the `$upload_dir` instead.

The second check is simple, the `$_POST['path']` need to contains `$upload_dir`.

```php
$pos = strpos($_POST['path'], $upload_dir);
if ($pos !== false) {
```

We can just append `/img/cms/` in the phar URL after the file path to phar file because if the directory is not exist inside the phar archive, the deserialization is still occurs. The `substr_replace($_POST['path'], $current_path, $pos, strlen($upload_dir))` will only replace `/img/cms/` to the absolute path (`$current_path`) of that folder (e.g. `/var/www/html/img/cms/` if the application is installed in `/var/www/html/`).

Because we can control the `getimagesize()` function to process a phar wrapper URL, we need to upload the malicious phar file to the server. By default, FileManager in PrestaShop only allows 'jpg', 'jpeg', 'png', 'gif', 'bmp', 'tiff', 'svg', 'pdf', 'mov', 'mpeg', 'mp4', 'avi', 'mpg', 'wma', 'flv', and 'webm' as extension. We can just craft the payload and save it with valid extension. We can use `Monolog` gadget chains from PHPGGC (https://github.com/ambionics/phpggc/blob/master/gadgetchains/Monolog/RCE/1/) as it is used by PrestaShop.

Final exploitation steps:
1. Craft the malicious phar file and save with valid extension (e.g. phar.pdf).
2. Upload the phar.pdf to FileManager.
3. Trigger the vulnerability to rename the upload directory to another name (e.g. renamed).
4. Call the `image_size` action with `phar://../../img/renamed/phar.pdf/img/cms/` as `path` parameter.
5. Deserialization payload in phar.pdf will be executed.

The `exploit.php` script will automatically do all steps.

Remember that the upload directory is renamed in step 3 and you can't upload the malicious phar file again if the folder name is not reverted. You might want to use reverse shell as payload or include the command to rename the folder again in the payload (you need to know the path to the upload directory).
