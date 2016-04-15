#!/usr/bin/env python

import re

class UplidDescription:
    UPLID_REGEX = "([\w\d.]*)-([\w\d.]*)-([\w\d.]*)-"\
                "([\w\d.]*)-([\w\d.]*)-([\w\d.]*)"
    
    def __init__(self, uplid):
        """
        Create a UplidDescription from the specified 'uplid' string.  A uplid
        string is documented:
        http://bloomberg.github.io/bde-tools/bde_repo.html#bde-metadata
        """
        match = re.match(self.UPLID_REGEX, uplid)
        if (match is None):
            raise Exception("Unable to parse uplid: {}".format(uplid))
        
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