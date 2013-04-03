import novaclient.client
import novaclient.exceptions
import os
import argparse
import sys
import time
from pprint import pprint

"""
A script that builds three 512 MB Servers that follow a similar naming
convention and returns the IP and login credentials for each server.
"""

# Acquire arguments
parser = argparse.ArgumentParser()
parser.add_argument('--user', action="store", dest="user",
                    required=False, default=os.getenv("OS_USERNAME"),
                    help="Openstack username")
parser.add_argument('--password', action="store", dest="password",
                    required=False, default=os.getenv("OS_PASSWORD"),
                    help="Openstack password")
parser.add_argument('--tenant_name', action="store", dest="tenant_name",
                    required=False, default=os.getenv("OS_TENANT_NAME"),
                    help="Openstack Tenant Name")
parser.add_argument('--url', action="store", dest="url", required=False,
                    default=os.getenv("OS_AUTH_URL"),
                    help="URL of OpenStack endpoint")
parser.add_argument('--server_name', action="store", dest="server_name",
                    required=False, default="devops",
                    help="Name for servers to create")
parser.add_argument('--num_servers', action="store", dest="num_servers",
                    required=False, default=3,
                    help="Number of servers to create")
args = parser.parse_args()
# Make sure all arguments have been defined
if not all(vars(args)[k] for k in vars(args).keys()):
    parser.print_usage()
    print "Undefined: " + ", ".join(k for k in vars(args).keys() if not vars(args)[k])
    sys.exit(1)

# Acquire a nova client
nova = novaclient.client.Client('2', args.user, args.password, args.tenant_name, args.url)

# Acquire a flavor with 512 MB
flavor = next(flavor for flavor in nova.flavors.list() if flavor.ram == 512)

# Acquire an Ubuntu Precise image
image = next(image for image in nova.images.list() if image.name == "precise")

# Create the servers
servers = []
for n in range(args.num_servers):
    servers.append(nova.servers.create(name="%s-%s" % (args.server_name, n+1), 
                                 flavor=flavor,
                                 image=image))

# Wait for networking to happen to print credentials
for server in servers:
    password = server.adminPass
    for wait in range(100):
        try:
            print "%s: %s" % (server.networks['public'][0], password)
        except (KeyError, AttributeError) as e:
            time.sleep(1)
            server = nova.servers.get(server.id)
        else:
            break
    else:
        print "server error: %s" % server

    
