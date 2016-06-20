#!/usr/bin/env python

print "Content-type: text/html"
print
print "<html><head><title>Situation snapshot</title></head>"
print "<body><pre>"

import sys
sys.stderr = sys.stdout
import os
from cgi import escape

print "<strong>Python %s</strong>" % sys.version

for k in sorted(os.environ.keys()):
    print "%s\t%s" % (escape(k), escape(os.environ[k]))

print "</pre></body></html>"
