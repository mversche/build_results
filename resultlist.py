#!/usr/bin/env python

from mako.template import Template
from result_table import ResultTable
import results_sqlite_query
import sqlite3

def create_detail_link_function(headers, category):
    def create_detail_link(row, col_index):
        return "detail.py uplid='{}' ufid='{}' category='{}' uor='{}'".format(
            row[0], row[1], category, headers[col_index])
    return create_detail_link
    
def create_summary_link_function(headers):
    def create_detail_link(row, col_index):
        return "detail.py uplid='{}' ufid='{}' category='{}'".format(
            row[0], row[1], headers[col_index])
            
    return create_detail_link

def main():
    conn = sqlite3.connect('example_results.db')
    result = results_sqlite_query.create_failure_list(conn, "TEST_RUN_FAILURE", 20)
    print(Template(filename="./resultlist_page.mako").render(result = result))
    conn.close()          

if __name__ == "__main__":
    main()
     