use serde::{Deserialize, Serialize};
use tobytes::{ByteView, ToBytes};

/// Tftp transfer modes
#[derive(PartialEq, Debug, Eq, Serialize, Deserialize)]
#[serde(rename = "mode")]
pub enum Mode {
    /// Ascii mode see also telnet
    #[serde(rename = "netascii")]
    Netascii,
    /// also called binary in older implementations
    #[serde(rename = "octet")]
    Octet,
}

impl Mode {
    pub fn from(string: &str) -> Self {
        match string {
            "octet" => Mode::Octet,
            "netascii" => Mode::Netascii,
            _ => panic!(),
        }
    }
}

impl ByteView for Mode {
    fn byte_at(&self, index: usize) -> Option<u8> {
        match self {
            Mode::Octet => "octet\0".as_bytes(),
            Mode::Netascii => "netascii\0".as_bytes(),
        }
        .get(index)
        .cloned()
    }

    fn byte_size(&self) -> usize {
        ToBytes::to_bytes(self).count()
    }
}

#[derive(PartialEq, Debug, Eq, Serialize, Deserialize)]
/// Tftp error codes
#[serde(rename = "error")]
pub enum Error {
    /// 0: Not defined, see error message (if any)
    #[serde(rename = "undefined")]
    Undefinied { message: String },
    /// 1: File not found
    #[serde(rename = "file_not_found")]
    FileNotFound { message: String },
    /// 2: Access violation
    #[serde(rename = "access_violation")]
    AccessViolation { message: String },
    /// 3: Disk full or allocation exceeded
    #[serde(rename = "disk_full")]
    DiskFull { message: String },
    /// 4: Illegal TFTP operation
    #[serde(rename = "illegal_tftp_operation")]
    IllegalTftpOperation { message: String },
    /// 5: Unknown transfer ID
    #[serde(rename = "unkown_transfer_id")]
    UnkownTransferId { message: String },
    /// 6: File already exists.
    #[serde(rename = "file_already_exists")]
    FileAlreadyExists { message: String },
    /// 7: No such user
    #[serde(rename = "no_such_user")]
    NoSuchUser { message: String },
}

impl ByteView for Error {
    fn byte_at(&self, index: usize) -> Option<u8> {
        let (id, msg) = match *self {
            Error::Undefinied { ref message } => (0u16, message),
            Error::FileNotFound { ref message } => (1u16, message),
            Error::AccessViolation { ref message } => (2u16, message),
            Error::DiskFull { ref message } => (3, message),
            Error::IllegalTftpOperation { ref message } => (4u16, message),
            Error::UnkownTransferId { ref message } => (5u16, message),
            Error::FileAlreadyExists { ref message } => (6u16, message),
            Error::NoSuchUser { ref message } => (7u16, message),
        };
        id.to_be_bytes()
            .iter()
            .chain(msg.as_bytes().iter())
            .chain(std::iter::once(&0u8))
            .nth(index)
            .cloned()
    }

    fn byte_size(&self) -> usize {
        ToBytes::to_bytes(self).count()
    }
}

// TODO NiCo: add mode for rrq and wrq -> right now it allways will be octett
// TODO NiCo: optimize memory efficiency -> String -> &str, Vec<u8> -> &[u8]
/// Defines all available types of tftp packets
#[derive(PartialEq, Debug, Eq, Serialize, Deserialize)]
#[serde(rename = "tftp_packet")]
pub enum TftpPacket {
    /// Opcode 0x01
    #[serde(rename = "read_request")]
    ReadRequest {
        #[serde(rename = "file_name")]
        filename: String,
        mode: Mode,
    },
    /// Opcode 0x02
    #[serde(rename = "write_request")]
    WriteRequest {
        #[serde(rename = "file_name")]
        filename: String,
        mode: Mode,
    },
    /// Opcode 0x03
    #[serde(rename = "data")]
    Data { block: u16, data: Vec<u8> }, // make data a slice -> ref so it does not need allocate memory by itself
    /// Opcode 0x04
    #[serde(rename = "ack")]
    Ack { block: u16 },
    /// Opcode 0x05
    #[serde(rename = "error")]
    Error { error: Error },
}

