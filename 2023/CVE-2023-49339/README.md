# CVE-2023-49339 Security Vulnerability Report: Ellucian Banner System

## Introduction

This document outlines a critical security vulnerability found in the Ellucian Banner System, particularly in version 9.17 and earlier versions. The vulnerability has been identified in systems used by various universities in Saudi Arabia, potentially exposing sensitive student data.

## Vulnerability Details

- **Type:** Insecure Direct Object Reference (IDOR)
- **Endpoint Affected:** `/StudentSelfService/ssb/studentCard/retrieveData`
- **Parameter in Question:** `bannerId`
- **Impact:** Unauthorized exposure of sensitive student data, including personal identifiers, academic records, and contact information.

### Steps to Reproduce

1. Log in to the Banner system using legitimate user credentials.
2. Navigate to the URL endpoint that retrieves student card information.
3. Modify the `bannerId` parameter in the URL to a different student's identifier.
4. Observe that the system displays information for the altered `bannerId`, bypassing necessary authorization checks.

## Affected Versions

The vulnerability impacts the Ellucian Banner System, version 9.17 and earlier. It is crucial for institutions using these versions to take immediate action to mitigate the risks.

## Recommended Actions

1. **Immediate Patching:** Ellucian should urgently develop and release a security patch for the affected versions.
2. **Enhanced Authorization Checks:** Implement strict authorization checks on the affected endpoint.
3. **System Audit:** Conduct a thorough audit to identify and fix similar vulnerabilities.
4. **Regular Updates and Training:** Establish protocols for regular system updates and user training on security best practices.
5. **Ongoing Monitoring:** Continuously monitor the system for signs of unauthorized access or exploitation attempts.


## CVE Submission

This vulnerability has been registered with the CVE ID: CVE-2023-49339. Further details and updates regarding the vulnerability will be provided as they become available.

## By

Abdulaziz Naif Almadhi

---
