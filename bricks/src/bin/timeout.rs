use clap::value_t;
use human_panic::setup_panic;
use tokio::time::timeout;

use std::process::exit;
use std::time::Duration;

pub const SUCCESS: i32 = 0;
pub const TIMEOUT: i32 = 1;
pub const ERROR: i32 = 2;

mod cli {

    use structopt::clap::{App, AppSettings, Arg};

    pub fn create_arg_parser<'a, 'b>() -> App<'a, 'b> {
        App::new("timeout")
            .about("Monitor a command to make sure it finishes in time.")
            .usage("timeout [OPTIONS] <COMMAND> [ARGS]...")
            .setting(AppSettings::AllowExternalSubcommands)
            .setting(AppSettings::ArgRequiredElseHelp)
            .setting(AppSettings::UnifiedHelpMessage)
            .arg(
                Arg::with_name("duration")
                    .short("d")
                    .long("duration")
                    .default_value("5")
                    .takes_value(true)
                    .help("specify the duration in seconds"),
            )
    }
}

#[tokio::main]
async fn main() {
    setup_panic!();
    let matches = cli::create_arg_parser().get_matches();
    let duration = value_t!(matches.value_of("duration"), u64).unwrap_or_else(|e| e.exit());
    let mut command = match matches.subcommand() {
        (name, Some(matches)) => {
            let mut c = tokio::process::Command::new(name);
            let args = matches
                .values_of("")
                .map(|v| v.collect())
                .unwrap_or(Vec::new());
            for argument in args {
                c.arg(argument);
            }
            c
        }
        _ => {
            eprintln!("{}", matches.usage());
            exit(ERROR)
        }
    };

    match command.spawn() {
        Err(e) => {
            eprintln!("Error while constructing command, details:\n {}", e);
        }
        Ok(child) => {
            let timed_command = timeout(Duration::from_secs(duration), child.wait_with_output());
            timed_command
                .await
                .map(|r| {
                    // TODO NiCo: find a good alterantive for the unwrap
                    r.map(|output| {
                        eprint!("{}", std::str::from_utf8(&output.stderr).unwrap());
                        print!("{}", std::str::from_utf8(&output.stdout).unwrap());
                        exit(SUCCESS);
                    })
                    .map_err(|e| {
                        eprintln!("Error while executing command, details: {}", e);
                        exit(ERROR);
                    })
                })
                .map_err(|_e| {
                    eprintln!("Timeout, command did not finish in time");
                    exit(TIMEOUT);
                });
        }
    }
}
