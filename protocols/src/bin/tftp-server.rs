use anyhow::Result;
use nom::AsBytes;

#[tokio::main]
async fn main() -> Result<()> {
    let _dir = std::path::Path::new(".");
    let addr = "127.0.0.1:9999";
    let listener = tokio::net::UdpSocket::bind(addr).await?;
    let mut receive_buffer = [0u8; 1024];

    loop {
        let (amount, src): (usize, std::net::SocketAddr) =
            listener.recv_from(&mut receive_buffer).await?;
        let data = &receive_buffer[..amount];
        println!("amount: {:?},  src: {:?}", amount, src);
        {
            let (_remains, packet) = protocols::tftp::parsers::tftp(data).unwrap();
            println!("{:?}", packet);

            let con = tokio::net::UdpSocket::bind("127.0.0.1:9998").await?;
            con.connect(src).await?;
            let r = con.send(b"Foo bar and stuff\n".as_bytes()).await?;
            println!("sent {} bytes", r);
            let _server_tid = 4000;
        }
    }
}
