pub mod adobe {
    use tobytes::{ByteView, ToBytes};

    #[derive(Debug, PartialEq)]
    pub struct Version {
        major: u16,
        minor: u16,
    }

    impl Version {
        pub fn new(major: u16, minor: u16) -> Self {
            Self { major, minor }
        }
    }

    impl ByteView for Version {
        fn byte_at(&self, index: usize) -> Option<u8> {
            self.major
                .to_be_bytes()
                .iter()
                .chain(self.minor.to_be_bytes().iter())
                .skip(index)
                .next()
                .cloned()
        }

        fn byte_size(&self) -> usize {
            ToBytes::to_bytes(self).count()
        }
    }

    #[derive(Debug, PartialEq, Clone)]
    pub struct Cmyk {
        cyan: f32,
        magenta: f32,
        yellow: f32,
        key: f32,
    }

    impl Cmyk {
        pub fn new(cyan: f32, magenta: f32, yellow: f32, key: f32) -> Self {
            Self {
                cyan,
                magenta,
                yellow,
                key,
            }
        }
    }

    impl ByteView for Cmyk {
        fn byte_at(&self, index: usize) -> Option<u8> {
            self.cyan
                .to_be_bytes()
                .to_owned()
                .iter()
                .chain(self.magenta.to_be_bytes().to_owned().iter())
                .chain(self.yellow.to_be_bytes().to_owned().iter())
                .chain(self.key.to_be_bytes().to_owned().iter())
                .skip(index)
                .next()
                .cloned()
        }

        fn byte_size(&self) -> usize {
            ToBytes::to_bytes(self).count()
        }
    }

    #[derive(Debug, PartialEq, Clone)]
    pub struct Rgb {
        red: f32,
        green: f32,
        blue: f32,
    }

    impl Rgb {
        pub fn new(red: f32, green: f32, blue: f32) -> Self {
            Self { red, green, blue }
        }
    }

    impl ByteView for Rgb {
        fn byte_at(&self, index: usize) -> Option<u8> {
            self.red
                .to_be_bytes()
                .to_owned()
                .iter()
                .chain(self.green.to_be_bytes().to_owned().iter())
                .chain(self.blue.to_be_bytes().to_owned().iter())
                .skip(index)
                .next()
                .cloned()
        }

        fn byte_size(&self) -> usize {
            ToBytes::to_bytes(self).count()
        }
    }

    #[derive(Debug, PartialEq, Clone)]
    pub struct Lab {
        l: f32,
        a: f32,
        b: f32,
    }

    impl Lab {
        pub fn new(l: f32, a: f32, b: f32) -> Self {
            Self { l, a, b }
        }
    }

    impl ByteView for Lab {
        fn byte_at(&self, index: usize) -> Option<u8> {
            self.l
                .to_be_bytes()
                .to_owned()
                .iter()
                .chain(self.a.to_be_bytes().to_owned().iter())
                .chain(self.b.to_be_bytes().to_owned().iter())
                .skip(index)
                .next()
                .cloned()
        }

        fn byte_size(&self) -> usize {
            ToBytes::to_bytes(self).count()
        }
    }

    #[derive(Debug, PartialEq, Clone)]
    pub struct Grey {
        grey: f32,
    }

    impl Grey {
        pub fn new(grey: f32) -> Self {
            Self { grey }
        }
    }

    impl ByteView for Grey {
        fn byte_at(&self, index: usize) -> Option<u8> {
            self.grey
                .to_be_bytes()
                .to_owned()
                .iter()
                .skip(index)
                .next()
                .cloned()
        }

        fn byte_size(&self) -> usize {
            ToBytes::to_bytes(self).count()
        }
    }

    #[derive(Debug, PartialEq, Clone)]
    pub enum ColorModel {
        CMYK(Cmyk),
        RGB(Rgb),
        LAB(Lab),
        GREY(Grey),
    }

