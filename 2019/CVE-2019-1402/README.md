## CorruptQueryAccessWorkaround: Query '' is corrupt

The latest workaround for the [Query is corrupt](https://support.office.com/en-us/article/access-error-query-is-corrupt-fad205a5-9fd4-49f1-be83-f21636caedec) error introduced with CVE-2019-1402 in MS Access.

There are other workarounds out there that need to be applied on an administrative level, e.g. by uninstalling the erroneous update. In contrast to those, the intention of the one provided here is to work by automatically altering the MDB/ACCDB content itself with as little work as possible.

### Note

Microsoft did release a fix for this issue on 2019-12-10 (patch day) that will by default be automatically installed via WSUS etc.
This workaround should therefore be obsolete after the fix got applied and anybody who has used it can call the `RemoveWorkaroundForCorruptedQueryIssue()` function to restore the original application state.

### Instructions

Make sure that either the `Microsoft DAO 3.6 Object Library` (backward compatibility) or `Microsoft Office x.x Access Database Engine Object Library` reference is enabled under `VBA Editor -> Tools -> References` (see [#1](https://github.com/lauxjpn/CurruptQueryAccessWorkaround/issues/1) for further details).

Use the `basWorkaround.bas` module to automatically implement Microsofts suggested workaround (using a query instead of a table). As a precaution, backup your database first.

Call `AddWorkaroundForCorruptedQueryIssue()` to apply the workaround and `RemoveWorkaroundForCorruptedQueryIssue()` to remove it at any time.

`AddWorkaroundForCorruptedQueryIssue()` will add the suffix `_Table` to all non-system tables, e.g. the table `IceCreams` would be renamed to `IceCreams_Table`.

It will also create a new query with the original table name, that will select all columns of the renamed table. In our example, the query would be named `IceCreams` and would execute the SQL `select * from [IceCreams_Table]`.

`RemoveWorkaroundForCorruptedQueryIssue()` does the reverse actions.

I am using this workaround on large projects with 400+ tables of all kinds, including external non-MDB tables (like SQL Server).

In my case I needed to manually rename `USysRibbons_Table` back to `USysRibbons`, as I hadn't marked it as a system table when I created it in the past.

Keep the following things in mind:

- Using a query instead of a table can lead to non-optimized statements being executed against a backend database in specific cases, especially if your original queries that used the tables are either of poor quality or very complex.
- The underlying table *must have* a primary key defined, or it will not be possible to update or insert rows.
- It is possible (depending on your coding style) that this does not cover all your code references (e.g. explicitly using statements like `TableDefs!MyTableName` will require you to do some find and replace for those instances in your code/UI).

### Futher information

- [Born's Tech and Windows World](https://borncity.com/win/2019/11/13/office-november-2019-updates-are-causing-access-error-3340/?unapproved=6359&moderation-hash=597d97fc3d9abf61a4a8c4940f25bbc1#comment-6359)
- [administrator.de (German)](https://administrator.de/content/detail.php?id=514571&token=511#comment-1405456)
- [Microsoft Error and Workaround Description](https://support.office.com/en-us/article/access-error-query-is-corrupt-fad205a5-9fd4-49f1-be83-f21636caedec)
- [Microsoft Forum: The CVE-2019-1402 updates (KB4484119, etc.) break Access 2010/2013/2016/365: Query '' is corrupt](https://social.msdn.microsoft.com/Forums/office/en-US/7e7f24cc-f1f3-43f8-a9a2-45b77812b211/the-cve20191402-updates-kb4484119-etc-break-access-201020132016365-query-is-corrupt?forum=accessdev)
- [StackOverflow](https://stackoverflow.com/questions/58832269/getting-error-3340-query-is-corrupt-while-executing-queries-docmd-runsql)

### Error message in other languages

- German: Abfrage '' ist beschädigt
