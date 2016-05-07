<head>
<link rel="stylesheet" type="text/css" href="results.css">
</head>
<a name="top"></a>
<div id="wrapper">
    <div id="header">
        <h1>Build Results from XYZ</h1>
    </div>
    <div id="nav">
        <ul class="nav_links">
        % for (tableidx, table) in enumerate(tables):
            <li class="nav_links"><a href="#table${tableidx}">${table.link_text}</a></li>
        % endfor
        </ul>
    </div>  
    <div id="tableresults">
        % for (tableidx, table) in enumerate(tables):
            <a name="table${tableidx}"></a>
            <h2>
                ${table.title}
            </h2>
            <table class="box-table-a">
                <tr>
                    % for cell in table.column_headers:
                    <th nowrap>${cell}</th>
                    % endfor

                </tr>
                % for row in table.data:
                    <tr>
                        % for idx, cell in enumerate(row):
                            %if type(cell) is int and table.detail_link_function is not None:
                                <% linktarget = table.detail_link_function(row, idx) %>
                                <td class="box-table-a-red" nowrap><a href="${linktarget}">${cell}</a></td>
                            %else:
                                <td nowrap>${cell}</td>
                            %endif
                        % endfor
                    </tr>        
                % endfor
            </table>   
            <a href="#top">top</a>            
        % endfor
    </div>
</div>

