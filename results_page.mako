<head>
<link rel="stylesheet" type="text/css" href="results.css">
</head>

<h1> Build Results for Today</h1>

<table class="box-table-a">
    % for row in table:
	<tr>
		% for cell in row:
		<td class="error">${cell}</td>
		% endfor
	</tr>        
    % endfor
</table>
