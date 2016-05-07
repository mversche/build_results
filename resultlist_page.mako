<head>
<link rel="stylesheet" type="text/css" href="results.css">
</head>
<a name="top"></a>
<div id="wrapper">
    <div id="header">
        <h1>Build Results from XYZ</h1>
    </div>
    <div id="nav">
        nav
    </div>  
    <div id="tableresults">
        <table  class="box-table-a">
        % for idx, row in enumerate(result[0]):
            <tr>
                % for idx, cell in enumerate(row):
                    <th>${cell}</th>
                % endfor
            </tr>
        % endfor
        % for idx, row in enumerate(result[1]):
            <tr>
                % for idx, cell in enumerate(row):
                    <td>${cell}</td>
                % endfor
            </tr>
        % endfor
        </table>

        <a href="#top">top</a>                    
    </div>
</div>