use anyhow::Result;
use human_panic::setup_panic;
use std::io::{BufRead, BufReader, BufWriter, Write};
use structopt::StructOpt;
use tobytes::ToBytes;

mod cli {
    use structopt::StructOpt;

    #[derive(Debug, StructOpt)]
    #[structopt(
        name = "tftp-encode",
        about = "Encode tftp packets into their binary representation"
    )]
    #[structopt(global_settings(&[structopt::clap::AppSettings::ColoredHelp]))]
    pub struct Encode {
        #[structopt(name = "input", default_value = "-")]
        #[structopt(help = "jsonl based input which will be encoded")]
        pub input: bricks::cli::Input,

        #[structopt(name = "output", default_value = "-")]
        #[structopt(help = "Output sink where the encoded data shall be written to")]
        pub output: bricks::cli::Output,

        #[structopt(name = "count", short = "c")]
        #[structopt(help = "amount of messages to encode before exiting")]
        pub count: Option<usize>,
    }
}

fn main() -> Result<()> {
    setup_panic!();
    let args = cli::Encode::from_args();
    let input: BufReader<Box<dyn std::io::Read>> = BufReader::new(args.input.into());
    let mut output: BufWriter<Box<dyn std::io::Write>> = BufWriter::new(args.output.into());
    let lines: Box<dyn Iterator<Item = std::io::Result<String>>> = if let Some(count) = args.count {
        Box::new(input.lines().take(count).into_iter())
    } else {
        Box::new(input.lines())
    };

    for line in lines {
        let tftp_packet: protocols::tftp::TftpPacket = serde_json::from_str(&line?)?;
        output.write(tftp_packet.to_bytes().collect::<Vec<u8>>().as_slice())?;
        output.flush()?;
    }
    Ok(())
}
