//! foo trailing is the most amazing foo
#[macro_use]
extern crate human_panic;
extern crate bricks;
extern crate structopt;

use cli::Trailing;
use std::io;
use std::path::PathBuf;
use structopt::StructOpt;

mod cli {

    use super::*;

    #[derive(structopt::StructOpt, Debug)]
    #[structopt(about = "Remove trailing whitespaces")]
    #[structopt(raw(setting = "structopt::clap::AppSettings::ColoredHelp"))]
    pub struct Trailing {
        #[structopt(
            name = "file",
            help = "file to process, if none is specified stdin will be processed",
            parse(from_os_str)
        )]
        pub file: Option<PathBuf>,

        #[structopt(
            short = "c",
            long = "check",
            help = "check the file for trailing ws instead of fixing it"
        )]
        pub check: bool,
    }

}

fn main() -> io::Result<()> {
    setup_panic!();
    let config = Trailing::from_args();
    let input_file = if let Some(path) = config.file {
        path.to_str().unwrap().to_string()
    } else {
        String::from("stdin")
    };
    let mut reader = bricks::create_reader(&input_file)?;
    if config.check {
        let file_reporter = bricks::reporter::FileReporter::new(&input_file);
        let reported_issues =
            bricks::process(&mut reader, &mut io::stdout(), |mut reader, mut writer| {
                file_reporter.report_trailing_whitespaces(&mut reader, &mut writer)
            })?;
        match reported_issues {
            0 => std::process::exit(0),
            _ => std::process::exit(1),
        }
    } else {
        let _bytes_written = bricks::process(
            &mut reader,
            &mut io::stdout(),
            bricks::transformations::remove_trailing_whitespaces,
        )?;
        std::process::exit(0);
    }
}
