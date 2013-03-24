#!/usr/bin/env python
import pyrax

pyrax.keyring_auth()
cs = pyrax.cloudservers

servers = cs.servers.list()
print servers
parent = raw_input('Parent server: ')

parent_server = next(server for server in servers if server.name == parent)
cs.servers.create_image(parent_server.id, "parent")
parent_image = next(image for image in cs.images.list() if image.name == "parent")
pyrax.utils.wait_until(parent_image, 'status', ['ACTIVE', 'ERROR'], interval=45, attempts=0, verbose=True)

cs.servers.create("CHILD", parent_image.id, 2) 

print 'Child server created.'