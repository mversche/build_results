
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
    result = results_sqlite_query.create_summary_table(conn)
    results = [ResultTable("Build Summary", "Build Summary", result[0][0], result[1], create_summary_link_function(result[0][0]))]

    DETAILS = ['BUILD_ERROR', 'TEST_RUN_FAILURE', 'BUILD_WARNING']
    for type in DETAILS:
        result = results_sqlite_query.create_package_group_detail_table(conn, type)
        results.append(ResultTable(results_sqlite_query.category_transform(type),
                                   results_sqlite_query.category_transform(type),
                                   result[0][0], 
                                   result[1],
                                   create_detail_link_function(result[0][0], type)))
    
    commit_info = results_sqlite_query.create_commit_information_table(conn)
    attribute_info = results_sqlite_query.create_build_attributes_information_table(conn)
    results.append(commit_info)
    results.append(attribute_info)
    
    print(Template(filename="./results_page.mako").render(tables = results,
                                                        commit_info = commit_info))
    conn.close()          

if __name__ == "__main__":
    main()
     