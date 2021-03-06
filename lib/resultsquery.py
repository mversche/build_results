#!/usr/bin/env python

import sqlite3

from pivottable import PivotTable
from tabledescription import TableDescription
from uplid import UplidDescription

CATEGORY_SORT_KEY = { 'BUILD_ERROR'      : 0, 
                      'TEST_RUN_FAILURE' : 1, 
                      'BUILD_WARNING'    : 2, 
                      'PROGRESS'         : 4, 
                      'TEST_WARNING'     : 3 }       

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

    #raw_table = map(lambda x: [uplid_transform(x[0]), x[1], category_transform(x[2]), x[3]], raw_table)
    
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
    #raw_table = map(lambda x: [uplid_transform(x[0]), x[1], x[2], x[3]], raw_table)
    
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
    
def create_failure_list(db_connection, category, limit, uplid = None, ufid = None):
    cursor = db_connection.cursor()
    
    statement = """
        SELECT component_name, uplid, ufid, 1
        FROM build_results
        WHERE {where}
        GROUP BY component_name, uplid, ufid
        """
    
    where_clause = ["category_name == :category"]
    bind_parameters = {'category' : category}
    if (uplid is not None):
        where_clause.append("uplid == :uplid")
        bind_parameters['uplid'] = uplid
    if (ufid is not None):
        where_clause.append("ufid == :ufid")
        bind_parameters['ufid'] = ufid
    
    print(statement.format(where = " AND ".join(where_clause), limit = limit))
    cursor.execute(statement.format(where = " AND ".join(where_clause), limit = limit),
                   bind_parameters)
    raw_table = cursor.fetchall()                
    result = PivotTable(raw_table, 
                       ['component', 'uplid', 'ufid', 'count'], 
                       ['component'],
                       ['uplid', 'ufid'],
                       ['count'],
                       {}
                       )
                   
    
    return result.flatten_table()
    
    
def create_commit_information_table(db_connection):
    cursor = db_connection.cursor()    
    cursor.execute("""SELECT repository, branch, SHA
                      FROM repositories
                      ORDER BY priority""")
    raw_table = cursor.fetchall()        
    
    return TableDescription("Repository Info", "Repositories",
                            ["repository", "bbranch", "sha"],
                            raw_table)
                       
def create_build_attributes_information_table(db_connection):
    cursor = db_connection.cursor()    
    cursor.execute("""SELECT name, contents
                      FROM status_entries
                      ORDER BY name""")
    raw_table = cursor.fetchall()        
    
    return TableDescription("Build Attributes", "Build Attributes",
                            ["Attribute", "Value"],
                            raw_table)

def main():
    conn = sqlite3.connect('example_results.db')
    table = create_summary_table(conn)   
    print(table[0])
    for row in table[1]:
        print(row)
    
if __name__ == "__main__":
    main()
