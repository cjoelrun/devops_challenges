#!/usr/bin/env python
import pyrax

pyrax.keyring_auth()
cs = pyrax.cloudservers

cs.servers.create("julian_web1", "8a3a9f96-b997-46fd-b7a8-a9e740796ffd", 2)
cs.servers.create("julian_web2", "8a3a9f96-b997-46fd-b7a8-a9e740796ffd", 2)
cs.servers.create("julian_web3", "8a3a9f96-b997-46fd-b7a8-a9e740796ffd", 2)
