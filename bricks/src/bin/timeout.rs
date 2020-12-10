#[macro_use]
extern crate clap;
#[macro_use]
extern crate human_panic;
extern crate tokio;
extern crate tokio_process;

use std::process::{exit, Command};
use std::time::Duration;

use tokio::prelude::Future;
use tokio::prelude::FutureExt;
use tokio_process::CommandExt;

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

fn main() {
    setup_panic!();
    let matches = cli::create_arg_parser().get_matches();
    let duration = value_t!(matches.value_of("duration"), u64).unwrap_or_else(|e| e.exit());
    let mut command = match matches.subcommand() {
        (name, Some(matches)) => {
            let mut c = Command::new(name);
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

    match command.spawn_async() {
        Err(e) => {
            eprintln!("Error while constructing command, details:\n {}", e);
        }
        Ok(child) => {
            let timed_command = child
                .wait_with_output()
                .timeout(Duration::from_secs(duration));
            let future = timed_command
                .map(|r| {
                    // TODO NiCo: find a good alterantive for the unwrap
                    eprint!("{}", std::str::from_utf8(&r.stderr).unwrap());
                    print!("{}", std::str::from_utf8(&r.stdout).unwrap());
                    exit(SUCCESS);
                })
                .map_err(|e| {
                    let exit_code = match e.is_elapsed() {
                        true => {
                            eprintln!("Timeout, command did not finish in time");
                            TIMEOUT
                        }
                        false => {
                            eprintln!("Command execution failed");
                            ERROR
                        }
                    };
                    exit(i32::from(exit_code));
                });
            tokio::run(future);
        }
    }
}
