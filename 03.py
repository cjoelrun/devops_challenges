#!/usr/bin/env python
import pyrax

pyrax.keyring_auth()
cf = pyrax.cloudfiles

folder = raw_input("Specify path: ")
upload_key, total_bytes = cf.upload_folder(folder, container="test")