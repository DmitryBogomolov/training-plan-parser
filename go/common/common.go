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

type SimpleSet struct {
	Count int `json:"count,omitempty"`
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
