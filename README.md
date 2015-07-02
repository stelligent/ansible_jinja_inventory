Ansible jinja2 inventory provider
=================================

This is a simple dynamic inventory provider for Ansible
that parses a text inventory file (inventory\_template.ini)
using jinja2. Environment variables are made available
to the template. The file is in a YAML format.

The use case is the need to provide inventories to
Ansible of desired state ("I want 5 web servers and 2
database instances") with the ability to avoid copying
and pasting (using jinja2 loops).

As well, the parsed format is YAML, which you may find to
be slightly more robust that the default Ansible
inventory file format.

