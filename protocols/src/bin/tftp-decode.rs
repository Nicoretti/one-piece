use anyhow::Result;
use human_panic::setup_panic;
use std::io::{BufWriter, Write};
use structopt::StructOpt;

mod cli {
    use structopt::StructOpt;

    #[derive(Debug, StructOpt)]
    #[structopt(
        name = "tftp-decode",
        about = "Decode a stream of binary tftp packets into a stream of jsonl"
    )]
    #[structopt(global_settings(&[structopt::clap::AppSettings::ColoredHelp]))]
    pub struct Decode {
        #[structopt(name = "input", default_value = "-")]
        #[structopt(help = "A source of a binary input stream of tftp packets")]
        pub input: bricks::cli::Input,

        #[structopt(name = "output", default_value = "-")]
        #[structopt(
            help = "Output sink where the decoded tftp packets (jsonl) shall be written to"
        )]
        pub output: bricks::cli::Output,

        #[structopt(name = "count", short = "c")]
        #[structopt(help = "amount of messages to encode before exiting")]
        pub count: Option<usize>,
    }
}

fn main() -> Result<()> {
    setup_panic!();
    let args = cli::Decode::from_args();
    let input: Box<dyn std::io::Read> = args.input.into();
    let mut output: BufWriter<Box<dyn std::io::Write>> = BufWriter::new(args.output.into());
    let parser = preidolia::parsers::ParsingIterator::new(
        preidolia::parsers::Parser::new(&protocols::tftp::parsers::tftp),
        input,
    );
    let tftp_packets: Box<dyn Iterator<Item = Result<protocols::tftp::TftpPacket>>> =
        if let Some(count) = args.count {
            Box::new(parser.take(count))
        } else {
            Box::new(parser)
        };

    for packet in tftp_packets {
        let p = packet?;
        writeln!(&mut output, "{}", serde_json::to_string(&p)?)?;
        output.flush()?;
    }
    Ok(())
}
