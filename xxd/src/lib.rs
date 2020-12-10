use std::ops;
pub use yansi::Color;

pub trait ColorMap: std::ops::Index<u8, Output = Color> {}
impl<T> ColorMap for T where T: std::ops::Index<u8, Output = Color> {}

pub trait Colored {
    // TODO: document
    fn foreground(&self) -> Option<Color>;

    // TODO: document
    fn background(&self) -> Option<Color>;

    fn colorize(&self, string: String) -> String {
        match (self.foreground(), self.background()) {
            (None, None) => string,
            (Some(fg), None) => format!("{}", fg.paint(string)),
            (None, Some(bg)) => {
                let style = yansi::Style::new(Color::Unset);
                format!("{}", style.bg(bg).paint(string))
            }
            (Some(fg), Some(bg)) => {
                let style = yansi::Style::new(fg);
                format!("{}", style.bg(bg).paint(string))
            }
        }
    }
}

pub struct NoColorMap {}
pub struct DefaultFgColorMap {}
pub struct DefaultBgColorMap {}

impl NoColorMap {
    const COLOR: Color = Color::Unset;
    const fn new() -> Self {
        NoColorMap {}
    }
}

impl DefaultFgColorMap {
    const COLOR_MAP: [Color; 10] = [
        Color::Red,
        Color::Magenta,
        Color::Green,
        Color::Magenta,
        Color::Cyan,
        Color::Cyan,
        Color::Magenta,
        Color::Cyan,
        Color::Magenta,
        Color::Red,
    ];

    pub const fn new() -> Self {
        DefaultFgColorMap {}
    }
}
impl DefaultBgColorMap {
    const COLOR_MAP: [Color; 10] = [
        Color::Unset,
        Color::Unset,
        Color::Unset,
        Color::Unset,
        Color::Unset,
        Color::Unset,
        Color::Unset,
        Color::Unset,
        Color::Unset,
        Color::White,
    ];

    pub const fn new() -> Self {
        DefaultBgColorMap {}
    }
}

impl std::ops::Index<u8> for NoColorMap {
    type Output = Color;
    fn index(&self, _: u8) -> &Self::Output {
        &Self::COLOR
    }
}

impl ops::Index<u8> for DefaultFgColorMap {
    type Output = Color;

    fn index(&self, index: u8) -> &Self::Output {
        &Self::COLOR_MAP[match index {
            0..=32 => 0,
            33..=47 => 1,
            48..=57 => 2,
            58..=64 => 3,
            65..=90 => 4,
            91..=96 => 5,
            97..=122 => 6,
            123..=125 => 7,
            126 => 8,
            _ => 9,
        }]
    }
}

impl ops::Index<u8> for DefaultBgColorMap {
    type Output = Color;

    fn index(&self, index: u8) -> &Self::Output {
        &Self::COLOR_MAP[match index {
            0..=32 => 0,
            33..=47 => 1,
            48..=57 => 2,
            58..=64 => 3,
            65..=90 => 4,
            91..=96 => 5,
            97..=122 => 6,
            123..=125 => 7,
            126 => 8,
            _ => 9,
        }]
    }
}

mod block;
mod blocks;
mod byte;
mod line;

pub use block::Block;
pub use blocks::Blocks;
pub use byte::Byte;
pub use byte::ByteBuilder;
pub use line::Line;
pub use line::LineIterator;
