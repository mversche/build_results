
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
            <li class="nav_links"><a href="#table${tableidx}">${table[0].link_text}</a></li>
        % endfor
        </ul>
    </div>  
    <div id="content">
        % for (tableidx, table) in enumerate(tables):
            <a name="table${tableidx}"></a>
            <h2>
                ${tableidx + 1}. ${table[0].title}
            </h2>
            <table class="box-table-a">
                <tr>
                    % for cell in table[0].column_headers:
                    <th>${cell}</th>
                    % endfor

                </tr>
                % for row in table[1]:
                    <tr>
                        % for cell in row:
                        <td>${cell}</td>
                        % endfor
                    </tr>        
                % endfor
            </table>   
            <a href="#top">top</a>            
        % endfor
    </div>
  
 
    <div id="footer">
        Generated now!
    </div>
</div>

