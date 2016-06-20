#!/usr/bin/env python

from mako.template import Template
import argparse
import cgi
import cgitb
import os
import sqlite3

from lib.tabledescription import TableDescription
from lib import resultsquery

def generate_datail_html(database_name, category, uplid, ufid, uor):
    conn = sqlite3.connect(database_name)
    cursor = conn.cursor()

    parameters = {}
    restrictions = ["category_name == :category"]
    parameters['category'] = category
    if (uplid is not None):
        restrictions.append("uplid == :uplid")
        parameters['uplid'] = uplid
    if (ufid is not None):
        restrictions.append("ufid == :ufid")
        parameters['ufid'] = ufid
    if (uor is not None):
        restrictions.append("uor_name == :uor")
        parameters['uor'] = uor

    where_clause = " AND ".join(restrictions)
    sql_statement = """
            SELECT uplid, ufid, uor_name, component_name, diagnostics
            FROM build_results
            WHERE {}
            ORDER BY uplid, ufid, component_name""".format(where_clause)

    cursor.execute(sql_statement, parameters)
    raw_table = cursor.fetchall()
    conn.close()

    parsed_table = list(
        map(lambda x: {'uplid': x[0], 'ufid': x[1], 'uor': x[2], 'component': x[3], 'diagnostic': x[4]}, raw_table))
    print(Template(filename="./detailpage.mako").render(details=parsed_table))
    print(category)

def cgimain():
    form = cgi.FieldStorage()
    category = form["category"].value.strip()
    uplid = form["uplid"].value.strip() if "uplid" in form else None
    ufid = form["ufid"].value if "ufid" in form else None
    uor = form["uor"].value if "uor" in form else None

    print("Content-type: text/html")
    print()
    generate_datail_html("example_results.db", category, uplid, ufid, uor)

def main():

    parser = argparse.ArgumentParser()
    parser.add_argument("--database",
                        help = "Database name")
    parser.add_argument("--uplid",                         
                        help = "Restrict results by uplid")
    parser.add_argument("--ufid",                         
                        help = "Restrict results by ufid")
    parser.add_argument("--uor",                         
                        help = "Restrict results by uor")
    parser.add_argument("--category",                         
                        help = "Restrict results by category",
                        required = True)  
    parser.add_argument("--limit",
                        type = int,
                        default = 20,
                        help = "Limit the number of results (default: 20).")
    args = parser.parse_args()
    generate_datail_html("example_results.db", args.category, args.uplid, args.ufid, args.uor)

if __name__ == "__main__":
    if 'GATEWAY_INTERFACE' in os.environ:
        cgitb.enable()
        cgimain()
    else:
        main()