    // TODO: consider moving the prefix information 'CMYK', 'RGB', ... into
    //       this structre and keep only the color information bit in the struct(s) Cmyk, Rgb, ..
    impl ByteView for ColorModel {
        fn byte_at(&self, index: usize) -> Option<u8> {
            match self {
                ColorModel::CMYK(cmyk) => ['C' as u8, 'M' as u8, 'Y' as u8, 'K' as u8]
                    .iter()
                    .cloned()
                    .chain(cmyk.to_bytes())
                    .skip(index)
                    .next(),
                ColorModel::RGB(rgb) => ['R' as u8, 'G' as u8, 'B' as u8, 0u8]
                    .iter()
                    .cloned()
                    .chain(rgb.to_bytes())
                    .skip(index)
                    .next(),
                ColorModel::LAB(lab) => ['L' as u8, 'A' as u8, 'B' as u8, 0u8]
                    .iter()
                    .cloned()
                    .chain(lab.to_bytes())
                    .skip(index)
                    .next(),
                ColorModel::GREY(grey) => ['G' as u8, 'R' as u8, 'E' as u8, 'Y' as u8]
                    .iter()
                    .cloned()
                    .chain(grey.to_bytes())
                    .skip(index)
                    .next(),
            }
        }

        fn byte_size(&self) -> usize {
            ToBytes::to_bytes(self).count()
        }
    }

    #[derive(Debug, PartialEq, Clone)]
    pub enum ColorType {
        Global,
        Spot,
        Normal,
    }

    impl ByteView for ColorType {
        fn byte_at(&self, index: usize) -> Option<u8> {
            match self {
                ColorType::Global => 0u16,
                ColorType::Spot => 1u16,
                ColorType::Normal => 2u16,
            }
            .to_be_bytes()
            .iter()
            .skip(index)
            .next()
            .cloned()
        }

        fn byte_size(&self) -> usize {
            ToBytes::to_bytes(self).count()
        }
    }

    #[derive(Debug, PartialEq, Clone)]
    pub enum BlockType {
        GroupStart,
        GroupEnd,
        ColorEntry,
    }

    impl ByteView for BlockType {
        fn byte_at(&self, index: usize) -> Option<u8> {
            match self {
                BlockType::GroupStart => 0xc001u16,
                BlockType::GroupEnd => 0xc002u16,
                BlockType::ColorEntry => 0x0001u16,
            }
            .to_be_bytes()
            .iter()
            .skip(index)
            .next()
            .cloned()
        }

        fn byte_size(&self) -> usize {
            ToBytes::to_bytes(self).count()
        }
    }

    #[derive(Debug, PartialEq)]
    pub struct Block {
        block_type: BlockType,
        length: u32,
        name: String,
        color_model: ColorModel,
        color_type: ColorType,
    }

    impl Block {
        pub fn new(
            block_type: BlockType,
            name: &str,
            color_model: ColorModel,
            color_type: ColorType,
        ) -> Self {
            let length = match block_type {
                BlockType::GroupStart => name.len() + 2,
                BlockType::ColorEntry => {
                    name.len() + 2 + color_model.byte_size() + color_type.byte_size()
                }
                BlockType::GroupEnd => 0,
            } as u32;
            Self {
                block_type,
                length,
                name: String::from(name),
                color_model,
                color_type,
            }
        }
    }

    impl ByteView for Block {
        fn byte_at(&self, index: usize) -> Option<u8> {
            self.block_type
                .to_bytes()
                .chain(self.length.to_be_bytes().iter().cloned())
                .chain((self.name.len() as u32).to_be_bytes().iter().cloned())
                .chain(self.name.as_bytes().iter().cloned())
                .chain(std::iter::once(0u8))
                .chain(std::iter::once(0u8))
                .chain(self.color_model.to_bytes())
                .chain(self.color_type.to_bytes())
                .skip(index)
                .next()
        }

        fn byte_size(&self) -> usize {
            ToBytes::to_bytes(self).count()
        }
    }

    /// Reference: http://www.selapa.net/swatches/colors/fileformats.php#adobe_ase
    #[derive(Debug, PartialEq)]
    pub struct AdobeSwatchExchange {
        version: Version,
        blocks: Vec<Block>,
    }

    impl AdobeSwatchExchange {
        pub fn new(version: Version, blocks: Vec<Block>) -> Self {
            Self { version, blocks }
        }
    }

    impl AdobeSwatchExchange {
        const FILE_SIGNATURE: [u8; 4] = [0x41, 0x53, 0x45, 0x46];
    }

    impl ByteView for AdobeSwatchExchange {
        fn byte_at(&self, index: usize) -> Option<u8> {
            AdobeSwatchExchange::FILE_SIGNATURE
                .iter()
                .cloned()
                .chain(self.version.to_bytes())
                .chain((self.blocks.len() as u32).to_be_bytes().iter().cloned())
                .chain(self.blocks.iter().map(|block| block.to_bytes()).flatten())
                .skip(index)
                .next()
        }

