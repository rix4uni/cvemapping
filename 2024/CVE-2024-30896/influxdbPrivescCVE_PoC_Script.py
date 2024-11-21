import influxdb_client
import argparse
import logging
import sys

argParser = argparse.ArgumentParser()
argParser.add_argument("-t", "--token", type=str, help="Custom or allAccess token to access influx DB instance")
argParser.add_argument("-e", "--endpointUrl", type=str, help="Endpoint Url of influxdb instance (ex. \"https://myInfluxdbInstance:8086/\")")
argParser.add_argument("-v", "--verbose", type=bool, const=True, nargs='?', help="Enable verbose logging - INFO")
argParser.add_argument("-vv", "--vverbose", type=bool, const=True, nargs='?', help="Enable verbose logging - DEBUG")

args = argParser.parse_args()

# Using user retrieved values or default (hardcoded) ones
all_access_token = "<allAccessToken>"
influx_endpoint_url = "<influxdbEndpointUrl>"

# Defining some colors
red = "\033[31m"
yellow = "\033[93m"
purple = "\33[1;95m"
green = "\033[0;92m"
cyan = "\033[96m"
bold ="\033[1m"
endc = "\033[39m"

if args.vverbose == True:
    logging.basicConfig(level=logging.DEBUG)
elif args.verbose == True:
    logging.basicConfig(level=logging.INFO)

logger = logging.getLogger()

if args.token:
    token = args.token
else:
    logger.debug(f"{yellow}User did not set a token, using default one{endc}")
    token = all_access_token

if args.endpointUrl:
    endpointUrl = args.endpointUrl
else:
    logger.debug(f"{yellow}User did not set an endpoint Url for influxdb, using default one{endc}")
    endpointUrl = influx_endpoint_url

logger.info(f"{cyan}Connecting to influx DB instance{endc}")
# Connecting to influxdb instance 
try:
    conn = influxdb_client.InfluxDBClient(
                url=endpointUrl,
                token=token,
                debug=False,
                verify_ssl=True
            )

    # Verify InfluxDB connection
    health = conn.ping()
    if not health:
        logger.error(f"{red}Unable to connect to db instace " + endpointUrl + f"{endc}") 
        print(f"{red}Quitting execution...{endc}")
        sys.exit(1)

except Exception as e:
    logger.error(f"{red}Failed to connect to db instance: " + endpointUrl + " Error: " + str(e) + f"{endc}")
    print(f"{red}Quitting execution...{endc}")
    sys.exit(1)

# Retrieving all current auths
logger.debug(f"{yellow}Retrieving all auth tokens{endc}")
print(f"{cyan}Enumerating current authorizations...{endc}")
try:
    auths = conn.authorizations_api().find_authorizations()
except Exception as e:
    logger.error(f"{red}Unable to retrieve authorizations. ERR: " + str(e) +f"{endc}")
    print(f"{red}Unable to retrieve authorizations. Quitting...{endc}")
    sys.exit(1)
if not auths:
    print(f"{cyan}No Authorization tokens found on the instance{endc}")
    sys.exit(1)
print(f"{cyan}{str(len(auths))} tokens found on the instance{endc}\n")
# Extracting operator token -> Parsing permissions to look for ("org = None" and "authType = write/auths"), not 100% efficiency -> TO OPTIMIZE
logger.debug(f"{yellow}Parsing auth permissions to retrieve operator tokens{endc}")
print(f"{cyan}Enumerating all operator tokens:{endc}")
op_tokens = []
# In order to understand if a token is of type "operator" we need to enumerate all permissions and look for "write/auths" on org 'None' -> Unrescticted access
try:
    for auth in auths:
        if auth.permissions:
            for perm in auth.permissions:
                if perm.action == "write" and perm.resource.org == None and perm.resource.type == "authorizations":
                    op_tokens.append(auth.token)
except Exception as e:
    logger.error(f"{red}Unable to parse permissions on found authorizations. ERR: " + str(e) + f"{endc}")
    print(f"{red}Unable to parse permissions on found authorizations. Quitting execution...{endc}")
    sys.exit(1)

logger.info(f"{cyan}Printing all operator auth tokens{endc}")
print(f"{cyan}{str(len(op_tokens))} operator tokens found.\n\nListing all operator tokens:\n{endc}")
for op_t in op_tokens:
    print(f"{green}{op_t}{endc}")

