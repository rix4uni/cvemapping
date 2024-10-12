# CVE-2023-48984

An issue in vicohome vicohome v.2.22.7 allows a remote attacker to execute arbitrary code via the xml/file_paths.xml component.

An insecure file path provider is a vulnerability in Android apps where a file path is exposed to other apps or users, which could potentially compromise sensitive data or allow unauthorized access to system resources.

By making your app more secure, you help preserve user trust and device integrity, so to protect your app from this vulnerability.

The application uses a content provider androidx.core.content.FileProvider that exposes a file provider android.support.FILE_PROVIDER_PATHS configured in res/xml/file_paths.xml file.
The file provider has an external-path type that allows the attackers to access external storage like an SD card.

<paths>
  <external-path name="external_storage_root" path="."/>
  <cache-path name="getCacheDir" path="."/>
</paths>

The application exposes a file provider using androidx.core.content.FileProvider

Credit: Lukasz Studniarz

