#!/usr/bin/env python

import uplid

class TableDescription:
    def __init__(self, title, link_text, column_headers, data, detail_link_function = None):    
        self.title = title
        self.link_text = link_text
        self.column_headers = column_headers
        self.data = data
        if detail_link_function is not None:
            self.detail_link_function = detail_link_function

            
    
    def __str__(self):
        result = "{} ({})\n{}\n".format(self.title,
                                        self.link_text,
                                        str(self.column_headers[0]))
        for row in self.data:
            result = result + str(row) + "\n"
        return result