impl ByteView for TftpPacket {
    fn byte_at(&self, index: usize) -> Option<u8> {
        match self {
            TftpPacket::ReadRequest { filename, mode } => 1u16
                .to_be_bytes()
                .iter()
                .cloned()
                .chain(filename.as_bytes().iter().cloned())
                .chain(std::iter::once(0u8))
                .chain(mode.to_bytes())
                .nth(index),
            TftpPacket::WriteRequest { filename, mode } => 2u16
                .to_be_bytes()
                .iter()
                .cloned()
                .chain(filename.as_bytes().iter().cloned())
                .chain(std::iter::once(0u8))
                .chain(mode.to_bytes())
                .nth(index),
            TftpPacket::Data { block, data } => 3u16
                .to_be_bytes()
                .iter()
                .cloned()
                .chain(block.to_be_bytes().iter().cloned())
                .chain(data.iter().cloned())
                .nth(index),
            TftpPacket::Ack { block } => 4u16
                .to_be_bytes()
                .iter()
                .chain(block.to_be_bytes().iter())
                .nth(index)
                .cloned(),
            TftpPacket::Error { error } => 5u16
                .to_be_bytes()
                .iter()
                .cloned()
                .chain(error.to_bytes())
                .nth(index),
        }
    }

    fn byte_size(&self) -> usize {
        ToBytes::to_bytes(self).count()
    }
}

#[cfg(test)]
mod tests {

    use super::*;

    #[test]
    fn serialize_read_request() {
        let rrq = TftpPacket::ReadRequest {
            filename: String::from("file.txt"),
            mode: Mode::Octet,
        };
        let expected: Vec<u8> = vec![
            0x00, 0x01, // opcode
            0x66, 0x69, 0x6c, 0x65, 0x2e, 0x74, 0x78, 0x74, // filename
            0x00, // 0 terminator
            0x6f, 0x63, 0x74, 0x65, 0x74, // mode
            0x00, // 0 terminator
        ];

        assert_eq!(expected, rrq.to_bytes().collect::<Vec<u8>>());
    }

    #[test]
    fn serialize_write_request() {
        let wrq = TftpPacket::WriteRequest {
            filename: String::from("file.txt"),
            mode: Mode::Octet,
        };
        let expected: Vec<u8> = vec![
            0x00, 0x02, // opcode
            0x66, 0x69, 0x6c, 0x65, 0x2e, 0x74, 0x78, 0x74, // filename
            0x00, // 0 terminator
            0x6f, 0x63, 0x74, 0x65, 0x74, // mode
            0x00, // 0 terminator
        ];

        assert_eq!(expected, wrq.to_bytes().collect::<Vec<u8>>());
    }

    #[test]
    fn serialize_data() {
        let payload = vec![0x66, 0x69, 0x6c, 0x65, 0x2e, 0x74, 0x78, 0x74];
        let data = TftpPacket::Data {
            block: 1,
            data: payload,
        };
        let expected: Vec<u8> = vec![
            0x00, 0x03, // opcode
            0x00, 0x01, // block id
            0x66, 0x69, 0x6c, 0x65, 0x2e, 0x74, 0x78, 0x74, // data
        ];

        assert_eq!(expected, data.to_bytes().collect::<Vec<u8>>());
    }

    #[test]
    fn serialize_ack() {
        let data = TftpPacket::Ack { block: 1 };
        let expected: Vec<u8> = vec![
            0x00, 0x04, // opcode
            0x00, 0x01, // block id
        ];

        assert_eq!(expected, data.to_bytes().collect::<Vec<u8>>());
    }

    #[test]
    fn serialize_error() {
        let error = Error::Undefinied {
            message: String::from("undefined error"),
        };
        let data = TftpPacket::Error { error };
        let expected: Vec<u8> = vec![
            0x00, 0x05, // opcode
            0x00, 0x00, // error code
            0x75, 0x6e, 0x64, 0x65, 0x66, 0x69, 0x6e, // error message
            0x65, 0x64, 0x20, 0x65, 0x72, 0x72, 0x6f, 0x72, // "undefined error"
            0x00, // 0 terminator
        ];

        assert_eq!(expected, data.to_bytes().collect::<Vec<u8>>());
    }
}

pub mod parsers {
    use super::{Error, Mode, TftpPacket};
    use nom::number::complete::be_u8;
    use nom::number::streaming::be_u16;
    use nom::{do_parse, many0, map, map_res, named, switch, take, take_until};

    named!(string<&[u8], &str>,
        do_parse!(
            string: map_res!(take_until!("\0"), ::std::str::from_utf8) >>
            take!(1) >>
            (string)
        )
    );

