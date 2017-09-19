const readStdin = require('./stdin');

const MAX_COLUMNS = 10;

function formatPage(table) {
    return `<!doctype html>
<html>
    <head>
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Training Plan</title>
        <style>
            table {
                border-collapse: collapse;
            }
            th, td {
                border: 1px solid black;
                font-size: 14px;
                text-align: left;
            }
            .week {
                height: 1.6em;
                font-weight: bold;
            }
            .day {
                height: 1.4em;
                font-weight: bolder;
            }
            .set {
                width: 2cm;
            }
        </style>
    </head>
    <body>
        <div>
            <table>
${table}
            </table>
        <div>
    </body>
</html>`;
}

function formatRatioCell(cell) {
    return `<td class="set">${(cell.ratio * 100).toFixed(0)}% ${cell.count} / ${cell.weight}</td>`;
}

function formatSimpleCell(cell) {
    return `<td class="set">${cell.count}</td>`;
}

function formatRow(name, sets, formatCell) {
    const cells = sets.slice(0, MAX_COLUMNS).map(formatCell);
    for (let i = sets.length; i < MAX_COLUMNS; ++i) {
        cells.push('<td></td>');
    }
    const content = [`<td class="exercise">${name}</td>`].concat(cells).join('');
    return `<tr>${content}</tr>`;
}

function formatWeights(weights) {
    return [
        '<td></td>',
        ...weights.map(({ name, weight }) =>
            `<td class="set">${name}</td><td class="set">${weight}</td>`)
    ].join('');
    return columns.join('');
}

function print(content) {
    const { week, weights, days } = JSON.parse(content);
    const rows = [
        `<tr><td class="week" colspan="11">${week}</td></tr>`,
        `<tr>${formatWeights(weights)}<tr>`
    ];
    days.forEach((day) => {
        rows.push(`<tr><td colspan="${MAX_COLUMNS + 1}">&nbsp;</td></tr>`);
        rows.push(`<tr><td class="day" colspan="${MAX_COLUMNS + 1}">${day.name}</td></tr>`);
        day.exercises.forEach(({ name, sets }) => {
            const formatCell = sets[0].ratio ? formatRatioCell : formatSimpleCell;
            rows.push(formatRow(name, sets, formatCell));
            if (sets.length > MAX_COLUMNS) {
                rows.push(formatRow('', sets.slice(MAX_COLUMNS), formatCell));
            }
        });
    });
    return formatPage(rows.join('\n'));
}

readStdin().then((data) => {
    process.stdout.write(print(data));
});
