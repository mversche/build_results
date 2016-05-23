#!/usr/bin/env python

from pylibinit import addlibpath
addlibpath.add_lib_path()     # add custom library path

import os
import sys

from mako.template import Template
from result_table import ResultTable
import results_sqlite_query
import sqlite3
import argparse

def main():

    parser = argparse.ArgumentParser()
    parser.add_argument("database")
    parser.add_argument("--uplid",                         
                        help = "Restrict results by uplid")
    parser.add_argument("--ufid",                         
                        help = "Restrict results by ufid")
    parser.add_argument("--uor",                         
                        help = "Restrict results by ufid")                       
    parser.add_argument("--category",                         
                        help = "Restrict results by ufid",
                        required = True)  
    parser.add_argument("--limit",
                        type = int,
                        default = 20,
                        help = "Limit the number of results (default: 20).")
    args = parser.parse_args()
        
    conn = sqlite3.connect(args.database)
    cursor = conn.cursor()
    
    parameters = {}
    restrictions = ["category_name == :category"]
    parameters['category'] = args.category
    if (args.uplid is not None):
        restrictions.append("uplid == :uplid")
        parameters['uplid'] = args.uplid
    if (args.ufid is not None):
        restrictions.append("ufid == :ufid")
        parameters['ufid'] = args.ufid
    if (args.uor is not None):
        restrictions.append("uor_name == :uor")
        parameters['uor'] = args.uor
        
    where_clause = " AND ".join(restrictions)
    sql_statement = """
        SELECT uplid, ufid, uor_name, component_name, diagnostics
        FROM build_results 
        WHERE {}
        ORDER BY uplid, ufid, component_name""".format(where_clause)
                    
    cursor.execute(sql_statement, parameters)    
    raw_table = cursor.fetchall()    
    conn.close()               

    parsed_table = list(map(lambda x: {'uplid': x[0], 'ufid': x[1], 'uor': x[2], 'component': x[3], 'diagnostic': x[4]}, raw_table))
    print(Template(filename="./detail_page.mako").render(details = parsed_table))
    
if __name__ == "__main__":
    main()
