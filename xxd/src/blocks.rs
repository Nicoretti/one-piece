use crate::ColorMap;
use crate::{Block, NoColorMap};
use std::fmt;

pub struct Blocks<'a> {
    bytes: Vec<u8>,
    block_size: usize,
    fg_map: &'a dyn ColorMap,
    bg_map: &'a dyn ColorMap,
}

impl<'a> Blocks<'a> {
    const COLOR_MAP: NoColorMap = NoColorMap::new();
    pub fn new(bytes: &[u8], block_size: usize) -> Self {
        let mut b = Vec::new();
        b.extend_from_slice(bytes);
        Blocks {
            bytes: b,
            block_size,
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

    pub fn interpretation(&self) -> String {
        let mut s = String::with_capacity(self.bytes.len());
        s.extend(self.bytes.iter().map(|b| match *b {
            b @ 20u8..=126u8 => b as char,
            _ => '.',
        }));
        s
    }
}

impl<'a> fmt::Display for Blocks<'a> {
    fn fmt(&self, f: &mut fmt::Formatter) -> fmt::Result {
        self.bytes
            .as_slice()
            .chunks(self.block_size)
            .try_for_each(|chunk| {
                write!(
                    f,
                    "{} ",
                    Block::new(chunk)
                        .fg_colors(self.fg_map)
                        .bg_colors(self.bg_map)
                )
            })?;
        Ok(())
    }
}

impl<'a> fmt::Binary for Blocks<'a> {
    fn fmt(&self, f: &mut fmt::Formatter) -> fmt::Result {
        self.bytes
            .as_slice()
            .chunks(self.block_size)
            .try_for_each(|chunk| {
                write!(
                    f,
                    "{:b} ",
                    Block::new(chunk)
                        .fg_colors(self.fg_map)
                        .bg_colors(self.bg_map)
                )
            })?;
        Ok(())
    }
}

impl<'a> fmt::Octal for Blocks<'a> {
    fn fmt(&self, f: &mut fmt::Formatter) -> fmt::Result {
        self.bytes
            .as_slice()
            .chunks(self.block_size)
            .try_for_each(|chunk| {
                write!(
                    f,
                    "{:o} ",
                    Block::new(chunk)
                        .fg_colors(self.fg_map)
                        .bg_colors(self.bg_map)
                )
            })?;
        Ok(())
    }
}

impl<'a> fmt::LowerHex for Blocks<'a> {
    fn fmt(&self, f: &mut fmt::Formatter) -> fmt::Result {
        self.bytes
            .as_slice()
            .chunks(self.block_size)
            .try_for_each(|chunk| {
                write!(
                    f,
                    "{:x} ",
                    Block::new(chunk)
                        .fg_colors(self.fg_map)
                        .bg_colors(self.bg_map)
                )
            })?;
        Ok(())
    }
}

impl<'a> fmt::UpperHex for Blocks<'a> {
    fn fmt(&self, f: &mut fmt::Formatter) -> fmt::Result {
        self.bytes
            .as_slice()
            .chunks(self.block_size)
            .try_for_each(|chunk| {
                write!(
                    f,
                    "{:X} ",
                    Block::new(chunk)
                        .fg_colors(self.fg_map)
                        .bg_colors(self.bg_map)
                )
            })?;
        Ok(())
    }
}
