use anyhow::{Error, Result};
use human_panic::setup_panic;
use structopt::StructOpt;
use tokio;

mod cli {
    use std::net::IpAddr;
    use std::path::PathBuf;
    use structopt;

    #[derive(structopt::StructOpt, Debug)]
    #[structopt(about = "More stable elgato ring light firmware updater")]
    #[structopt(setting = structopt::clap::AppSettings::ColoredHelp)]
    pub struct Updater {
        #[structopt(
            name = "firmware",
            help = "Path to the firmware file which shall be used for the update",
            parse(from_os_str)
        )]
        pub file: PathBuf,

        #[structopt(name = "ip", help = "Ip address of the ring light")]
        pub ip: IpAddr,

        #[structopt(
            short = "d",
            long = "delay",
            default_value = "50",
            help = "inter packet delay in milli seconds"
        )]
        pub delay: usize,
    }
}

#[tokio::main]
async fn main() -> Result<()> {
    setup_panic!();
    let args = cli::Updater::from_args();
    // 1. determine firmware size
    // 2. send initial update info to start update (endpoint ...)
    // 3. while remaining size > 0: send next chunk to chunk endpoint including chunk size
    // 4. wait delay
    // 5. go to 3

    // TODO:
    // 1. Figure out max timeout delay for update process
    // 2. Get a trace from a successful update to determine if final packet or so needs to to something special
    Ok(())
}
