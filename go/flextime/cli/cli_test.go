package cli

import (
	"testing"
	"time"
)

type currentMonthTestData struct {
	input    time.Time
	expected string
}

var currentMonthTets = []currentMonthTestData{

	{time.Date(2022, 1, 1, 0, 0, 0, 0, time.Local), "Jan"},
	{time.Date(2022, 2, 1, 0, 0, 0, 0, time.Local), "Feb"},
	{time.Date(2022, 3, 1, 0, 0, 0, 0, time.Local), "Mar"},
	{time.Date(2022, 4, 1, 0, 0, 0, 0, time.Local), "Apr"},
	{time.Date(2022, 5, 1, 0, 0, 0, 0, time.Local), "May"},
	{time.Date(2022, 6, 1, 0, 0, 0, 0, time.Local), "June"},
	{time.Date(2022, 7, 1, 0, 0, 0, 0, time.Local), "July"},
	{time.Date(2022, 8, 1, 0, 0, 0, 0, time.Local), "Aug"},
	{time.Date(2022, 9, 1, 0, 0, 0, 0, time.Local), "Sept"},
	{time.Date(2022, 10, 1, 0, 0, 0, 0, time.Local), "Oct"},
	{time.Date(2022, 11, 1, 0, 0, 0, 0, time.Local), "Nov"},
	{time.Date(2022, 12, 1, 0, 0, 0, 0, time.Local), "Dez"},
}

func Test_GetCurrentMonth(t *testing.T) {

	for _, test := range currentMonthTets {
		if got := CurrentMonth(&test.input); got != test.expected {
			t.Errorf("got %q, wanted %q", got, test.expected)
		}
	}
}
