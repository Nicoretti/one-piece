use human_panic::setup_panic;
use pareidolia::synalize::grammar::Ufwb;
use quick_xml::de::{from_reader, DeError};
use std::fs::File;
use std::io::BufReader;
use std::path::PathBuf;
use structopt::StructOpt;

mod cli {
    use super::*;

    #[derive(structopt::StructOpt, Debug)]
    #[structopt(about = "Convert a SynalizeIt/Hexinator grammar to json")]
    #[structopt(setting = structopt::clap::AppSettings::ColoredHelp)]
    pub struct Uwfb2Json {
        #[structopt(
            name = "grammar-file",
            help = "Grammar file to process",
            parse(from_os_str)
        )]
        pub grammar: PathBuf,
    }
}

fn main() -> Result<(), std::io::Error> {
    setup_panic!();

    let args = cli::Uwfb2Json::from_args();
    let xml = File::open(args.grammar)?;
    let r = BufReader::new(xml);
    let ufwb: Result<Ufwb, DeError> = from_reader(r);
    match ufwb {
        Ok(v) => println!("{:#}", serde_json::to_string(&v).unwrap()),
        Err(e) => println!("fail {:#?}", e),
    }
    Ok(())
}