    // FIXME: either parse 512 byte or to the enf if < 512
    named!(data<&[u8], Vec<u8>>, many0!(be_u8));
    named!(opcode<&[u8], u16>, do_parse!(value: be_u16 >> (value)));
    named!(block<&[u8], u16>, do_parse!(value: be_u16 >> (value)));
    named!(error_code<&[u8], u16>, do_parse!( value: be_u16 >> (value)));
    named!(mode<&[u8], Mode>, map!(string, Mode::from));

    named!(error<&[u8], Error>,
        switch!(error_code,
            0 => do_parse!( msg: string >> (Error::Undefinied { message: String::from(msg) }))                  |
            1 => do_parse!( msg: string >> (Error::FileNotFound { message: String::from(msg) }))                |
            2 => do_parse!( msg: string >> (Error::AccessViolation { message: String::from(msg) }))             |
            3 => do_parse!( msg: string >> (Error::DiskFull { message: String::from(msg) }))                    |
            4 => do_parse!( msg: string >> (Error::IllegalTftpOperation { message: String::from(msg) }))        |
            5 => do_parse!( msg: string >> (Error::UnkownTransferId { message: String::from(msg) }))            |
            6 => do_parse!( msg: string >> (Error::FileAlreadyExists { message: String::from(msg) }))           |
            7 => do_parse!( msg: string >> (Error::NoSuchUser { message: String::from(msg) }))
         )
    );

    // FIXME NiCo: what happens if unknonw value occurs?
    named!(pub tftp<&[u8], TftpPacket>,
               switch!(opcode,
                1 => do_parse!(
                    name: string >>
                    mode: string >>
                    (TftpPacket::ReadRequest { filename: String::from(name), mode: Mode::from(mode) }))         |
                2 => do_parse!(
                    name: string >>
                    mode: string >>
                    (TftpPacket::WriteRequest { filename: String::from(name), mode: Mode::from(mode) }))        |
                3 => do_parse!(
                    id: block >>
                    payload: data >>
                    (TftpPacket::Data { block: id, data: payload }))                    |
                4 => do_parse!(id : block >> (TftpPacket::Ack { block : id }))          |
                5 => do_parse!(err : error >> (TftpPacket::Error { error: err }))
                )
    );

    #[cfg(test)]
    mod tests {
        use super::*;
        use nom::IResult;

        #[test]
        fn parse_string() {
            let expected = nom::IResult::Ok((&b""[..], "file.txt"));
            let input: Vec<u8> = vec![
                0x66, 0x69, 0x6c, 0x65, 0x2e, 0x74, 0x78, 0x74, // filename
                0x00, // 0 terminator
            ];

            assert_eq!(string(&input), expected);
        }

        #[test]
        fn parse_data() {
            let expected = IResult::Ok((&b""[..], vec![0, 1, 2, 3, 4, 5]));
            let input: Vec<u8> = vec![0, 1, 2, 3, 4, 5];
            assert_eq!(data(&input), expected);
        }

        #[test]
        fn parse_opcode() {
            assert_eq!(opcode(&[0x00, 0x00]), IResult::Ok((&b""[..], 0)));
            assert_eq!(opcode(&[0x00, 0x01]), IResult::Ok((&b""[..], 1)));
            assert_eq!(opcode(&[0x00, 0x02]), IResult::Ok((&b""[..], 2)));
            assert_eq!(opcode(&[0x00, 0x03]), IResult::Ok((&b""[..], 3)));
            assert_eq!(opcode(&[0x00, 0x04]), IResult::Ok((&b""[..], 4)));
            assert_eq!(opcode(&[0x00, 0x05]), IResult::Ok((&b""[..], 5)));
        }

        #[test]
        fn parse_block() {
            assert_eq!(block(&[0x01, 0x00]), IResult::Ok((&b""[..], 0x0100)));
            assert_eq!(block(&[0x10, 0x01]), IResult::Ok((&b""[..], 0x1001)));
            assert_eq!(block(&[0x00, 0x02]), IResult::Ok((&b""[..], 0x0002)));
            assert_eq!(block(&[0xF0, 0x03]), IResult::Ok((&b""[..], 0xF003)));
            assert_eq!(block(&[0x00, 0xFF]), IResult::Ok((&b""[..], 0x00FF)));
            assert_eq!(block(&[0x00, 0x05]), IResult::Ok((&b""[..], 0x0005)));
        }

