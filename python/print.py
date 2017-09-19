import json
from process import process

MAX_COLUMNS = 10

PAGE_TEMPLATE = '''<!doctype html>
<html>
    <head>
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Training Plan</title>
        <style>
            table {{
                border-collapse: collapse;
            }}
            th, td {{
                border: 1px solid black;
                font-size: 14px;
                text-align: left;
            }}
            .week {{
                height: 1.6em;
                font-weight: bold;
            }}
            .day {{
                height: 1.4em;
                font-weight: bolder;
            }}
            .set {{
                width: 2cm;
            }}
        </style>
    </head>
    <body>
        <div>
            <table>
                {0}
            </table>
        <div>
    </body>
</html>'''

def render(content):
    data = json.loads(content)
    rows = [
        '<tr><td class="week" colspan="11">{0}</td></tr>'.format(data['week']),
        '<tr>{0}<tr>'.format(format_weights(data['weights']))
    ];
    colspan = MAX_COLUMNS + 1
    for day in data['days']:
        rows.append('<tr><td colspan="{0}">&nbsp;</td></tr>'.format(colspan))
        rows.append('<tr><td class="day" colspan="{0}">{1}</td></tr>'.format(colspan, day['name']))
        for exercise in day['exercises']:
            sets = exercise['sets']
            format_cell = format_ratio_cell if 'ratio' in sets[0] else format_simple_cell
            rows.append(format_row(exercise['name'], sets, format_cell))
            if len(sets) > MAX_COLUMNS:
                rows.append(format_row('', sets[MAX_COLUMNS:], format_cell))
    return PAGE_TEMPLATE.format('\n'.join(rows))

def format_weights(weights):
    items = ['<td></td>']
    for item in weights:
        items.append('<td class="set">{name}</td><td class="set">{weight}</td>'.format(**item))
    return ''.join(items)

def format_ratio_cell(cell):
    return '<td class="set">{0}% {1} / {2}</td>'\
        .format(round(cell['ratio'] * 100), cell['count'], cell['weight'])

def format_simple_cell(cell):
    return '<td class="set">{0}</td>'.format(cell['count'])

def format_row(name, sets, format_cell):
    cells = ['<td class="exercise">{0}</td>'.format(name)]
    cells.extend(map(format_cell, sets[:MAX_COLUMNS]))
    for _ in range(len(sets), MAX_COLUMNS):
        cells.append('<td></td>')
    return '<tr>{0}</tr>'.format(''.join(cells))

process(render)
