#!/usr/bin/env python

import uplid

class ResultTable:
    def __init__(self, title, link_text, column_headers, data):    
        self.title = title
        self.link_text = link_text
        self.column_headers = column_headers
        self.data = data
            
    
    def __str__(self):
        result = "{} ({})\n{}\n".format(self.title,
                                        self.link_text,
                                        str(self.column_headers[0]))
        for row in self.data:
            result = result + str(row) + "\n"
        return result