from jinja2 import Template


TPL = '''
<html>
    <head>
        <meta charset="UTF-8">
    </head>
    <body>
            <p style='font-size:15px; font-family:Arial;'>{{ content }}</p>
            <table border="1" cellspacing="0" cellpadding="0">
            <tr>
                {% if array_table_head %}
                {% for var_i in array_table_head %}
                    <th style="font-size: 15px; padding: 3px;">{{var_i}}</th>
                {% endfor %}
                {% endif %}
            </tr>
            {% if dict_table_data %}
            {% for table_data in dict_table_data %}
            <tr>
                <th style="font-size: 12px; padding: 3px;">{{ table_data.Name }}</th>
                <th style="font-size: 12px; padding: 3px;">{{ table_data.Type }}</th>
                <th style="font-size: 12px; padding: 3px;">{{ table_data.Value }}</th>
            </tr>
            {% endfor %}
            {% endif %}
            </table>
    </body>
</html>
'''

render_dict = {}
dict_table_data = [{'Name': 'Basketball', 'Type': 'Sports', 'Value': 5},
                   {'Name': 'Football', 'Type': 'Sports', 'Value': 4.5},
                   {'Name': 'Pencil', 'Type': 'Learning', 'Value': 5},
                   {'Name': 'Hat', 'Type': 'Wearing', 'Value': 2}]
render_dict.update({'Content': 'Hello reader, here is a table:',
                    'array_table_head': ['Name', 'Type', 'Value'],
                    'dict_table_data': dict_table_data})


content = Template(TPL).render(render_dict)
with open('out.html', "w") as f:
        f.write(content)  # 写入文件

