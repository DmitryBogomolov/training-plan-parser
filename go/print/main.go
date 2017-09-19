package main

import (
	"encoding/json"
	"fmt"
	"math"
	"strings"

	"../common"
)

const maxColumns = 10

type formatCellHandler func(interface{}) string

const pageTemplate = `<!doctype html>
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
                %s
            </table>
        <div>
    </body>
</html>`

func render(content string) (string, error) {
	var info common.Info
	err := json.Unmarshal([]byte(content), &info)
	if err != nil {
		return "", err
	}

	rows := make([]string, 0, 2+len(info.Days)*(2+2*maxColumns))
	rows = append(rows, fmt.Sprintf(`<tr><td class="week" colspan="11">%s</td></tr>`, info.Week))
	rows = append(rows, fmt.Sprintf(`<tr>%s</tr>`, formatWeights(info.Weights)))

	const colspan = maxColumns + 1
	for _, day := range info.Days {
		rows = append(rows, fmt.Sprintf(`<tr><td colspan="%d">&nbsp;</td></tr>`, colspan))
		rows = append(rows, fmt.Sprintf(`<tr><td class="day" colspan="%d">%s</td></tr>`, colspan, day.Name))
		for _, ex := range day.Exercises {
			sets := ex.Sets
			var formatCell formatCellHandler
			if _, ok := sets[0].(map[string]interface{})["ratio"]; ok {
				formatCell = formatRatioCell
			} else {
				formatCell = formatSimpleCell
			}
			rows = append(rows, formatRow(ex.Name, sets, formatCell))
			if len(sets) > maxColumns {
				rows = append(rows, formatRow("", sets[maxColumns:], formatCell))
			}
		}
	}

	return fmt.Sprintf(pageTemplate, strings.Join(rows, "\n")), nil
}

func formatWeights(weights []common.Weight) string {
	items := make([]string, 0, 1+len(weights))
	items = append(items, `<td></td>`)
	for _, w := range weights {
		items = append(items, fmt.Sprintf(`<td class="set">%s</td><td class="set">%d</td>`, w.Name, w.Weight))
	}
	return strings.Join(items, "")
}

type formatter interface {
	format() string
}

func formatRatioCell(item interface{}) string {
	cell := common.ParseRatioSet(item)
	return fmt.Sprintf(`<td class="set">%.0f%% %d / %d</td>`, cell.Ratio*100, cell.Count, cell.Weight)
}

func formatSimpleCell(item interface{}) string {
	cell := common.ParseSimpleSet(item)
	return fmt.Sprintf(`<td class="set">%d</td>`, cell.Count)
}

func formatRow(name string, sets []interface{}, formatCell formatCellHandler) string {
	cells := make([]string, 0, 1+2*maxColumns)
	cells = append(cells, fmt.Sprintf(`<td class="exercise">%s</td>`, name))
	for _, set := range sets[:int(math.Min(float64(len(sets)), maxColumns))] {
		cells = append(cells, formatCell(set))
	}
	for i := len(sets); i < maxColumns; i++ {
		cells = append(cells, `<td></td>`)
	}
	return fmt.Sprintf(`<tr>%s</tr>`, strings.Join(cells, ""))
}

func main() {
	common.Process(render)
}
