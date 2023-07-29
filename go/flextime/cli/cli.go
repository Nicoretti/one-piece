package cli

import (
	"fmt"
	"time"
)

func CurrentMonth(now *time.Time) string {
	dispatch := map[int]string{
		1:  "Jan",
		2:  "Feb",
		3:  "Mar",
		4:  "Apr",
		5:  "May",
		6:  "June",
		7:  "July",
		8:  "Aug",
		9:  "Sept",
		10: "Oct",
		11: "Nov",
		12: "Dez",
	}
	return dispatch[int(now.Month())]
}

type Config struct {
}

type MoinCommand struct {
}

func (cmd *MoinCommand) Run(cfg *Config) error {
	fmt.Println("Executing moin command")
	return nil
}

type AddCmd struct {
	// TODO: Consider adding extra types for adding break, work
	Note  string `arg help:"Note to add to the entry."`
	Break bool   `flag help:"Is the added entry of the type break. [default: ${default}]" default:"false"`
	Tags  string `flag help:"A list of tags for the entry, e.g.: tag1,tag2,...,tagN."`
}

func (cmd *AddCmd) Run(cfg *Config) error {
	fmt.Println("Executing add command")
	fmt.Println("Note:", cmd.Note)
	fmt.Println("Break:", cmd.Break)
	fmt.Println("Tags:", cmd.Tags)
	return nil
}

// TODO: Consider using json(l) based format instead plain text
type EditCommand struct {
	// TODO: Add path to editor to be used as argument
}

func (cmd *EditCommand) Run(cfg *Config) error {
	fmt.Println("Executing edit command")
	return nil
}

type ReportCommand struct {
	Type       string `flag enum:"all,work,break" default:"all" help:"Type of report which shall be shown. [choices: ${enum}]"`
	TagsFilter string `flag help:"Flags to filter for, e.g. tag1,tag2,..,tagN."`
	Day        struct {
		DayNumber int `arg help:"Number of the day to be shown. [default: ${day}]" default:"${day}"`
	} `cmd help: "Report the specified day."`
	Week struct {
		WeekNumber int `arg help:"Number of the week to be shown. [default: ${week}]" default:"${week}"`
	} `cmd help: "Report the specified week"`
	Month struct {
		Name string `arg enum:"Jan,Feb,Mar,Apr,May,June,July,Aug,Sept,Oct,Nov,Dec" default:"${month}" help:"Short name of the month to report. [default: ${month}, choices: ${enum}]"`
	} `cmd help: "list the specified month"`
	Period struct {
		Start time.Time `arg format:"2.1.2006" help:"<day>.<month>.<year>"`
		End   time.Time `arg format:"2.1.2006" help:"<day>.<month>.<year> default: today" default:"${today}"`
	} `cmd help: "report for the given time period"`
}

func (cmd *ReportCommand) Run(cfg *Config) error {
	fmt.Println("Executing report command")
	return nil
}

type Cli struct {
	Moin   MoinCommand   `cmd help:"Start tracking time for the day."`
	Add    AddCmd        `cmd help:"Add a new time tracking entry."`
	Edit   EditCommand   `cmd help:"Edit time tracking file manually."`
	Report ReportCommand `cmd help:"Show a time report."`
}
