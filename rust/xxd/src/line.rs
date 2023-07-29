use crate::blocks::Blocks;
use crate::{ColorMap, DefaultBgColorMap, DefaultFgColorMap};
use std::fmt;
use std::io::Read;
use yansi::{Color, Style};

pub struct Line<'a> {
    address: usize,
    blocks: Blocks<'a>,
}

impl<'a> Line<'a> {
    pub fn new(address: usize, blocks: Blocks<'a>) -> Self {
        Line { address, blocks }
    }
}

pub struct LineIterator<'a, R: Read> {
    bytes: std::io::Bytes<R>,
    offset: usize,
    columns: usize,
    block_size: usize,
    fg_map: &'a dyn ColorMap,
    bg_map: &'a dyn ColorMap,
}

impl<'a, R: Read> LineIterator<'a, R> {
    const FG_COLOR_MAP: DefaultFgColorMap = DefaultFgColorMap::new();
    const BG_COLOR_MAP: DefaultBgColorMap = DefaultBgColorMap::new();

    pub fn new(read: R) -> Self {
        LineIterator {
            bytes: read.bytes(),
            offset: 0,
            columns: 16,
            block_size: 1,
            fg_map: &Self::FG_COLOR_MAP,
            bg_map: &Self::BG_COLOR_MAP,
        }
    }
}

impl<'a, R: Read> Iterator for LineIterator<'a, R> {
    type Item = Line<'a>;
    fn next(&mut self) -> Option<Self::Item> {
        let mut v: Vec<u8> = Vec::new();
        for _ in 1..(self.columns * self.block_size) {
            match self.bytes.next() {
                Some(Ok(byte)) => v.push(byte),
                None => break,
                _ => return None,
            }
        }
        if v.is_empty() {
            return None;
        }

        let address = self.offset;
        self.offset += self.columns * self.block_size;
        Some(Line::new(
            address,
            Blocks::new(&v, self.block_size)
                .fg_colors(self.fg_map)
                .bg_colors(self.bg_map),
        ))
    }
}

impl<'a> fmt::Display for Line<'a> {
    fn fmt(&self, f: &mut fmt::Formatter) -> fmt::Result {
        write!(
            f,
            "{}",
            Style::new(Color::White).paint(format!("{:08x}: ", self.address))
        )?;
        write!(f, "{:x} ", self.blocks)?;
        write!(f, "{}", self.blocks.interpretation())?;
        Ok(())
    }
}
