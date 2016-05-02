#!/usr/bin/env python

import sqlite3

from pivot_table import PivotTable
from result_table import ResultTable
from uplid import UplidDescription

CATEGORY_SORT_KEY = { 'Build Error'      : 0, 
                      'Test Run Failure' : 1, 
                      'Build Warning'    : 2, 
                      'Progress'         : 4, 
                      'Test Warning'     : 3 }       

UOR_SORT_KEY = { 'bsl'  : 0,
                 'bdl'  : 1,                      
                 'bal'  : 2,
                 'btl'  : 3,
                 'bbl'  : 4,
                 'bde'  : 5,
                 'bce'  : 6,
                 'bae'  : 7,
                 'bte'  : 8,
                 'bsi'  : 9,
                 'bbe'  : 10,
                 'unknown' : 11}  
                 
CATEGORY_NAME_MAP = {
                    'BUILD_ERROR'      : 'Build Error', 
                    'TEST_RUN_FAILURE' : 'Test Run Failure', 
                    'BUILD_WARNING'    : 'Build Warning', 
                    'PROGRESS'         : 'Progress', 
                    'TEST_WARNING'     : 'Test Warning' }       
                 
                 
def uplid_transform(uplid_string):
    uplid = UplidDescription(uplid_string)
    return uplid.os_name + " (" + uplid.compiler_type + "-" + uplid.compiler_version + ")"
    
def category_transform(category_string):
    return CATEGORY_NAME_MAP[category_string]
                      
def list_tables(db_connection):
    """
    Return a list of tables available from the specified 'db_connection'
    """
    cursor = db_connection.cursor()
    cursor.execute("select name from sqlite_master where type = 'table';")
    results = cursor.fetchall()
    return list(map(lambda x: x[0], results))       
    
def create_summary_table(db_connection):
    cursor = db_connection.cursor()
    cursor.execute("SELECT uplid, ufid, category_name, SUM(cast(count as INTEGER)) "\
                   " FROM aggregated_results_at_uor_name_level"\
                   " WHERE category_name != 'TEST_WARNING'"\
                   " GROUP BY category_name, ufid, uplid;")
                    
    raw_table = cursor.fetchall()   

    raw_table = map(lambda x: [uplid_transform(x[0]), x[1], category_transform(x[2]), x[3]], raw_table)
    
    result = PivotTable(raw_table, 
                       ['uplid', 'ufid', 'category_name', 'count'], 
                       ['uplid', 'ufid'],
                       ['category_name'],
                       ['count'],
                       {'category_name': lambda x: CATEGORY_SORT_KEY[x]}                    
                       ).flatten_table()
    return result
    
def create_package_group_detail_table(db_connection, category):
    cursor = db_connection.cursor()
    
    cursor.execute("SELECT uplid, ufid, uor_name, SUM(cast(count as INTEGER)) "\
                   " FROM aggregated_results_at_uor_name_level"\
                   " WHERE category_name == ?"\
                   " GROUP BY ufid, uplid, uor_name;",
                   tuple([category]))
    
                    
    raw_table = cursor.fetchall()        
    raw_table = map(lambda x: [uplid_transform(x[0]), x[1], x[2], x[3]], raw_table)
    
    result = PivotTable(raw_table, 
                       ['uplid', 'ufid', 'uor_name', 'count'], 
                       ['uplid', 'ufid'],
                       ['uor_name'],
                       ['count'], 
                       {'uor_name' : lambda x: UOR_SORT_KEY[x]}
                       )
                       
    cursor.execute("SELECT uor_name FROM aggregated_results_at_uor_name_level GROUP BY uor_name")
    uors = cursor.fetchall()
    result.insert_column_keys(uors)
    return result.flatten_table()
    
def create_commit_information_table(db_connection):
    cursor = db_connection.cursor()    
    cursor.execute("""SELECT repository, branch, SHA
                      FROM repositories
                      ORDER BY priority""")
    raw_table = cursor.fetchall()        
    
    return ResultTable("Repository Info", "Repositories",
                       ["repository", "bbranch", "sha"],
                       raw_table)
                       
    
def main():
    conn = sqlite3.connect('example_results.db')
    table = create_summary_table(conn)   
    print(table[0])
    for row in table[1]:
        print(row)
    
if __name__ == "__main__":
    main()
