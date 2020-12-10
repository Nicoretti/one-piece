extern crate bricks;
extern crate structopt;

use cli::Spaces;
use std::io;
use std::path::PathBuf;
use structopt::StructOpt;

mod cli {

    use super::*;

    #[derive(structopt::StructOpt, Debug)]
    #[structopt(about = "Replace tabs with spaces")]
    #[structopt(raw(setting = "structopt::clap::AppSettings::ColoredHelp"))]
    pub struct Spaces {
        #[structopt(
            name = "file",
            help = "file to process, if none is specified stdin will be processed",
            parse(from_os_str)
        )]
        pub file: Option<PathBuf>,

        #[structopt(
            short = "n",
            long = "number-of-spaces",
            default_value = "4",
            help = "of spaces which shall be used to replace one tab"
        )]
        pub number_of_spaces: usize,
    }

}

fn main() -> io::Result<()> {
    let config = Spaces::from_args();
    let _input_file: String = if let Some(path) = config.file {
        path.to_str().unwrap().to_string()
    } else {
        String::from("stdin")
    };
    // TODO: Add actual implementation/functionality
    // let mut reader = bricks::create_reader(&input_file)?;
    std::process::exit(1);
}
