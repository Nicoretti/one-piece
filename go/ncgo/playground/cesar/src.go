// This file implements the cesar chiper
package cesar

import (
	"bytes"
)

type Interval struct {
	Start int
	End   int
}

func (i *Interval) Contains(value int) bool {
	return value >= i.Start && value <= i.End
}

type Encode struct {
	Key int
}

type Decode struct {
	Key int
}

const (
	LowerCase = iota
	UpperCase
	Other
)

var UpperCaseChars = Interval{Start: 65, End: 90}
var LowerCaseChars = Interval{Start: 97, End: 122}

func inputType(input byte) int {
	if UpperCaseChars.Contains(int(input)) {
		return UpperCase
	}
	if LowerCaseChars.Contains(int(input)) {
		return LowerCase
	}
	return Other
}

func (c *Encode) Byte(input byte) byte {
	base := input
	switch inputType(input) {
	case UpperCase:
		base = byte(UpperCaseChars.Start)
	case LowerCase:
		base = byte(LowerCaseChars.Start)
	}

	offset := input - base
	switch inputType(input) {
	case UpperCase:
		offset += byte(c.Key)
	case LowerCase:
		offset += byte(c.Key)
	}

	return base + (offset % 26)
}

func (c *Encode) String(plain string) string {
	var buffer bytes.Buffer
	for _, char := range plain {
		buffer.WriteByte(c.Byte(byte(char)))
	}
	return buffer.String()
}

func (c *Decode) Byte(input byte) byte {
	decoder := Encode{Key: 26 - c.Key}
	return decoder.Byte(input)
}

func (c *Decode) String(cipher string) string {
	var buffer bytes.Buffer
	for _, char := range cipher {
		buffer.WriteByte(c.Byte(byte(char)))
	}
	return buffer.String()
}
