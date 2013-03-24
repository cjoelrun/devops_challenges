#!/usr/bin/env python
import pyrax

pyrax.keyring_auth()
dns = pyrax.cloud_dns

fqdn = raw_input('Fully-Qualified Domain Name: ') 
email_addr = raw_input('E-mail Address: ')
ip_addr = raw_input('IP Address: ')

dns.create(name=fqdn,
           emailAddress=email_addr,
           records=[{
                    "type":"A",
                    "name": fqdn,
                    "data": ip_addr
           }])