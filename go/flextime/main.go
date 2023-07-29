package main

import (
	"github.com/alecthomas/kong"
	"github.com/nicoretti/flextime/cli"
	"strconv"
	"time"
)

func main() {
	var commandLine cli.Cli
	var now = time.Now()
	var _, weekNumber = time.Now().ISOWeek()
	var ctx = kong.Parse(&commandLine,
		kong.Vars{
			"today": time.Now().Format("2.1.2006"),
			"day":   strconv.FormatInt(int64(time.Now().Day()), 10),
			"week":  strconv.FormatInt(int64(weekNumber), 10),
			"month": cli.CurrentMonth(&now),
		})
	config := cli.Config{}
	err := ctx.Run(&config)
	ctx.FatalIfErrorf(err)
}
