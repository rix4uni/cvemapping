# CVE-2020-29156
woocommerce wordpress plugin - Affected Version: V 4.5.2 [CVE-2020-29156]

#WooCommerce before 4.7.0 allows remote attackers to view the status of arbitrary orders via the order_id parameter in a fetch_order_status

#Vulnerability Type - Incorrect Access Control

#Vendor of Product - woocommerce

#Affected Product Code Base - woocommerce wordpress plugin - Affected Version: V 4.5.2 ( Fixed in 4.7.0)

#Affected Component - https://[target-site].com/wp-admin/admin-ajax.php?action=fetch_order_status&order_id=[1234]

#Attack Type - Local

#Impact Information Disclosure - true


#Attack Vectors
> - Go to website that is using woo-commerce plugin 
> - Please make order and malicious user will get order-ID
> - Go to this link and insert his order-ID `` https://[target-site].com/wp-admin/admin-ajax.php?action=fetch_order_status&order_id=[order-ID] ''
> - Response will be order status, i.e, processing, pending, trash, cancelled, etc.
> - Malicious user can view unauthorized  order status of other customer's order status by changing '' order-ID ''
