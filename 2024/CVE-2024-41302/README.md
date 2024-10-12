# CVE-2024-41302-Bookea-tu-Mesa-is-vulnerable-to-SQL-Injection-
Bookea-tu-Mesa is susceptible to a SQL Injection (SQLi) vulnerability. This flaw allows attackers to inject malicious SQL commands that can manipulate the database, potentially compromising the application's data integrity and security.

<B>Steps to Reproduce:</B>

1. Go to http://localhost/Bookea-tu-Mesa/ReservationTable.php.
2. In the search field, type the following SQL injection payload: ''"+UNION+SELECT+VERSION(),NULL,NULL,NULL,NULL,NULL,NULL,NULL#'.
3. The query will show the database version, demonstrating the SQL injection vulnerability.
   ![alt text](https://github.com/patrickdeanramos/Bookea-tu-Mesa-is-vulnerable-to-SQL-Injection-/blob/main/SQli%20Bookea-tu-Mesa.png?raw=True)

<B>Vulnerable Code:</B><br>
The vulnerability exists in insert_reservation.php at the following lines:
Line 40: $query = "SELECT * FROM reservaciones WHERE RestaurantName LIKE '%$search_query%' OR FullName LIKE '%$search_query%'";
Line 41: $result = $conex->query($query);
Line 87:$result->free();

<B>Suggested Fix:</B><br>
Use prepared statements with parameterized queries to prevent SQL injection. Here is the revised code:
// insert_reservation.php
$query = "SELECT * FROM reservaciones WHERE RestaurantName LIKE ? OR FullName LIKE ?";
$stmt = $conex->prepare($query);
$search_with_wildcards = '%' . $search_query . '%';
$stmt->bind_param('ss', $search_with_wildcards, $search_with_wildcards);
$stmt->execute();
$result = $stmt->get_result();
$stmt->close();

Authors:<br>
Patrick Dean Ramos<br>
Nathu Nandwani<br>
Junnair Manla<br>
Kevin Rosales<br>
Steve Nyan<br>
Shanavas Shakeer<br>
Lani Lambert<br>
