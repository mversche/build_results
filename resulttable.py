#!/usr/bin/env python

import uplid

class ResultTableDescription:
    def __init__(self, title, link_text, column_headers, data):
        self.title = title
        self.link_text = link_text
        self.column_headers = column_headers
        self.sql_statement = sql_statement
        self.column_formatter = column_formatter
            
def display_uplid(uplid_string):
    up = uplid.UplidDescription(uplid_string)
    return up.os_name
    

