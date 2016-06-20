#!/usr/bin/env python

from mako.template import Template
from lib.tabledescription import TableDescription
from lib import resultsquery
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
    result = resultsquery.create_summary_table(conn)
    results = [TableDescription("Build Summary", "Build Summary", result[0][0], result[1], create_summary_link_function(result[0][0]))]

    DETAILS = ['BUILD_ERROR', 'TEST_RUN_FAILURE', 'BUILD_WARNING']
    for type in DETAILS:
        result = resultsquery.create_package_group_detail_table(conn, type)
        results.append(TableDescription(resultsquery.category_transform(type),
                                   resultsquery.category_transform(type),
                                   result[0][0], 
                                   result[1],
                                   create_detail_link_function(result[0][0], type)))
    
    commit_info = resultsquery.create_commit_information_table(conn)
    attribute_info = resultsquery.create_build_attributes_information_table(conn)
    results.append(commit_info)
    results.append(attribute_info)
    
    print(Template(filename="./summarypage.mako").render(tables = results,
                                                         commit_info = commit_info))
    conn.close()          

if __name__ == "__main__":
    main()
     
