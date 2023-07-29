use anyhow::{anyhow, Error};
use human_panic::setup_panic;
use std::path::PathBuf;
use std::str::FromStr;
use structopt::StructOpt;

mod cli {

    use super::*;

    #[derive(Debug)]
    pub enum Format {
        HexLower,
        HexUpper,
        Binary,
        Octal,
        Decimal,
    }

    impl FromStr for Format {
        type Err = Error;
        fn from_str(s: &str) -> Result<Self, Self::Err> {
            match s {
                "Hex" => Ok(Format::HexUpper),
                "hex" => Ok(Format::HexLower),
                "bin" => Ok(Format::Binary),
                "oct" => Ok(Format::Octal),
                "dec" => Ok(Format::Decimal),
                _ => Err(anyhow!("Unknown format {}.", s)),
            }
        }
    }

    #[derive(structopt::StructOpt, Debug)]
    #[structopt(about = "Dump binary data")]
    #[structopt(setting = structopt::clap::AppSettings::ColoredHelp)]
    pub struct Dump {
        #[structopt(
            name = "inputs",
            help = "Input files which shall be processed",
            default_value = "-",
            parse(from_os_str)
        )]
        pub inputs: Vec<PathBuf>,

        #[structopt(long = "config", help = "Configuration file", parse(from_os_str))]
        pub config: PathBuf,

        #[structopt(
            short = "f",
            long = "format",
            possible_values = &["Hex", "hex", "oct", "dec"],
            default_value = "Hex",
            help = "Specifies the output format"
        )]
        pub format: Format,

        #[structopt(
            short = "p",
            long = "plain-hexdump",
            help = "Output plain hexdump style"
        )]
        pub plain_hexdump: bool,

        #[structopt(
            short = "g",
            long = "group-size",
            default_value = "1",
            help = "Amount of bytes which shall be grouped"
        )]
        pub group_size: usize,

        #[structopt(
            short = "c",
            long = "columns",
            default_value = "15",
            help = "Specifies the amount of output columns"
        )]
        pub columns: usize,

        #[structopt(
            short = "l",
            long = "length",
            help = "Amount of bytes which shall be read"
        )]
        pub length: Option<usize>,

        #[structopt(
            short = "s",
            long = "seek",
            help = "Offset into the data stream where to start reading"
        )]
        pub seek: Option<usize>,
    }
}

fn main() {
    setup_panic!();
    let _config = crate::cli::Dump::from_args();
}
