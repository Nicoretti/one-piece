use human_panic::setup_panic;
use structopt::StructOpt;

mod cli {
    use bricks::cli::Input;
    use std::path::PathBuf;

    #[derive(structopt::StructOpt, Debug)]
    #[structopt(about = "Decode binary data based on a grammar")]
    #[structopt(setting = structopt::clap::AppSettings::ColoredHelp)]
    pub struct Decode {
        #[structopt(name = "grammar", help = "Grammar file to process", parse(from_os_str))]
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
