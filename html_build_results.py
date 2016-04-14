
#!/usr/bin/env python

import sqlite3
from mako.template import Template
import re


class UorDescription:
    UOR_REGEX = "([\w\d.]*)-([\w\d.]*)-([\w\d.]*)-"\
                "([\w\d.]*)-([\w\d.]*)-([\w\d.]*)"
    
    def __init__(self, uor):
        match = re.match(self.UOR_REGEX, uor)
        if (match is None):
            raise Exception("Unable to parse UOR: {}".format(uor))
        
        self.os_type = match.group(1)
        self.os_name = match.group(2)
        self.cpu_type = match.group(3)
        self.os_version = match.group(4)
        self.compiler_type = match.group(5)
        self.compiler_version = match.group(6)
    
    def __str__(self):
        return "{}-{}-{}-{}-{}-{}".format(self.os_type,
                                          self.os_name,
                                          self.cpu_type,
                                          self.os_version,
                                          self.compiler_type,
										  self.compiler_version)
										  
										  
value = [
   ["unix-linux-x86_64-2.6.18-gcc-4.3.2", "BUILD", 7 ],
   ["unix-linux-x86_64-2.6.18-gcc-4.9.2", "BUILD", 7 ],
   ["unix-linux-x86_64-2.6.18-gcc-4.9.2", "b ild", 7 ],
]

val = UorDescription("unix-linux-x86_64-2.6.18-gcc-4.3.2")
print(Template(filename="./results_page.mako").render(table=value))
print("Parsed: " + str(val))