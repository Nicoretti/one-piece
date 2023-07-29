use crate::{ColorMap, Colored, NoColorMap};
use std::convert::From;
use std::fmt;
use yansi::Color;

pub struct Byte {
    byte: u8,
    fg_color: Option<Color>,
    bg_color: Option<Color>,
}

impl Byte {
    const COLOR_MAP: NoColorMap = NoColorMap::new();

    pub fn build<'a>(byte: u8) -> ByteBuilder<'a> {
        ByteBuilder::new(byte, &Self::COLOR_MAP, &Self::COLOR_MAP)
    }
}

impl crate::Colored for Byte {
    fn foreground(&self) -> Option<Color> {
        self.fg_color
    }

    fn background(&self) -> Option<Color> {
        self.bg_color
    }
}

impl fmt::Binary for Byte {
    fn fmt(&self, f: &mut fmt::Formatter) -> fmt::Result {
        write!(f, "{}", self.colorize(format!("{:08.b}", self.byte)))?;
        Ok(())
    }
}

impl fmt::Octal for Byte {
    fn fmt(&self, f: &mut fmt::Formatter) -> fmt::Result {
        write!(f, "{}", self.colorize(format!("{:03.o}", self.byte)))?;
        Ok(())
    }
}

impl fmt::LowerHex for Byte {
    fn fmt(&self, f: &mut fmt::Formatter) -> fmt::Result {
        write!(f, "{}", self.colorize(format!("{:02.x}", self.byte)))?;
        Ok(())
    }
}

impl fmt::UpperHex for Byte {
    fn fmt(&self, f: &mut fmt::Formatter) -> fmt::Result {
        write!(f, "{}", self.colorize(format!("{:02.X}", self.byte)))?;
        Ok(())
    }
}

impl fmt::Display for Byte {
    fn fmt(&self, f: &mut fmt::Formatter) -> fmt::Result {
        write!(f, "{}", self.colorize(format!("{:03}", self.byte)))?;
        Ok(())
    }
}

pub struct ByteBuilder<'a> {
    byte: u8,
    fg_map: &'a dyn ColorMap,
    bg_map: &'a dyn ColorMap,
}

impl<'a> ByteBuilder<'a> {
    pub fn new(byte: u8, fg_map: &'a dyn ColorMap, bg_map: &'a dyn ColorMap) -> Self {
        ByteBuilder {
            byte,
            fg_map,
            bg_map,
        }
    }
}

impl<'a> From<ByteBuilder<'a>> for Byte {
    fn from(builder: ByteBuilder<'a>) -> Self {
        Byte {
            byte: builder.byte,
            fg_color: Some(builder.fg_map[builder.byte]),
            bg_color: Some(builder.bg_map[builder.byte]),
        }
    }
}

#[cfg(test)]
mod tests {

    use super::Byte;

    #[test]
    fn test_byte_fmt_lower_hex() {
        let expected = "0a";
        let byte = Byte {
            byte: 0x0A,
            fg_color: None,
            bg_color: None,
        };
        assert_eq!(expected, format!("{:x}", byte));
    }
    #[test]
    fn test_byte_fmt_binary() {
        let expected = "00001010";
        let byte = Byte {
            byte: 0x0A,
            fg_color: None,
            bg_color: None,
        };
        assert_eq!(expected, format!("{:b}", byte));
    }
    #[test]
    fn test_byte_fmt_octal() {
        let expected = "012";
        let byte = Byte {
            byte: 0x0A,
            fg_color: None,
            bg_color: None,
        };
        assert_eq!(expected, format!("{:o}", byte));
    }
    #[test]
    fn test_byte_fmt_upper_hex() {
        let expected = "0A";
        let byte = Byte {
            byte: 0x0A,
            fg_color: None,
            bg_color: None,
        };
        assert_eq!(expected, format!("{:X}", byte));
    }
    #[test]
    fn test_byte_fmt_decimal() {
        let expected = "010";
        let byte = Byte {
            byte: 0x0A,
            fg_color: None,
            bg_color: None,
        };
        assert_eq!(expected, format!("{}", byte));
    }
}
