
#!/usr/bin/env python

from mako.template import Template
from resulttable import ResultTableDescription
import results_sqlite_query
import sqlite3

conn = sqlite3.connect('example_results.db')

data = results_sqlite_query.create_summary_table(conn)
tables = [ResultTableDescription("Build Summary",
                                 "Build Summary",
                                 data[0],
                                 data[1:])]
print(Template(filename="./results_page.mako").render(tables = tables))
conn.close()               