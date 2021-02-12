## RouterOS Firewall Cloudflare Address List Updater

Script to update firewall address list 'cloudflare' in Mikrotik RouterOS with current cloudflare IP ranges

The firewall rules can configured to only forwards ports if the source address is in the "cloudflare" address list. This script gets the current IP ranges from the CloudFlare API and makes any necessary updates to the RouterOS list.
