package main

import (
	"encoding/json"
	"math"
	"regexp"
	"strconv"
	"strings"

	"../common"
)

var dayPattern = regexp.MustCompile("\\d+ день")
var ratioExercisePattern = regexp.MustCompile("(\\d+)% (\\d+)х(\\d+)")
var simpleExercisePattern = regexp.MustCompile("(\\d+)х(\\d+)")

type pattern struct {
	pattern *regexp.Regexp
	weight  int
}

func splitToLines(data string) []string {
	lines := strings.Split(data, "\n")
	var ret []string
	for _, line := range lines {
		trimmed := strings.TrimSpace(line)
		if trimmed != "" {
			ret = append(ret, trimmed)
		}
	}
	return ret
}

func findDayPositions(lines []string) []int {
	var positions []int
	for i, line := range lines {
		if dayPattern.FindString(line) != "" {
			positions = append(positions, i)
		}
	}
	return append(positions, len(lines))
}

func findWeightsAndPatterns(lines []string) ([]common.Weight, []pattern) {
	weights := make([]common.Weight, len(lines))
	patterns := make([]pattern, len(lines))
	for i, line := range lines {
		parts := strings.Split(line, " ")
		name := strings.TrimSpace(parts[0])
		value, _ := strconv.Atoi(strings.TrimSpace(parts[1]))
		reg := regexp.MustCompile("(?i)" + strings.ToLower(name))
		weights[i] = common.Weight{Name: name, Weight: value}
		patterns[i] = pattern{pattern: reg, weight: value}
	}
	return weights, patterns
}

func extractExercise(line string, patterns []pattern) *common.Exercise {
	var ex *common.Exercise
	ex = extractExerciseByRatioPattern(line, patterns)
	if ex == nil {
		ex = extractExerciseBySimplePattern(line)
	}
	return ex
}

func extractExerciseByRatioPattern(line string, patterns []pattern) *common.Exercise {
	name := checkPattern(line, ratioExercisePattern)
	if name == "" {
		return nil
	}
	weight := selectWeightByName(name, patterns)
	matches := ratioExercisePattern.FindAllStringSubmatch(line, -1)
	sets := make([]interface{}, 0, len(matches)*4)
	for _, match := range matches {
		ratio, _ := strconv.Atoi(match[1])
		k := float64(ratio) / 100
		w := calculateWeight(k, weight)
		reps, _ := strconv.Atoi(match[2])
		count, _ := strconv.Atoi(match[3])
		set := common.RatioSet{Ratio: k, Count: reps, Weight: w}
		for i := 0; i < count; i++ {
			sets = append(sets, set)
		}
	}
	return &common.Exercise{Name: name, Sets: sets}
}

func selectWeightByName(name string, patterns []pattern) int {
	for _, obj := range patterns {
		if obj.pattern.FindString(name) != "" {
			return obj.weight
		}
	}
	return 0
}

func calculateWeight(ratio float64, weight int) int {
	w := ratio * float64(weight)
	return int(math.Floor(w/5+0.5)) * 5
}

func extractExerciseBySimplePattern(line string) *common.Exercise {
	name := checkPattern(line, simpleExercisePattern)
	if name == "" {
		return nil
	}
	match := simpleExercisePattern.FindStringSubmatch(line)
	reps, _ := strconv.Atoi(match[1])
	count, _ := strconv.Atoi(match[2])
	set := common.SimpleSet{Count: reps}
	sets := make([]interface{}, 0, count)
	for i := 0; i < count; i++ {
		sets = append(sets, set)
	}
	return &common.Exercise{Name: name, Sets: sets}
}

func checkPattern(line string, reg *regexp.Regexp) string {
	loc := reg.FindStringIndex(line)
	if len(loc) == 0 {
		return ""
	}
	return strings.TrimSpace(line[:loc[0]])
}

func parse(data string) (string, error) {
	lines := splitToLines(data)

	week := strings.TrimSpace(lines[0])
	positions := findDayPositions(lines)
	weights, patterns := findWeightsAndPatterns(lines[1:positions[0]])

	days := make([]*common.Day, 0, len(positions)-1)
	for i, pos := range positions[:len(positions)-1] {
		items := lines[pos+1 : positions[i+1]]
		exercises := make([]*common.Exercise, 0, len(items))
		for _, item := range items {
			ex := extractExercise(item, patterns)
			exercises = append(exercises, ex)
		}
		d := &common.Day{Name: lines[pos], Exercises: exercises}
		days = append(days, d)
	}

	info := common.Info{Week: week, Weights: weights, Days: days}

	str, err := json.MarshalIndent(info, "", "  ")
	return string(str) + "\n", err
}

func main() {
	common.Process(parse)
}
