# CVE-2022-43144 : Stored-XSS

## Description
A cross-site scripting (XSS) vulnerability in Canteen Management System v1.0 allows attackers to execute arbitrary web scripts or HTML via a crafted payload.

## Impact 
  - Allowing an attacker to hijack the user's session and take over the account.
  - To exploit this vulnerability victim must visit the page where the XXS payload is stored.

## Affected Application link
- https://www.sourcecodester.com/php/15688/canteen-management-system-project-source-code-php.html
- https://www.sourcecodester.com/download-code?nid=15688&title=Canteen+Management+System+Project+Source+Code+in+PHP+Free+Download

## Proof of concept
Once the application is up and running we can log in.

![1_login_page](https://user-images.githubusercontent.com/22985192/200138425-9ea78c19-53bf-44a1-9bcd-ba9fcd91bc1d.png)

We have "Add Invoice" feature with in the application.

![2_add_invoice_feature](https://user-images.githubusercontent.com/22985192/200138432-dcab7f32-aaa5-4921-92a9-6d668a8bcfa3.png)

we can add an invoice and check our entries are made available on the "manage Invoice page".

![3_adding_invoice](https://user-images.githubusercontent.com/22985192/200138453-8006ada3-1a12-424d-9ad1-50fd58dc67a3.png)

![4_invoice_stored_in_application](https://user-images.githubusercontent.com/22985192/200138457-2dc1ed5c-e8af-4859-a5d7-cef67d66e95c.png)

Let's add an invoice with a special characters in the contact field.

![5_data_validation_1](https://user-images.githubusercontent.com/22985192/200138490-eeed493b-2c05-491b-9f1f-d65e88027eeb.png)

The application does not perform any encoding of special characters provided by the user.

![5_data_validation_2](https://user-images.githubusercontent.com/22985192/200138499-1abc665f-45bd-4c55-822e-faac8a7053cb.png)

let's analyze the source and understand how the application is handling provided data.

![10_source_code_1](https://user-images.githubusercontent.com/22985192/200138509-2da2f308-560c-4bd2-93d4-302bedad2c5b.png)

It is clear that the application doesn't perform data validation and trust user-supplied data, we can use the below XSS payload as input which may be stored in the application.

![6_XSS_payload](https://user-images.githubusercontent.com/22985192/200138527-eb5f0fcb-17cf-4b02-8f5a-3569282cae59.png)

Let's analyze the source too if there is any data validation in place while storing the data.

![10_source_code_2](https://user-images.githubusercontent.com/22985192/200138542-c3b36384-bb5d-4ea1-9659-066c5628aa85.png)

The entry provided was added to the database.

![10_source_code_3](https://user-images.githubusercontent.com/22985192/200138547-7fcdf217-455f-4e23-a567-3c63cc717785.png)

We can successfully execute the javascript payload indicating the application is vulnerable to XXS.

![8_Poc](https://user-images.githubusercontent.com/22985192/200138566-b89fb131-f8b8-4aa8-8f55-ce249bf50cf8.png)

![9_poc](https://user-images.githubusercontent.com/22985192/200138579-efc5d9d6-8177-484d-91f8-e51e52a1bd4d.png)

![7_poc](https://user-images.githubusercontent.com/22985192/200138587-26bf7293-6a0d-4a7b-9d72-f3e050ccccd8.png)
