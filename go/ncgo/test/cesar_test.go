package test

import (
	"fmt"
	"ncgo/playground/cesar"
	"testing"
)

func TestCesarEncode(t *testing.T) {
	tests := []struct {
		input    byte
		key      int
		expected byte
	}{
		{input: 'a', expected: 'b', key: 1},
		{input: 'A', expected: 'B', key: 1},
		{input: '?', expected: '?', key: 1},
		{input: '?', expected: '?', key: 5},
	}
	for index, tc := range tests {
		t.Run(
			fmt.Sprintf("Test-Case-%d", index),
			func(t *testing.T) {
				cesar := cesar.Encode{tc.key}
				actual := cesar.Byte(tc.input)
				Expect(
					actual == tc.expected,
					fmt.Sprintf("Expected: %d, Actual: %d", tc.expected, actual),
					t,
				)
			})
	}
}
