# CVE-2024-33453


---

# Sensitive Data Exposure via Object Level Access Control in esp-idf

## Description

A Buffer Overflow vulnerability in the `esp-idf` framework version 5.1, used by some Schoolbox products, allows a remote attacker to obtain sensitive information through improper object-level access control. This vulnerability is triggered by manipulating the `id` parameter linked to the `externalId` component, leading to unauthorized access to sensitive data.

## Additional Information

The esp-idf framework has a vulnerability in the `externalId` component that results in improper object-level access control. This issue allows authenticated users to exploit the system by changing the `id` parameter in the URL to access data belonging to other users.

### Vulnerable URL Example

An authenticated user can change the `id` parameter in the URL to access different users' information:

- Original URL: `https://example.com/search/user?id=9682`
- Modified URL: `https://example.com/search/user?id=9683`

This lack of proper access control could lead to sensitive information being exposed unintentionally.

## Vulnerability Details

- **Vulnerability Type:** Incorrect Access Control
- **Vendor of Product:** Espressif Systems (esp-idf)
- **Affected Product Code Base:** esp-idf - 5.1
- **Vulnerable Parameter:** `id`
- **Vulnerable Component:** `externalId`
- **Attack Type:** Remote

## Impact

This vulnerability allows authenticated users to access and potentially manipulate sensitive data belonging to other users by altering the `id` parameter, leading to significant information disclosure risks.

## Attack Vectors

To exploit this vulnerability, an attacker must be authenticated in the system that uses the esp-idf framework. By modifying the `id` parameter in the URL, the attacker can access data not intended for their account, thus exposing sensitive user information.

## Mitigation

To mitigate this vulnerability, it is crucial to implement robust object-level access controls within the esp-idf framework to restrict access based on user roles and permissions. Additionally, always validate and sanitize user inputs, ensuring URL parameters like `id` do not control access to sensitive information.

---

**Disclaimer:** This proof of concept is intended for educational and research purposes only. Unauthorized exploitation of this vulnerability may be illegal and is punishable by law.

---

This README outlines the vulnerability details and provides a clear path for understanding and potentially mitigating the issue.  
