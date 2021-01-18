use serde::{Deserialize, Serialize};

pub mod Adobe {
    use tobytes::ByteView;

    #[derive(Debug, Serialize, Deserialize, PartialEq)]
    pub struct Version {
        major: usize,
        minor: usize,
    }

    #[derive(Debug, Serialize, Deserialize, PartialEq)]
    pub enum ColorModel {
        CMYK {
            cyan: f32,
            magenta: f32,
            yellow: f32,
            key: f32,
        },
        RGB {
            red: f32,
            green: f32,
            blue: f32,
        },
        LAB {
            l: f32,
            a: f32,
            b: f32,
        },
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
        color_type: Type,
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
            let last_index = size - 1;
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
                    12..=last_index => Some(0),
                    // catch everything else
                    _ => None,
                }
            } else {
                None
            }
        }

        fn byte_size(&self) -> usize {
            const FILE_SIGNATURE_SIZE: usize = 4;
            const VERSION_SIZE: usize = 4;
            const BLOCKS_SIZE: usize = 4;
            FILE_SIGNATURE_SIZE + VERSION_SIZE + BLOCKS_SIZE + self.size_of(&self.blocks)
        }
    }
}

#[cfg(test)]
mod tests {
    #[test]
    fn it_works() {
        assert_eq!(2 + 2, 4);
    }
}
