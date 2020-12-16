use crate::byte::{Byte, ByteBuilder};
use crate::{ColorMap, NoColorMap};
use std::fmt;

pub struct Block<'a> {
    bytes: &'a [u8],
    fg_map: &'a dyn ColorMap,
    bg_map: &'a dyn ColorMap,
}

struct BlockIterator<'a> {
    block: &'a Block<'a>,
    pos: usize,
}

impl<'a> Iterator for BlockIterator<'a> {
    type Item = Byte;
    fn next(&mut self) -> Option<Self::Item> {
        let item = self.block.bytes.get(self.pos);
        match item {
            Some(byte) => {
                self.pos += 1;
                Some(Into::<Byte>::into(ByteBuilder::new(
                    *byte,
                    self.block.fg_map,
                    self.block.bg_map,
                )))
            }
            None => None,
        }
    }
}

impl<'a> Block<'a> {
    const COLOR_MAP: NoColorMap = NoColorMap::new();

    pub fn new(bytes: &'a [u8]) -> Self {
        Block {
            bytes,
            fg_map: &Self::COLOR_MAP,
            bg_map: &Self::COLOR_MAP,
        }
    }
    pub fn fg_colors(mut self, color_map: &'a dyn ColorMap) -> Self {
        self.fg_map = color_map;
        self
    }

    pub fn bg_colors(mut self, color_map: &'a dyn ColorMap) -> Self {
        self.bg_map = color_map;
        self
    }
}

impl<'a> fmt::LowerHex for Block<'a> {
    fn fmt(&self, f: &mut fmt::Formatter) -> fmt::Result {
        let mut it = BlockIterator {
            block: self,
            pos: 0,
        };
        it.try_for_each(|byte| write!(f, "{:x}", byte))?;
        Ok(())
    }
}

impl<'a> fmt::UpperHex for Block<'a> {
    fn fmt(&self, f: &mut fmt::Formatter) -> fmt::Result {
        let mut it = BlockIterator {
            block: self,
            pos: 0,
        };
        it.try_for_each(|byte| write!(f, "{:X}", byte))?;
        Ok(())
    }
}

impl<'a> fmt::Display for Block<'a> {
    fn fmt(&self, f: &mut fmt::Formatter) -> fmt::Result {
        let mut it = BlockIterator {
            block: self,
            pos: 0,
        };
        it.try_for_each(|byte| write!(f, "{}", byte))?;
        Ok(())
    }
}

impl<'a> fmt::Binary for Block<'a> {
    fn fmt(&self, f: &mut fmt::Formatter) -> fmt::Result {
        let mut it = BlockIterator {
            block: self,
            pos: 0,
        };
        it.try_for_each(|byte| write!(f, "{:b}", byte))?;
        Ok(())
    }
}

impl<'a> fmt::Octal for Block<'a> {
    fn fmt(&self, f: &mut fmt::Formatter) -> fmt::Result {
        let mut it = BlockIterator {
            block: self,
            pos: 0,
        };
        it.try_for_each(|byte| write!(f, "{:o}", byte))?;
        Ok(())
    }
}

#[cfg(test)]
mod tests {

}
