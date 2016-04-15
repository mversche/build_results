
#!/usr/bin/env python

import pandas

from mako.template import Template
import resulttable
import results_sqlite_query
import sqlite3

conn = sqlite3.connect('example_results.db')

tables = [(resulttable.SUMMARY_TABLE, results_sqlite_query.query_table(conn, resulttable.SUMMARY_TABLE))]
print(Template(filename="./results_page.mako").render(tables = tables))
conn.close()               