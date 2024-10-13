# Metabase_CVE-2021-41277

### Description
Metabase is an open source data analytics platform. In affected versions a security issue has been discovered with the custom GeoJSON map (`admin->settings->maps->custom maps->add a map`) support and potential local file inclusion (including environment variables). URLs were not validated prior to being loaded. This issue is fixed in a new maintenance release (0.40.5 and 1.40.5), and any subsequent release after that. If you&#8217;re unable to upgrade immediately, you can mitigate this by including rules in your reverse proxy or load balancer or WAF to provide a validation filter before the application.


#### Follow us 
#### [Vulnmachines](https://www.twitter.com/vulnmachines)
#### [YouTube](https://www.youtube.com/c/vulnmachines)
#### [Twitter](https://www.twitter.com/vulnmachines)
#### [Facebook](https://www.facebook.com/vulnmachines)
#### [LinkedIn](https://www.linkedin.com/company/vulnmachines)
