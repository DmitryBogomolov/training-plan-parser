package common

import (
	"errors"
	"io/ioutil"
	"os"
	"time"
)

type pair struct {
	data string
	err  error
}

func readStdin() (string, error) {
	c := make(chan pair)
	go func() {
		data, err := ioutil.ReadAll(os.Stdin)
		c <- pair{data: string(data), err: err}
	}()
	select {
	case ret := <-c:
		return ret.data, ret.err
	case <-time.After(time.Second):
		return "", errors.New("empty input")
	}
}

type Handler func(string) (string, error)

func Process(f Handler) {
	content, err := readStdin()
	// data, err := ioutil.ReadFile("../sample.json")
	// content := string(data)
	if err != nil {
		os.Stderr.WriteString(err.Error())
		return
	}
	result, err := f(content)
	if err != nil {
		os.Stderr.WriteString(err.Error())
		return
	}
	os.Stdout.WriteString(result)
}

type Weight struct {
	Name   string `json:"name,omitempty"`
	Weight int    `json:"weight,omitempty"`
}

type RatioSet struct {
	Ratio  float64 `json:"ratio,omitempty"`
	Weight int     `json:"weight,omitempty"`
	Count  int     `json:"count,omitempty"`
}

func ParseRatioSet(data interface{}) *RatioSet {
	obj := data.(map[string]interface{})
	return &RatioSet{
		Ratio:  obj["ratio"].(float64),
		Weight: int(obj["weight"].(float64)),
		Count:  int(obj["count"].(float64)),
	}
}

type SimpleSet struct {
	Count int `json:"count,omitempty"`
}

func ParseSimpleSet(data interface{}) *SimpleSet {
	obj := data.(map[string]interface{})
	return &SimpleSet{
		Count: int(obj["count"].(float64)),
	}
}

type Exercise struct {
	Name string        `json:"name,omitempty"`
	Sets []interface{} `json:"sets,omitempty"`
}

type Day struct {
	Name      string      `json:"name,omitempty"`
	Exercises []*Exercise `json:"exercises,omitempty"`
}

type Info struct {
	Week    string   `json:"week,omitempty"`
	Weights []Weight `json:"weights,omitempty"`
	Days    []*Day   `json:"days,omitempty"`
}
