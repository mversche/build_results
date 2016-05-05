<head>
<link rel="stylesheet" type="text/css" href="result.css">
</head>
<h1> Results </h1>
<table>
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
