#!/usr/bin/env python

import sqlite3

CATEGORY_SORT_KEY = { 'BUILD_ERROR'      : 0, 
                      'TEST_RUN_FAILURE' : 1, 
                      'BUILD_WARNING'    : 2, 
                      'PROGRESS'         : 4, 
                      'TEST_WARNING'     : 3 }
                      
def query_tables(db_connection):
    """
    Return a list of tables available from the specified 'db_connection'
    """
    cursor = db_connection.cursor()
    cursor.execute("select name from sqlite_master where type = 'table';")
    results = cursor.fetchall()
    return list(map(lambda x: x[0], results))


def query_table(db_connection, table):
    cursor = db_connection.cursor()
    cursor.execute(table.sql_statement)
    return list(map(table.column_formatter, cursor.fetchall()))
    
    
    
def pivotSum(oldSum, value):
    return oldSum + value
    
def aggregate_value(result, keys, value, aggregator): 
    result_walker = result
    for key in keys[:-1]:
        if key not in result_walker:
            result_walker[key] = {}
        result_walker = result_walker[key]
        
    if keys[-1] not in result_walker:
        result_walker[keys[-1]] = value
    else:
        result_walker[keys[-1]] = aggregator(result_walker[keys[-1]], value)


def zero_fill(result, keys):
    # base case, 1 set of keys
    if (1 == len(keys)):
        for key_value in keys[0]:
            if key_value not in result:
                result[key_value] = 0
        return
    
    for key_value in keys[0]:
        if key_value not in result:
            result[key_value] = {}
        zero_fill(result[key_value], keys[1:])
    
def create_sort_function(item_sorts, column_items):
    sort_functions = []
    for item in column_items:
        if item in item_sorts:
            sort_functions.append(item_sorts[item])
        else:
            sort_functions.append(lambda x: x)
           
    def functor(value_tuple): 
        result = []
        for idx, value in enumerate(value_tuple):
            result.append(sort_functions[idx](value))
        return tuple(result)
    
    return functor
    
def pivot(data, data_columns, row_items, column_items, value_items, item_sorts, aggregator = pivotSum):
    """
    Create a pivot table for the specified 'data', having the specified 'data_columns', where the rows of the 
    pivot table are defined by the items in 'row_items', the columns in the pivot table are defined by 'column_items',
    and the data values in the pivot table are defined by 'value_items', and finally where the values are aggregated with
    the specified 'aggregator' function.
    """
    result = {}
    row_indexes    = []
    column_indexes = []
    value_indexes  = []
    
    # Create sets of the column and value keys used to index 'result'.  Note that
    # the keys must be tuple, so the elements of 'value_items' must be made into
    # tuples.
    column_keys = set()
    value_keys  = set(map(lambda x: tuple([x]), value_items))
    
    # Use the higher-order function 'create_sort_function' to generate functions
    # for sorting tuples based on the items_sorts and the items in the tuple.
    column_sorter = create_sort_function(item_sorts, column_items)
    row_sorter = create_sort_function(item_sorts, row_items)
    value_sorter = create_sort_function(item_sorts, value_items)
            
    # Populate [row|column|value]_indexes with the index into 'data_columns' where the
    # [row|column|value]_items element at the corresponding index can be found.
    for row_item in row_items:
        for (idx, column) in enumerate(data_columns):
            if (row_item == column):
                row_indexes.append(idx)
    
    for column_item in column_items:
        for (idx, column) in enumerate(data_columns):
            if (column_item == column):
                column_indexes.append(idx)
            
    for value in value_items:
        for (idx, column) in enumerate(data_columns):
            if (value == column):
                value_indexes.append(idx)
    
    # Create the pivot table.
    for row in data:       
        row_key = tuple(map(lambda x: row[x], row_indexes))
        column_key = tuple(map(lambda x: row[x], column_indexes))                        
        column_keys.add(column_key)
        for idx, value in enumerate(value_items):
            aggregate_value(result, [row_key, column_key, tuple([value])], row[value_indexes[idx]], aggregator)
        
    # Fill in 0 cells for row_key/column_key/value_key combinations not found in the data.
    zero_fill(result, [result.keys(), list(column_keys), list(value_keys)])
          
    # flatten back into a table
    headers = row_items
    for column in sorted(column_keys, key=column_sorter):
        headers.append(column[0])
    table = [headers]
    for row in sorted(result.keys(), key=row_sorter):
        row_value = list(row)
        for column in sorted(column_keys, key=column_sorter):
            row_value.append(result[row][column][tuple([value_items[0]])])
        table.append(row_value)    
    return table    


SORT_KEY2 = {'unix-AIX-powerpc-7.1-xlc-11.2': 3, 'unix-Linux-x86_64-2.6.18-gcc-4.9.2' : 2, 'unix-SunOS-sparc-5.10-cc-5.12' : 0, 'unix-darwin-x86_64-13.2.0-clang-5.1.0' : 4, 'windows-Windows_NT-amd64-6.1-cl-18.00' : 1 }
    
def create_summary_table(db_connection):
    cursor = db_connection.cursor()
    cursor.execute( "SELECT uplid, ufid, category_name, cast(count as INTEGER) "\
                    " FROM aggregated_results_at_uor_name_level"\
                    " GROUP BY category_name, ufid, uplid"\
                    " ORDER BY uplid, ufid;")
                    
    raw_table = cursor.fetchall()    
    
    result = pivot(raw_table, 
                   ['uplid', 'ufid', 'category_name', 'count'], 
                   ['uplid', 'ufid'],
                   ['category_name'],
                   ['count'],
                   {'category_name': lambda x: CATEGORY_SORT_KEY[x]}                    
                   )
    return result


conn = sqlite3.connect('example_results.db')

data = create_summary_table(conn)
for row in data:
    print(row)
conn.close()               