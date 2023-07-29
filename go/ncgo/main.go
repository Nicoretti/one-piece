package main

import (
	"bufio"
	"errors"
	"flag"
	"fmt"
	"ncgo/playground/cesar"
	"os"
	"strings"
)

const ENCODE = 0
const DECODE = 1

func IsError(err error) bool {
	return err != nil
}

func main() {
	key := flag.Int("key", 13, "Key used for encrypting/encode the input data")
	var mode int = ENCODE
	flag.Func("mode", "Mode of operation [encode|decode] (default encode)", func(s string) error {
		switch strings.ToLower(s) {
		case "encode":
			mode = ENCODE
		case "decode":
			mode = DECODE
		default:
			return errors.New(fmt.Sprintf("<%s> Unknonw mode, use [encode | decode].", s))
		}
		return nil
	})
	flag.Parse()

	// TODO: make configurable if no filename or - is provided use stdin otherwise file
	scanner := bufio.NewScanner(os.Stdin)
	output := bufio.NewWriter(os.Stdout)
	// TODO: consider adding logging / stderr support

	result := ""
	for scanner.Scan() {
		input := scanner.Text()
		switch mode {
		case ENCODE:
			encoder := cesar.Encode{Key: *key}
			result = encoder.String(input)
		case DECODE:
			decoder := cesar.Decode{Key: *key}
			result = decoder.String(input)
		}
		fmt.Fprintln(output, result)
		output.Flush()
	}
}
