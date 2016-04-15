#!/usr/bin/env python

import sqlite3
import resulttable

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
    
    
#SUMMARY_TABLE = ResultTableDescription(
#    "Build Summary",               # Title
#    "Build Summary",               # Link Text
#    ["uplid", "ufid", "category", "count"], # Column headers
#    "SELECT uplid, ufid, category_name, cast(count as INTEGER) "\
#    " FROM aggregated_results_at_uor_name_level"\
#    " GROUP BY category_name, ufid, uplid"\
#    " ORDER BY uplid, ufid;",   # SQL
#    lambda x: [display_uplid(x[0]), x[1], x[2], x[3]]
    
def pivotSum(oldSum, value):
    if (oldSum is None):
        return value
    return oldSum + value
    
def pivot(data, data_columns, row_items, column_items, values, aggregator = pivotSum):
    result = {}
    row_indexes    = []
    column_indexes = []
    value_indexes  = []
    
    for row_item in row_items:
        for (idx, column) in enumerate(data_columns):
            if (row_item == column):
                row_indexes.append(idx)
    
    for column_item in column_items:
        for (idx, column) in enumerate(data_columns):
            if (column_item == column):
                column_indexes.append(idx)
            
    for value in values:
        for (idx, column) in enumerate(data_columns):
            if (value == column):
                value_indexes.append(idx)
    
    for row in data:
        row_key = list(map(lambda x: row[x], row_indexes))
        column_key = list(map(lambda x: row[x], column_indexes))
        result[row_key, column_key] = aggregator(result[row_key, column_key], row[value_indexes[0]])

    print(result)
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
                   ['count'])
                        
                           
    
conn = sqlite3.connect('example_results.db')
result = create_summary_table(conn)
conn.close()               