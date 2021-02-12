# Automation Scripts

## FirewallIpAllowListUpdate

Script to update firewall address list in Mikrotik RouterOS for use in firewall rules

My firewall only allows inbound traffic from cloudflare (for remote access of self-hosted services). The firewall rule is configured to only forwards ports if the source address is in the "cloudflare" address list. This script gets the current IP ranges from the CloudFlare API and makes any necessary updates to the RouterOS list