        #[test]
        fn parse_error_code() {
            assert_eq!(error_code(&[0x00, 0x00]), IResult::Ok((&b""[..], 0)));
            assert_eq!(error_code(&[0x00, 0x01]), IResult::Ok((&b""[..], 1)));
            assert_eq!(error_code(&[0x00, 0x02]), IResult::Ok((&b""[..], 2)));
            assert_eq!(error_code(&[0x00, 0x03]), IResult::Ok((&b""[..], 3)));
            assert_eq!(error_code(&[0x00, 0x04]), IResult::Ok((&b""[..], 4)));
            assert_eq!(error_code(&[0x00, 0x05]), IResult::Ok((&b""[..], 5)));
            assert_eq!(error_code(&[0x00, 0x06]), IResult::Ok((&b""[..], 6)));
            assert_eq!(error_code(&[0x00, 0x07]), IResult::Ok((&b""[..], 7)));
        }

        #[test]
        fn parse_mode() {
            assert_eq!(mode(&b"octet\0"[..]), IResult::Ok((&b""[..], Mode::Octet)));
            assert_eq!(
                mode(&b"netascii\0"[..]),
                IResult::Ok((&b""[..], Mode::Netascii))
            );
        }

        #[test]
        fn parse_error() {
            let expected = IResult::Ok((
                &b""[..],
                Error::Undefinied {
                    message: String::from("file.txt"),
                },
            ));
            let input: Vec<u8> = vec![
                0x00, 0x00, // error code
                0x66, 0x69, 0x6c, 0x65, 0x2e, 0x74, 0x78, 0x74, // error msg (file.txt)
                0x00, // 0 terminator
            ];

            assert_eq!(error(&input), expected);
        }

        #[test]
        fn parse_tftp_rrq() {
            let expected = IResult::Ok((
                &b""[..],
                TftpPacket::ReadRequest {
                    filename: String::from("file.txt"),
                    mode: Mode::Octet,
                },
            ));
            let input: Vec<u8> = vec![
                0x00, 0x01, // opcode
                0x66, 0x69, 0x6c, 0x65, 0x2e, 0x74, 0x78, 0x74, // filename  (file.txt)
                0x00, // 0 terminator
                0x6f, 0x63, 0x74, 0x65, 0x74, // mode
                0x00, // 0 terminator
            ];

            assert_eq!(tftp(&input), expected);
        }

        #[test]
        fn parse_tftp_wrq() {
            let expected = IResult::Ok((
                &b""[..],
                TftpPacket::WriteRequest {
                    filename: String::from("file.txt"),
                    mode: Mode::Octet,
                },
            ));
            let input: Vec<u8> = vec![
                0x00, 0x02, // opcode
                0x66, 0x69, 0x6c, 0x65, 0x2e, 0x74, 0x78, 0x74, // filename  (file.txt)
                0x00, // 0 terminator
                0x6f, 0x63, 0x74, 0x65, 0x74, // mode
                0x00, // 0 terminator
            ];

            assert_eq!(tftp(&input), expected);
        }

        #[test]
        fn parse_tftp_data() {
            let expected = IResult::Ok((
                &b""[..],
                TftpPacket::Data {
                    block: 2,
                    data: vec![0x66, 0x69, 0x6c, 0x65, 0x2e, 0x74, 0x78, 0x74],
                },
            ));
            let input: Vec<u8> = vec![
                0x00, 0x03, // opcode
                0x00, 0x02, // blockid
                0x66, 0x69, 0x6c, 0x65, 0x2e, 0x74, 0x78, 0x74, // data
            ];

            assert_eq!(tftp(&input), expected);
        }

        #[test]
        fn parse_tftp_ack() {
            let expected = IResult::Ok((&b""[..], TftpPacket::Ack { block: 2 }));
            let input: Vec<u8> = vec![
                0x00, 0x04, // opcode
                0x00, 0x02, // blockid
            ];

            assert_eq!(tftp(&input), expected);
        }

        #[test]
        fn parse_tftp_error() {
            let expected = IResult::Ok((
                &b""[..],
                TftpPacket::Error {
                    error: Error::Undefinied {
                        message: String::from("file.txt"),
                    },
                },
            ));
            let input: Vec<u8> = vec![
                0x00, 0x05, // opcode
                0x00, 0x00, // error code
                0x66, 0x69, 0x6c, 0x65, 0x2e, 0x74, 0x78, 0x74, // error msg (file.txt)
                0x00, // 0 terminator
            ];

            assert_eq!(tftp(&input), expected);
        }
    }
}
