# CVE-2017-8295

Wordpress has a password reset feature that contains a vulnerability which
might in some cases allow attackers to get hold of the password reset link
without previous authentication. 
Such attack could lead to an attacker gaining unauthorised access to a 
victim's WordPress account.


vulnerable Code 
------[ wp-includes/pluggable.php ]------

...

if ( !isset( $from_email ) ) {
        // Get the site domain and get rid of www.
        $sitename = strtolower( $_SERVER['SERVER_NAME'] );
        if ( substr( $sitename, 0, 4 ) == 'www.' ) {
                $sitename = substr( $sitename, 4 );
        }

        $from_email = 'wordpress@' . $sitename;
}

