pub mod adobe {
    use serde::{Deserialize, Serialize};
    use tobytes::ByteView;

    #[derive(Debug, Serialize, Deserialize, PartialEq)]
    pub struct Version {
        major: u16,
        minor: u16,
    }

    impl Version {
        pub fn new(major: u16, minor: u16) -> Self {
            Version { major, minor }
        }
    }

    impl ByteView for Version {
        fn byte_at(&self, index: usize) -> Option<u8> {
            if index < ByteView::byte_size(self) {
                match index {
                    0..=1 => Some(self.major.to_be_bytes()[index]),
                    2..=3 => Some(self.minor.to_be_bytes()[index - 2]),
                    _ => None,
                }
            } else {
                None
            }
        }

        fn byte_size(&self) -> usize {
            core::mem::size_of::<u16>() + core::mem::size_of::<u16>()
        }
    }

    #[derive(Debug, Serialize, Deserialize, PartialEq)]
    pub struct Cmyk {
        cyan: f32,
        magenta: f32,
        yellow: f32,
        key: f32,
    }

    impl Cmyk {
        pub fn new(cyan: f32, magenta: f32, yellow: f32, key: f32) -> Self {
            Cmyk {
                cyan,
                magenta,
                yellow,
                key,
            }
        }
    }

    impl ByteView for Cmyk {
        fn byte_at(&self, index: usize) -> Option<u8> {
            match index {
                0 => Some('C' as u8),
                1 => Some('M' as u8),
                2 => Some('Y' as u8),
                3 => Some('K' as u8),
                4..=7 => Some(self.cyan.to_be_bytes()[index - 4]),
                8..=11 => Some(self.magenta.to_be_bytes()[index - 8]),
                12..=15 => Some(self.yellow.to_be_bytes()[index - 12]),
                16..=19 => Some(self.key.to_be_bytes()[index - 16]),
                _ => None,
            }
        }

        fn byte_size(&self) -> usize {
            4 + 4 * core::mem::size_of::<f32>()
        }
    }

    #[derive(Debug, Serialize, Deserialize, PartialEq)]
    pub struct Rgb {
        red: f32,
        green: f32,
        blue: f32,
    }

    #[derive(Debug, Serialize, Deserialize, PartialEq)]
    pub struct Lab {
        l: f32,
        a: f32,
        b: f32,
    }

    #[derive(Debug, Serialize, Deserialize, PartialEq)]
    pub enum ColorModel {
        CMYK(Cmyk),
        RGB(Rgb),
        LAB(Lab),
        Grey(f32),
    }

    #[derive(Debug, Serialize, Deserialize, PartialEq)]
    pub enum ColorType {
        Global,
        Spot,
        Normal,
    }

    #[derive(Debug, Serialize, Deserialize, PartialEq)]
    pub enum BlockType {
        GroupStart,
        GroupEnd,
        ColorEntry,
    }

    #[derive(Debug, Serialize, Deserialize, PartialEq)]
    pub struct Block {
        block_type: BlockType,
        length: usize,
        name: String,
        color_model: ColorModel,
        color_type: ColorType,
    }

    impl Block {
        fn size(&self) -> usize {
            0
        }
    }

    /// Reference: http://www.selapa.net/swatches/colors/fileformats.php#adobe_ase
    #[derive(Debug, Serialize, Deserialize, PartialEq)]
    pub struct AdobeSwatchExchange {
        version: Version,
        blocks: Vec<Block>,
    }

    impl AdobeSwatchExchange {
        const FILE_SIGNATURE: [u8; 4] = [0x41, 0x53, 0x45, 0x46];

        fn size_of(blocks: &[Block]) -> usize {
            blocks.into_iter().map(|block| block.size()).sum()
        }
    }

    impl ByteView for AdobeSwatchExchange {
        fn byte_at(&self, index: usize) -> Option<u8> {
            let size = ByteView::byte_size(self);
            if index < size {
                match index {
                    // file signature
                    0..=3 => Some(AdobeSwatchExchange::FILE_SIGNATURE[index]),
                    // version
                    4 => Some(0),
                    5 => Some(0),
                    6 => Some(0),
                    7 => Some(0),
                    // blocks size
                    8 => Some(0),
                    9 => Some(0),
                    10 => Some(0),
                    11 => Some(0),
                    // blocks
                    _ => {
                        if index < size {
                            // blocks
                            Some(0)
                        } else {
                            None
                        }
                    }
                }
            } else {
                None
            }
        }

        fn byte_size(&self) -> usize {
            const FILE_SIGNATURE_SIZE: usize = 4;
            const VERSION_SIZE: usize = 4;
            const BLOCKS_SIZE: usize = 4;
            FILE_SIGNATURE_SIZE
                + VERSION_SIZE
                + BLOCKS_SIZE
                + AdobeSwatchExchange::size_of(&self.blocks)
        }
    }
}

#[cfg(test)]
mod tests {

    use super::adobe::Version;
    use crate::adobe::Cmyk;
    use tobytes::ToBytes;

    #[test]
    fn version_as_bytes() {
        let version = Version::new(10, 1);
        let bytes: Vec<u8> = version.to_bytes().collect();
        assert_eq!(vec![0x00u8, 0x0Au8, 0x00u8, 0x01u8], bytes)
    }

    #[test]
    fn cmyk_as_bytes() {
        let color = Cmyk::new(1.0, 2.0, 3.0, 4.0);
        let bytes: Vec<u8> = color.to_bytes().collect();
        assert_eq!(
            vec![
                'C' as u8, 'M' as u8, 'Y' as u8, 'K' as u8, 0x00u8, 0x00u8, 0x00u8, 0x01u8, 0x00u8,
                0x00u8, 0x00u8, 0x02u8, 0x00u8, 0x00u8, 0x00u8, 0x03u8, 0x00u8, 0x00u8, 0x00u8,
                0x04u8
            ],
            bytes
        )
    }
}
