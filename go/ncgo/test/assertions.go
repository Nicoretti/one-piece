package test

import "testing"

func validate(condition bool, message string, validator func(args ...interface{})) {
	if !condition {
		validator(message)
	}
}

func Assert(condition bool, message string, t *testing.T) {
	validate(condition, message, t.Fatal)
}

func Expect(condition bool, message string, t *testing.T) {
	validate(condition, message, t.Error)
}

// Consider adding better table test by creating a runner with generics
