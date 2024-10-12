# CVE-2023-45503 Vulnerability Details

## Overview

In Macrob7 Macs Framework Content Management System (CMS) versions 1.1.4f and prior, insecure handling of user input leads to 16 SQL injection vulnerabilities. The ability to execute arbitrary SQL queries can lead to private data being leaked including users' password hashes and the ability to modify other users' credentials and privilege level. The impact can include privilege escalation and potential remote code execution (RCE).

A spreadsheet outlining each affected endpoint, vulnerable parameter, and the vulnerable functions can be found at [this link](https://docs.google.com/spreadsheets/d/1AzXspN8oBAJ80YQxfN44bpbOuNzA3PZEccQ6IGQMs5E/edit?usp=sharing).

**CWE Classification:** CWE-89: Improper Neutralization of Special Elements used in an SQL Command ('SQL Injection')

**Reported By:** Ally Petitt 

**Affected Product**: Macrob7 Macs CMS

**Affected Versions**: 1.1.4f and prior

## Technical Details
In 16 instances that I spotted, user input was recieved without proper sanitization or parameterization. For instance, in the "Forgot Password" functionality of this CMS, an email address is requested.

_Application/plugins/CMS/controllers/CMS.php:224_
```
    public function forgotPasswordProcess()
    {
      $this->loadModels();
      $emailAddress = Post::getByKey('emailAddress');

      $user = $this->usersModel->getUserByEmailAddress($emailAddress);
```

The email address is then passed into the method `getUserByEmailAddress()`, which passes the email to `selectSingle()`, a method that does not properly protect against injected SQL queries.

_Application/plugins/CMS/models/Users_Model.php:41_
```
    public function getUserByEmailAddress($emailAddress)
    {
       return $this->selectSingle( $this->getCMSTableNameUsers(), array('EmailAddress'=>$emailAddress));
    }
```

Then, `selectSingle()` calls to `select()` with the passed user input.

_Application/core/DB.php:200_
```
    public function selectSingle($tableName, array $where = array(), array $fields = array('*'))
    {
      $return = $this->select($tableName, $where, $fields);

      $single = NULL;

      if( count($return) > 0 )
        $single = $return[0];

      return $single;
    }
```

The vulnerable `select()` function proceeds to concatenate the parameters passed into it into a SQL query that is subsequently executed. 

_Application/core/DB.php:186_
```
    public function select($tableName, array $where = array(), array $fields = array('*'))
    {      
      $fieldsString = $this->generatePair($fields, ',');
      $whereString = $this->generateKeyValuePair($where, '=', 'AND');

      $sql = 'SELECT '.$fieldsString.' FROM '.$tableName;

      if($whereString !='')
        $whereString = ' WHERE '.$whereString;

      $sql = $sql.' '.$whereString.';';     
      return $this->execute($sql)->fetchAll($this->returnType, $this->className);
    }
```

Due to the lack of input sanitization, validation, and parameterization, this function remains vulnerable to SQL injection attacks.


## Mitigation
Unfortunately, a lack of maintenance on this CMS means that a patched update is unavailable. Individual users may modify the code to contain parameterized SQL queries as opposed to relying on concatenation to pass user input into the database. Prepared statements are an example of a mitigation that can accomplish this.



