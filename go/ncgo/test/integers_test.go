package test

import (
	"fmt"
	"ncgo/playground"
	"testing"
)

func TestAdder(t *testing.T) {
	Assert(playground.Add(2, 2) == 4, "", t)
}

func TestTableBasedAdder(t *testing.T) {
	tests := []struct {
		lhs      int
		rhs      int
		expected int
	}{
		{lhs: 1, rhs: 2, expected: 3},
		{lhs: 5, rhs: 2, expected: 7},
		{lhs: 3, rhs: 2, expected: 5},
	}
	for index, tc := range tests {
		Expect(
			playground.Add(tc.lhs, tc.rhs) == tc.expected,
			fmt.Sprintf("Test-Case %d failed", index),
			t,
		)
	}
}

func TestTableBasedWithSubTestsAdder(t *testing.T) {
	tests := []struct {
		lhs      int
		rhs      int
		expected int
	}{
		{lhs: 1, rhs: 2, expected: 3},
		{lhs: 5, rhs: 2, expected: 7},
		{lhs: 3, rhs: 2, expected: 5},
	}
	for index, tc := range tests {
		t.Run(
			fmt.Sprintf("Test-Case-%d", index),
			func(t *testing.T) {
				Expect(playground.Add(tc.lhs, tc.rhs) == tc.expected, "", t)
			})
	}
}
