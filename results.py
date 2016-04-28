
#!/usr/bin/env python

from mako.template import Template
from result_table import ResultTable
import results_sqlite_query
import sqlite3

conn = sqlite3.connect('example_results.db')

result = results_sqlite_query.create_summary_table(conn)
results = [ResultTable("Build Summary", "Build Summary", result[0][0], result[1])]

DETAILS = ['BUILD_ERROR', 'TEST_RUN_FAILURE', 'BUILD_WARNING']
for type in DETAILS:
    result = results_sqlite_query.create_package_group_detail_table(conn, type)
    results.append(ResultTable(type, type, result[0][0], result[1]))
    
commit_info = results_sqlite_query.create_commit_information_table(conn)
results.append(commit_info)
    
print(Template(filename="./results_page.mako").render(tables = results,
                                                      commit_info = commit_info))
conn.close()               