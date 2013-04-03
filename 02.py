import novaclient.client
from novaclient.v1_1 import shell
import os
import argparse
import sys
import time


"""
A script that clones a server (takes an image and deploys the image as
a new server.
"""

# Acquire arguments
parser = argparse.ArgumentParser()
parser.add_argument('--user', action="store", dest="user",
                    default=os.getenv("OS_USERNAME"),
                    help="Openstack username")
parser.add_argument('--password', action="store", dest="password",
                    default=os.getenv("OS_PASSWORD"),
                    help="Openstack password")
parser.add_argument('--tenant_name', action="store", dest="tenant_name",
                    default=os.getenv("OS_TENANT_NAME"),
                    help="Openstack Tenant Name")
parser.add_argument('--url', action="store", dest="url",
                    default=os.getenv("OS_AUTH_URL"),
                    help="URL of OpenStack endpoint")
parser.add_argument('--server_name', action="store", dest="server_name",
                    help="Name of server to clone")
parser.add_argument('--flavor', action="store", dest="flavor",
                    help="Flavor the clone should be")
args = parser.parse_args()
# Make sure all needed arguments have been defined
undefined = list(k for k in vars(args).keys() if not vars(args)[k])
if undefined:
    parser.print_usage()
    print "Undefined: " + ", ".join(undefined)
    # Print the servers and flavors if we can
    if not set(undefined) - set(['server_name', 'flavor']):
        nova = novaclient.client.Client('2', args.user, args.password, args.tenant_name, args.url)
        servers = "\n\t".join(server.name for server in nova.servers.list() if server.status == "ACTIVE")
        flavors = "\n\t".join(flavor.name for flavor in nova.flavors.list())
        print "servers:%s\nflavors:%s" % (servers, flavors)
    sys.exit(1)

# Acquire a nova client
nova = novaclient.client.Client('2', args.user, args.password, args.tenant_name, args.url)

# Acquire a server
try:
    server = next(server for server in nova.servers.list() if server.name == args.server_name)
except StopIteration:
    print "Error: No server exists with name: %s" % args.server.name
    servers = (server.name for server in nova.servers.list() if server.status == "ACTIVE")
    print "servers:%s" % (servers, flavors)
    sys.exit(1)
    
# Create an image and wait for active status
image_name = "%s-%s" % (server.name, time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime()))
image = server.create_image(image_name)
shell._poll_for_status(nova.images.get, image, 'snapshotting', ['active'])

# Create the clone
flavor = nova.flavors.get(server.flavor['id'])
new_server = nova.servers.create(name="%s-clone" % server.name,
                                 flavor=flavor,
                                 image=nova.images.get(image))

# Wait for networking to happen to print credentials
password = new_server.adminPass
for wait in range(100):
    try:
        print "%s: %s" % (new_server.networks['public'][0], password)
    except (KeyError) as e:
        time.sleep(1)
        new_server = nova.servers.get(new_server.id)
    else:
        break
else:
    print "Error: server networking error: %s" % server
    sys.exit(1)
