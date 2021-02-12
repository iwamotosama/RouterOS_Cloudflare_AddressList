#################################################################################################
# Script to update firewall address list in Mikrotik RouterOS for use in firewall rules
# 
# Firewall only allows inbound traffic from cloudflare (for remote access ofself-hosted 
# services). The firewall rule only forwards ports if the source address is in the "cloudflare"
# address list. This script gets the current IP ranges from the cloudflare API and makes any
# necessary updates to the RouterOS list
#################################################################################################
import requests
from configparser import ConfigParser
from RouterOS_API.routeros_api import Api


print("Starting Cloudflare IP range update")

config = ConfigParser()
config.read('.config')
rosConfig = config['RouterOS']

# cloudflare API info: https://api.cloudflare.com/#cloudflare-ips-properties
cloudflareApiUrl = "https://api.cloudflare.com/client/v4/ips"
print("Requesting Cloudflare IP range: " + cloudflareApiUrl)
retVal = requests.get(cloudflareApiUrl)
data = retVal.json()

cfIps = data['result']['ipv4_cidrs']
print("Cloudflare IPv4 CIDRs:")
print(*cfIps, sep="\n")

routerApi = Api(rosConfig['RosApiAddress'], user=rosConfig['RosApiUsername'], password=rosConfig['RosApiPassword'], use_ssl=True)

# get existing ip list
rosRet = routerApi.talk('/ip/firewall/address-list/print\n?list=cloudflare\n=.proplist=.id,address')

print("Current IPv4 CIDRs in RouterOS 'Cloudflare' list:")
print(*rosRet, sep="\n")

# temporary list of valid cloudflare IPs already in RouterOS
rosIps = []
# addresses that need to be added to RouterOS
addIps = []
# RouterOS address list IDs to be removed -- these are no longer cloudflare addresses
removeIds = []

for entry in rosRet:
    address = entry['address']
    if(address in cfIps):
        # add to temporary list so we can compare cloudflare IPs to what is already in RouterOS
        rosIps.append(address)
    else:
        # this address is no longer used by cloudflare, add its ID to the remove list
        removeIds.append(entry['.id'])

for address in cfIps:
    if(not address in rosIps):
        # this address is not in the RouterOS cloudflare list, add it to the add list
        addIps.append(address)

print("The following entries will be removed from RouterOS address list:")
print(*removeIds, sep=', ')

for id in removeIds:
    routerApi.talk("/ip/firewall/address-list/remove\n=.id=" + id)

print("The following address will be added to RouterOS address list:")
print(*addIps, sep=', ')

for address in addIps:
    routerApi.talk("/ip/firewall/address-list/add\n=list=cloudflare\n=address=" + address)

print("Update complete")
routerApi.close()