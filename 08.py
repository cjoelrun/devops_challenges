"""
A script that will create a static webpage served out of Cloud Files. 
Creates a new container with cdn enabled to serve an index file. 
Creates an index file object, uploads the object to the container, and
creates a CNAME record pointing to the CDN URL of the container.
"""
