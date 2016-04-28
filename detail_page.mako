<head>
<link rel="stylesheet" type="text/css" href="detail.css">
</head>
% for row in details:
    <table>
        <tr>
            <th>UPLID</th><th>UFID</th><th>UOR</th>
        </tr>
        <tr>
            <td>${row['uplid']} </td><td> ${row['ufid']}</td><td>${row['uor']}</td>
        </tr>
    </table></h1>
    ${row['diagnostic']}
%endfor
