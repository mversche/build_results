
<head>
<link rel="stylesheet" type="text/css" href="results.css">
</head>

<div id="wrapper">
    <div id="header">
        <h1>Build Results from XYZ</h1>
    </div>
    <div id="nav">
        link1<p>
        link2<p>
    </div>  
    <div id="content">
         text<p>text<p>
         <table class="box-table-a">
            % for row in table:
                <tr>
                    % for cell in row:
                    <td class="error">${cell}</td>
                    % endfor
                </tr>        
            % endfor
        </table>     
                more text
    </div>
  
 
    <div id="footer">
        Generated now!
    </div>
</div>

