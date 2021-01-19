pub mod adobe {
    use nom::AsBytes;
    use serde::{Deserialize, Serialize};
    use tobytes::{ByteView, ToBytes};

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

    impl ByteView for Rgb {
        fn byte_at(&self, index: usize) -> Option<u8> {
            match index {
                0 => Some('R' as u8),
                1 => Some('G' as u8),
                2 => Some('B' as u8),
                3 => Some(0u8),
                4..=7 => Some(self.red.to_be_bytes()[index - 4]),
                8..=11 => Some(self.green.to_be_bytes()[index - 8]),
                12..=15 => Some(self.blue.to_be_bytes()[index - 12]),
                _ => None,
            }
        }

        fn byte_size(&self) -> usize {
            4 + 3 * core::mem::size_of::<f32>()
        }
    }

    #[derive(Debug, Serialize, Deserialize, PartialEq)]
    pub struct Lab {
        l: f32,
        a: f32,
        b: f32,
    }

    impl ByteView for Lab {
        fn byte_at(&self, index: usize) -> Option<u8> {
            match index {
                0 => Some('L' as u8),
                1 => Some('A' as u8),
                2 => Some('B' as u8),
                3 => Some(0u8),
                4..=7 => Some(self.l.to_be_bytes()[index - 4]),
                8..=11 => Some(self.a.to_be_bytes()[index - 8]),
                12..=15 => Some(self.b.to_be_bytes()[index - 12]),
                _ => None,
            }
        }

        fn byte_size(&self) -> usize {
            4 + 3 * core::mem::size_of::<f32>()
        }
    }

    #[derive(Debug, Serialize, Deserialize, PartialEq)]
    pub struct Grey {
        grey: f32,
    }

    impl ByteView for Grey {
        fn byte_at(&self, index: usize) -> Option<u8> {
            match index {
                0 => Some('G' as u8),
                1 => Some('R' as u8),
                2 => Some('E' as u8),
                3 => Some('Y' as u8),
                4..=7 => Some(self.grey.to_be_bytes()[index - 4]),
                _ => None,
            }
        }

        fn byte_size(&self) -> usize {
            4 + core::mem::size_of::<f32>()
        }
    }

    #[derive(Debug, Serialize, Deserialize, PartialEq)]
    pub enum ColorModel {
        CMYK(Cmyk),
        RGB(Rgb),
        LAB(Lab),
        Grey(f32),
    }

    impl ByteView for ColorModel {
        fn byte_at(&self, index: usize) -> Option<u8> {
            match self {
                ColorModel::CMYK(cmyk) => cmyk.byte_at(index),
                ColorModel::RGB(rgb) => rgb.byte_at(index),
                ColorModel::LAB(lab) => lab.byte_at(index),
                ColorModel::Grey(grey) => grey.byte_at(index),
            }
        }

        fn byte_size(&self) -> usize {
            match self {
                ColorModel::CMYK(cmyk) => cmyk.byte_size(),
                ColorModel::RGB(rgb) => rgb.byte_size(),
                ColorModel::LAB(lab) => lab.byte_size(),
                ColorModel::Grey(grey) => grey.byte_size(),
            }
        }
    }

    #[derive(Debug, Serialize, Deserialize, PartialEq)]
    pub enum ColorType {
        Global,
        Spot,
        Normal,
    }

    impl ByteView for ColorType {
        fn byte_at(&self, index: usize) -> Option<u8> {
            let value: u16 = match self {
                ColorType::Global => 0,
                ColorType::Spot => 1,
                ColorType::Normal => 2,
            };
            match index {
                0..=1 => Some(value.to_be_bytes()[index]),
                _ => None,
            }
        }

        fn byte_size(&self) -> usize {
            core::mem::size_of::<u16>()
        }
    }

    #[derive(Debug, Serialize, Deserialize, PartialEq)]
    pub enum BlockType {
        GroupStart,
        GroupEnd,
        ColorEntry,
    }

    impl ByteView for BlockType {
        fn byte_at(&self, index: usize) -> Option<u8> {
            let value: u16 = match self {
                BlockType::GroupStart => 0xc001,
                BlockType::GroupEnd => 0xc002,
                BlockType::ColorEntry => 0x0001,
            };
            match index {
                0..=1 => Some(value.to_be_bytes()[index]),
                _ => None,
            }
        }

        fn byte_size(&self) -> usize {
            core::mem::size_of::<u16>()
        }
    }

    #[derive(Debug, Serialize, Deserialize, PartialEq)]
    pub struct Block {
        block_type: BlockType,
        length: usize,
        name: String,
        color_model: ColorModel,
        color_type: ColorType,
    }

    impl ByteView for Block {
        fn byte_at(&self, index: usize) -> Option<u8> {
            self.block_type
                .to_bytes()
                .chain(self.length.to_be_bytes().iter().cloned())
                .chain(self.name.as_bytes().iter().cloned())
                .chain(std::iter::once(0u8))
                .chain(self.color_model.to_bytes())
                .chain(self.color_type.to_bytes())
                .skip(index)
                .next()
        }

        fn byte_size(&self) -> usize {
            self.block_type.byte_size()
                + core::mem::size_of::<u32>()
                + (self.name.as_bytes().len() + 1)
                + self.color_model.byte_size()
                + self.color_type.byte_size()
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
            blocks.into_iter().map(|block| block.byte_size()).sum()
        }
    }

    impl ByteView for AdobeSwatchExchange {
        fn byte_at(&self, index: usize) -> Option<u8> {
            AdobeSwatchExchange::FILE_SIGNATURE
                .as_bytes()
                .iter()
                .cloned()
                .chain(self.version.to_bytes())
                .chain(self.blocks.len().to_be_bytes().iter().cloned())
                .chain(self.blocks.iter().map(|block| block.to_bytes()).flatten())
                .skip(index)
                .next()
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
    use tobytes::ToBytes;

    #[test]
    fn version_as_bytes() {
        let version = Version::new(10, 1);
        let bytes: Vec<u8> = version.to_bytes().collect();
        assert_eq!(vec![0x00u8, 0x0Au8, 0x00u8, 0x01u8], bytes)
    }

    #[test]
    fn Cmyk_as_bytes() {
        // Todo: Implement
        assert!(false)
    }

    #[test]
    fn Rgb_as_bytes() {
        // Todo: Implement
        assert!(false)
    }

    #[test]
    fn Lab_as_bytes() {
        // Todo: Implement
        assert!(false)
    }

    #[test]
    fn Grey_as_bytes() {
        // Todo: Implement
        assert!(false)
    }

    #[test]
    fn ColorModel_as_bytes() {
        // Todo: Implement
        assert!(false)
    }

    #[test]
    fn ColorType_as_bytes() {
        // Todo: Implement
        assert!(false)
    }

    #[test]
    fn BlockType_as_bytes() {
        // Todo: Implement
        assert!(false)
    }

    #[test]
    fn Block_as_bytes() {
        // Todo: Implement
        assert!(false)
    }

    #[test]
    fn AdobeSwatchExchange_as_bytes() {
        // Todo: Implement
        assert!(false)
    }
}
