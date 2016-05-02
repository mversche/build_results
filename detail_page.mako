<head>
<link rel="stylesheet" type="text/css" href="detail.css">
</head>
<a name="top"></a>
<ul>
    % for idx, row in enumerate(details):
       <% 
          component_padded = row['component'].ljust(50)
          uplid_padded = row['uplid'].ljust(40)
          ufid_padded = row['ufid'].ljust(20)
       %>
       <li><a href="#table${idx}"><pre> ${component_padded}[${uplid_padded}, ${ufid_padded}]</pre></a>
    % endfor
</ul>
% for idx, row in enumerate(details):
 
    <a name="table${idx}"></a>
    <table>        
        <tr>
            <td>${row['uplid']} </td><td> ${row['ufid']}</td><td>${row['component']}</td>
        </tr>
    </table></h1>
    <a href="#top">top</a> 
    <pre>
        ${row['diagnostic']}
    </pre>
% endfor
