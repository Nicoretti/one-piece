use human_panic::setup_panic;

use anyhow::{anyhow, Error};
use std::io::{BufReader, BufWriter};
use std::path::{Path, PathBuf};
use std::str::FromStr;
use structopt::StructOpt;

mod cli {
    use super::*;

    #[derive(Debug)]
    pub enum Input {
        Stdin,
        File { path: PathBuf },
    }

    #[derive(Debug)]
    pub enum Output {
        Stdout,
        File { path: PathBuf },
    }

    impl Into<BufReader<Box<dyn std::io::Read>>> for Input {
        fn into(self) -> BufReader<Box<dyn std::io::Read>> {
            match self {
                Input::Stdin => BufReader::new(Box::new(std::io::stdin())),
                Input::File { path } => BufReader::new(Box::new(std::fs::File::open(path).unwrap())),
            }
        }
    }

    impl Into<BufWriter<Box<dyn std::io::Write>>> for Output {
        fn into(self) -> BufWriter<Box<dyn std::io::Write>> {
            match self {
                Output::Stdout => BufWriter::new(Box::new(std::io::stdout())),
                Output::File { path } => BufWriter::new(Box::new(std::fs::File::open(path).unwrap())),
            }
        }
    }

    impl FromStr for Input {
        type Err = Error;
        fn from_str(s: &str) -> Result<Self, Self::Err> {
            match s.to_lowercase().as_ref() {
                "stdin" => Ok(Input::Stdin),
                _ => {
                    let path = Path::new(s).to_path_buf();
                    if path.exists() {
                        Ok(Input::File { path })
                    } else {
                        Err(anyhow!("Could not find file {:?}", path))
                    }
                }
            }
        }
    }

    impl FromStr for Output {
        type Err = Error;
        fn from_str(s: &str) -> Result<Self, Self::Err> {
            match s.to_lowercase().as_ref() {
                "stdout" => Ok(Output::Stdout),
                _ => {
                    let path = Path::new(s).to_path_buf();
                    if !path.exists() {
                        Ok(Output::File { path })
                    } else {
                        Err(anyhow!("File already exists {:?}", path))
                    }
                }
            }
        }
    }

    #[derive(structopt::StructOpt, Debug)]
    #[structopt(about = "Decode binary data based on a grammar")]
    #[structopt(setting = structopt::clap::AppSettings::ColoredHelp)]
    pub struct Decode {
        #[structopt(
        name = "grammar",
        help = "Grammar file to process",
        parse(from_os_str)
        )]
        pub grammar: PathBuf,

        #[structopt(name = "input", default_value = "stdin")]
        #[structopt(help = "input data to be decoded")]
        pub input: Input,
    }
}

fn main() {
    setup_panic!();
    let _args = cli::Decode::from_args();
}
