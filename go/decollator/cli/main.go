package main

import (
	"encoding/json"
	"errors"
	"fmt"
	"io"
	"os"
	"text/template"
)

type Entry struct {
	Type    string
	Summary string
	Details map[string]interface{}
}

func loadEntries(reader io.Reader) ([]Entry, error) {
	var entries []Entry
	decoder := json.NewDecoder(reader)
	for {
		if err := decoder.Decode(&entries); err == io.EOF {
			return entries, nil
		} else if IsError(err) {
			return nil, errors.New(fmt.Sprintf("Error while decoding json, details: %v", err))
		}
	}
}

// IsError Indicates whether or not an actual error was signaled
func IsError(err error) bool {
	return err != nil
}

func main() {

	args := os.Args[1:]

	var reader io.Reader
	if len(args) == 1 {
		var err error
		reader, err = os.Open(args[0])
		if IsError(err) {
			fmt.Fprintf(os.Stderr, "Error while opening the input, details: %v", err)
		}
	} else {
		reader = os.Stdin
	}

	entries, err := loadEntries(reader)
	if IsError(err) {
		fmt.Fprintf(os.Stderr, "Error while loading entries, details: %v", err)
	}

	data := map[string]interface{}{
		"version":    "1.0.2",
		"date":       "2022-07-22",
		"summary":    "This release is all about foo bar",
		"added":      []Entry{},
		"changed":    []Entry{},
		"deprecated": []Entry{},
		"removed":    []Entry{},
		"fixed":      []Entry{},
		"security":   []Entry{},
	}

	for _, entry := range entries {
		list := data[entry.Type].([]Entry)
		data[entry.Type] = append(list, entry)
	}

	template := template.Template{}
	_, err = template.ParseGlob("templates/*.md")
	if IsError(err) {
		fmt.Fprintf(os.Stderr, "Error while loading the templates, details: %v", err)
	}

	err = template.ExecuteTemplate(os.Stdout, "EMOTICON_CHANGELOG.md", data)
	if IsError(err) {
		fmt.Fprintf(os.Stderr, "Error while rendering the template, details: %v", err)
	}
}
