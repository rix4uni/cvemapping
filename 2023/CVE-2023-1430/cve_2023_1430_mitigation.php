<?php


/**
 * CVE-2023-1430 Mitigation
 * 
 * Add the following snippet to your child-theme’s functions.php file (without
 * the <?php tag above this comment). If you don’t have a child-theme, you must 
 * add this snippet to your theme’s functions.php file after every theme update. 
 * Remeber to delete the snippet after installing the official patch when it is 
 * available.
 * 
 * WARNING! This snippet comes with no warranty and no support. The snippet does
 * not patch the vulnerability. It just prevents vulnerability exploitation.
 * The snippet is made publicly available since WPManageNinja hasn’t been able 
 * to patch the vulnerability within the 90-day responsible disclosure window. 
 * Karl Emil Nikka and Nikka Systems are not affiliated with WPManageNinja. This
 * snippet is neither endorsed nor supported by WPManageNinja.
 * 
 * Author:       Karl Emil Nikka
 * Author URI:   https://nikkasystems.com
 * License:      GPLv2 or later
 * License URI:  https://www.gnu.org/licenses/gpl-2.0.html
 * Text Domain:  cve-2023-1430
 * Version:      1.0
 */
 

/**
 * Remove vulnerable FluentCRM forms
 * 
 * Replaces the content on the unsubscribe page and page for managing
 * preferences with an error message telling contacts to reach out to 
 * customer support via email. 
 * 
 * @param   void
 * @return  void
 */
 
function cve_2023_1430_remove_vulnerable_fluent_crm_forms() {
    
    // Define text and variables.
    $email_address = get_bloginfo( 'admin_email' );
    $email_title = sprintf( __( 'Send email to %s.', 'cve-2023-1430' ), $email_address );  
    $email_link = '<a href="mailto:' . $email_address . '" . title="' . esc_attr( $email_title ) .'">' . $email_address . '</a>';
    $error_title = esc_html__( 'Temporarily disabled preferences form', 'cve-2023-1430' );
    $error_body = esc_html__( 'The preferences form is temporarily disabled. Please reach out to us via email (%s) to edit your preferences or unsubscribe from our newsletter.', 'cve-2023-1430' );
    
    // Crete error message. 
    $out  = '</head>';
    $out .= '<body>';
    $out .= '<h1>' . $error_title . '</h1>';
    $out .= '<p>' . sprintf( $error_body, $email_link ) . '</p>';
    $out .= '</body>';
    $out .= '</html>';
    
    // Output error message and kill process. 
    echo $out;
    exit();
}

add_action( 'fluent_crm/manage_subscription_head', 'cve_2023_1430_remove_vulnerable_fluent_crm_forms', 20, 0 );
add_action( 'fluent_crm/unsubscribe_head', 'cve_2023_1430_remove_vulnerable_fluent_crm_forms', 20, 0 );


/**
 * Disable public FluentCRM shortcode
 * 
 * Replaces the content of the fluentcrm_pref shortcode with an error message
 * if displayed for non-logged-in visitors. CVE-2023-1430 cannot be expolited
 * from the shortcode if the contact is a logged-in user. 
 * 
 * @param   false|string    Short-circuit return value. 
 * @param   string          Shortcode name.
 * @param   array|string    Shortcode attributes array or empty string.
 * @param   array           Regular expression match array.
 * @return  false|string    Filtered shortcode output. 
 */
 
function cve_2023_1430_disable_public_fluent_crm_shortcode( $output, $tag, $attr, $m ) {

    // Return if the filtered tag isn’t fluentcrm_pref or if the user is logged in.
    if ( $tag !== 'fluentcrm_pref' || is_user_logged_in() === true ) {
        return $output;
    }

    // Define text and variables. 
    $link_url = wp_login_url();
    $link_title = __( 'Go to login page.', 'cve-2023-1430' );
    $link = '<a href="' . $link_url . '" title="' . esc_attr( $link_title ) . '">' . esc_html_x( 'log in', 'Verb, part of link.', 'cve-2023-1430' ) . '</a>';
    $error_body = esc_html__( 'The public preference form is temporarily disabled. Please %s to edit your preferences.', 'cve-2023-1430' );
    
    // Return new error message as output. 
    $output = '<p>' . sprintf( $error_body, $link ) . '</p>';
    return $output;
}

add_filter( 'pre_do_shortcode_tag', 'cve_2023_1430_disable_public_fluent_crm_shortcode', 10, 4 );