        fn byte_size(&self) -> usize {
            ToBytes::to_bytes(self).count()
        }
    }
}

#[cfg(test)]
mod tests {

    use super::adobe::Version;
    use crate::adobe::Rgb;
    use crate::adobe::{AdobeSwatchExchange, Block};
    use crate::adobe::{BlockType, Lab};
    use crate::adobe::{Cmyk, ColorModel};
    use crate::adobe::{ColorType, Grey};
    use tobytes::ToBytes;

    #[test]
    fn version_as_bytes() {
        let version = Version::new(10, 1);
        let bytes: Vec<u8> = version.to_bytes().collect();
        assert_eq!(vec![0x00u8, 0x0Au8, 0x00u8, 0x01u8], bytes)
    }

    #[test]
    fn cmyk_as_bytes() {
        let c: f32 = 100.0;
        let m: f32 = 200.0;
        let y: f32 = 300.0;
        let k: f32 = 10.0;
        let mut expected: Vec<u8> = vec![];
        expected.extend(c.to_be_bytes().iter());
        expected.extend(m.to_be_bytes().iter());
        expected.extend(y.to_be_bytes().iter());
        expected.extend(k.to_be_bytes().iter());

        let cmyk = Cmyk::new(c, m, y, k);
        let bytes: Vec<u8> = cmyk.to_bytes().collect();

        assert_eq!(expected, bytes)
    }

    #[test]
    fn rgb_as_bytes() {
        let r: f32 = 100.0;
        let g: f32 = 200.0;
        let b: f32 = 240.0;
        let mut expected: Vec<u8> = vec![];
        expected.extend(r.to_be_bytes().iter());
        expected.extend(g.to_be_bytes().iter());
        expected.extend(b.to_be_bytes().iter());

        let rgb = Rgb::new(r, g, b);
        let bytes: Vec<u8> = rgb.to_bytes().collect();

        assert_eq!(expected, bytes)
    }

    #[test]
    fn lab_as_bytes() {
        let l: f32 = 100.0;
        let a: f32 = 200.0;
        let b: f32 = 240.0;
        let mut expected: Vec<u8> = vec![];
        expected.extend(l.to_be_bytes().iter());
        expected.extend(a.to_be_bytes().iter());
        expected.extend(b.to_be_bytes().iter());

        let lab = Lab::new(l, a, b);
        let bytes: Vec<u8> = lab.to_bytes().collect();

        assert_eq!(expected, bytes)
    }

    #[test]
    fn grey_as_bytes() {
        let g: f32 = 100.0;
        let mut expected: Vec<u8> = vec![];
        expected.extend(g.to_be_bytes().iter());

        let grey = Grey::new(g);
        let bytes: Vec<u8> = grey.to_bytes().collect();

        assert_eq!(expected, bytes)
    }

    #[test]
    fn colormodel_as_bytes() {
        {
            let c: f32 = 100.0;
            let m: f32 = 200.0;
            let y: f32 = 300.0;
            let k: f32 = 10.0;
            let mut expected: Vec<u8> = vec!['C' as u8, 'M' as u8, 'Y' as u8, 'K' as u8];
            expected.extend(c.to_be_bytes().iter());
            expected.extend(m.to_be_bytes().iter());
            expected.extend(y.to_be_bytes().iter());
            expected.extend(k.to_be_bytes().iter());

            let cmyk = ColorModel::CMYK(Cmyk::new(c, m, y, k));
            let bytes: Vec<u8> = cmyk.to_bytes().collect();

            assert_eq!(expected, bytes)
        }
        {
            let r: f32 = 100.0;
            let g: f32 = 200.0;
            let b: f32 = 240.0;
            let mut expected: Vec<u8> = vec!['R' as u8, 'G' as u8, 'B' as u8, 0x00];
            expected.extend(r.to_be_bytes().iter());
            expected.extend(g.to_be_bytes().iter());
            expected.extend(b.to_be_bytes().iter());

            let rgb = ColorModel::RGB(Rgb::new(r, g, b));
            let bytes: Vec<u8> = rgb.to_bytes().collect();

            assert_eq!(expected, bytes)
        }
        {
            let l: f32 = 100.0;
            let a: f32 = 200.0;
            let b: f32 = 240.0;
            let mut expected: Vec<u8> = vec!['L' as u8, 'A' as u8, 'B' as u8, 0x00];
            expected.extend(l.to_be_bytes().iter());
            expected.extend(a.to_be_bytes().iter());
            expected.extend(b.to_be_bytes().iter());

            let lab = ColorModel::LAB(Lab::new(l, a, b));
            let bytes: Vec<u8> = lab.to_bytes().collect();

            assert_eq!(expected, bytes)
        }
        {
            let g: f32 = 100.0;
            let mut expected: Vec<u8> = vec!['G' as u8, 'R' as u8, 'E' as u8, 'Y' as u8];
            expected.extend(g.to_be_bytes().iter());

            let grey = ColorModel::GREY(Grey::new(g));
            let bytes: Vec<u8> = grey.to_bytes().collect();

            assert_eq!(expected, bytes)
        }
    }

