use anyhow::{format_err, Result};
use human_panic::setup_panic;
use itertools::Itertools;
use reqwest::{ClientBuilder, StatusCode};
use std::io::Read;
use structopt::StructOpt;
use tokio::time::{sleep, Duration};

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
            name = "ms",
            short = "d",
            long = "delay",
            default_value = "25",
            help = "inter packet delay in milli seconds"
        )]
        pub delay: u64,

        #[structopt(
            name = "bytes",
            short = "c",
            long = "chunk-size",
            default_value = "4096",
            help = "size of individually transferred chunks in bytes"
        )]
        pub chunk_size: usize,

        #[structopt(
            name = "count",
            long = "chunk-retries",
            help = "Amount of retires for a single chunk upload, if not specified it will retry until chunk upload succeeds"
        )]
        pub chunk_retries: Option<usize>,
    }
}

#[tokio::main]
async fn main() -> Result<()> {
    setup_panic!();
    let args = cli::Updater::from_args();
    let firmware = std::fs::File::open(args.file)?;

    let client = ClientBuilder::new().gzip(true).deflate(true).build()?;

    // 1. determine firmware size
    let size = firmware.metadata()?.len();

    // 2. start firmware update upload and signal firmware size
    let prepare_update = client
        .put(format!(
            "http://{}:9123/elgato/firmware-update/prepare",
            args.ip
        ))
        .body(format!("{{\"size\":{}}}", size))
        .build()?;

    client.execute(prepare_update).await?;

    // 3. while remaining size > 0: send next chunk to chunk endpoint including chunk size
    let mut offset: usize = 0;
    for chunk in firmware.bytes().chunks(args.chunk_size).into_iter() {
        let data: Vec<u8> = chunk.filter_map(|r| r.ok()).collect();
        let size = data.len();

        let mut success = false;
        let mut retries = 0usize;
        while !success {
            // maximum retries for a chunk reached
            if let Some(max_retries) = args.chunk_retries {
                if retries >= max_retries {
                    return Err(format_err!(
                        "Reached the maximum amount of retries for a chunk, details: offset={}",
                        offset
                    ));
                }
                retries += 1;
            }

            let upload_data = client
                .put(format!(
                    "http://{}:9123/elgato/firmware-update/data?offset={}",
                    args.ip, offset,
                ))
                .body(data.clone())
                .build()?;
            let status = client.execute(upload_data).await?.status();
            if status == StatusCode::ACCEPTED {
                success = true;
            } else {
                sleep(Duration::from_millis(args.delay)).await;
            }
        }
        offset += size;
    }

    // 4. tell ring light to execute/install firmware update
    let execute_update = client
        .post(format!(
            "http://{}:9123/elgato/firmware-update/execute",
            args.ip
        ))
        .build()?;

    match client.execute(execute_update).await?.status() {
        StatusCode::OK => Ok(()),
        status => Err(format_err!("Update failed, details {}", status)),
    }
}