    #[test]
    fn colortype_as_bytes() {
        {
            let expected: Vec<u8> = vec![0x00, 0x00];
            let c_type = ColorType::Global;
            let bytes: Vec<u8> = c_type.to_bytes().collect();
            assert_eq!(expected, bytes)
        }
        {
            let expected: Vec<u8> = vec![0x00, 0x01];
            let c_type = ColorType::Spot;
            let bytes: Vec<u8> = c_type.to_bytes().collect();
            assert_eq!(expected, bytes)
        }
        {
            let expected: Vec<u8> = vec![0x00, 0x02];
            let c_type = ColorType::Normal;
            let bytes: Vec<u8> = c_type.to_bytes().collect();
            assert_eq!(expected, bytes)
        }
    }

    #[test]
    fn blocktype_as_bytes() {
        {
            let expected: Vec<u8> = vec![0xc0, 0x01];
            let b_type = BlockType::GroupStart;
            let bytes: Vec<u8> = b_type.to_bytes().collect();
            assert_eq!(expected, bytes)
        }
        {
            let expected: Vec<u8> = vec![0xc0, 0x02];
            let b_type = BlockType::GroupEnd;
            let bytes: Vec<u8> = b_type.to_bytes().collect();
            assert_eq!(expected, bytes)
        }
        {
            let expected: Vec<u8> = vec![0x00, 0x01];
            let b_type = BlockType::ColorEntry;
            let bytes: Vec<u8> = b_type.to_bytes().collect();
            assert_eq!(expected, bytes)
        }
    }

    #[test]
    fn block_as_bytes() {
        let block_type = BlockType::ColorEntry;
        let name = "myname";
        let color_model = ColorModel::GREY(Grey::new(10.0));
        let color_type = ColorType::Normal;
        let length = (name.len() + 2 + 8 + 2) as u32;

        let mut expected: Vec<u8> = vec![];
        expected.extend(
            block_type.to_bytes().chain(
                length
                    .to_be_bytes()
                    .iter()
                    .cloned()
                    .chain((name.len() as u32).to_be_bytes().iter().cloned())
                    .chain(name.as_bytes().iter().cloned())
                    .chain(std::iter::once(0u8))
                    .chain(std::iter::once(0u8))
                    .chain(color_model.to_bytes())
                    .chain(color_type.to_bytes()),
            ),
        );
        let block = Block::new(block_type, name, color_model, color_type);

        let bytes: Vec<u8> = block.to_bytes().collect();
        assert_eq!(expected, bytes)
    }

    #[test]
    fn adobeswatchexchange_as_bytes() {
        let version = Version::new(1, 0);
        let block_type = BlockType::ColorEntry;
        let name = "myname";
        let color_model = ColorModel::GREY(Grey::new(10.0));
        let color_type = ColorType::Normal;
        let block = Block::new(
            block_type.clone(),
            name,
            color_model.clone(),
            color_type.clone(),
        );
        let blocks = vec![Block::new(block_type, name, color_model, color_type)];
        let ase = AdobeSwatchExchange::new(Version::new(1, 0), blocks);

        let mut expected: Vec<u8> = vec![];
        expected.extend(
            [0x41u8, 0x53u8, 0x45u8, 0x46u8]
                .iter()
                .cloned()
                .chain(version.to_bytes())
                .chain((1u32).to_be_bytes().iter().cloned())
                .chain(block.to_bytes()),
        );

        let bytes: Vec<u8> = ase.to_bytes().collect();
        assert_eq!(expected, bytes)
    }
}
