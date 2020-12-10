//! The main goal of this crate is to simplify serialization of type's and structures to bytes.
//!
//! # Why?
//! If one works with binary formats/protocols a lot of time is spent implementing
//! decoding and encoding types and structures of the format/protocol in order to further
//! process the contained data.
//!
//! For decoding parsers generators like [nom](https://github.com/Geal/nom) are very helpful and easy the implmentation.
//! This create tries to provide a lightweight encoding/output conbinator by just introducing 2 new traits
//! which in turn then can make use of the iterator facilites to crate the desired output chain of bytes.
//!
//! ## Why this extra step with the trait's
//!
//! 1. By introducing such a trait complex (compsites) structures in a lot of cases can be implemented
//!    by just encoding and chaining the childs in order
//!
//! 2. The fileds of a type still can be used for encoding but there is no hard dependency
//!    on their order nor their actual size
//!
//!    e.g. a protocol field size with the encoded size of 2 Bytes (u16), still can
//!    be represented e.g. as usize withn the structures/type which save quite some
//!    converting and casting.
//!
//! 3. There is no need of a type to provide a specific amount of memory in order
//!    to be serialized (the serialization of a type or a type could be 100% computational)
//!
//!    e.g.: assume this protocol type/structure   (Packet)
//!     ```shell
//!     +-----------------+-------------------+-----------------+
//!     | field1 (1 Byte) | reserved (7 Byte) | filed2 (8 Byte) |
//!     +-----------------+-------------------+-----------------+
//!     ```
//!
//!    internally it could be represented and implemented like this
//!
//!    ```rust
//!    use tobytes::ByteView;
//!    use tobytes::ToBytes;
//!
//!    struct Packet {
//!    field1: u8,
//!    field2: u64
//!    }
//!
//!    impl Packet {
//!       const RESERVED : u8 = 0x00;
//!    }
//!
//!    impl ByteView for Packet {
//!
//!
//!        fn byte_at(&self, index: usize) -> Option<u8> {
//!            if index < ByteView::byte_size(self) {
//!                match index {
//!                    0 => self.field1.byte_at(index),
//!                    1..=7 => Some(Packet::RESERVED),
//!                    8..=15 => self.field2.byte_at(index -7),
//!                    _ => None
//!                }       
//!            }           
//!            else {
//!               None
//!            }   
//!        }
//!
//!        fn byte_size(&self) -> usize {
//!        ByteView::byte_size(&self.field1) + 7usize + ByteView::byte_size(&self.field2)
//!        }
//!    }
//!
//!    let field1 = 0xaau8;
//!    let field2 = 0xaabbccddeeff11u64.to_be();
//!    let p = Packet {field1, field2};
//!    let mut bytes = p.to_bytes();
//!
//!    assert_eq!(16usize, p.byte_size());
//!
//!    assert_eq!(
//!        vec![0xaa, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0xaa, 0xbb, 0xcc, 0xdd, 0xee, 0xff, 0x11],
//!        bytes.collect::<Vec<u8>>()
//!    );
//!    ```
//!
//! # How? (Usage)
//!
//! ## Example(s)
//!
//! ### How to serialize integers of different endianess and size
//!
//! ```rust
//! use tobytes::ByteView;
//! use tobytes::ToBytes;
//!
//! let uint16_be : u16 = 0x0A0Bu16.to_be();
//! let uint16_le : u16 = 0x0C0Du16.to_le();
//! let uint32_le : u32 = 0x01020304u32.to_le();
//!
//! let uint16_be_bytes = uint16_be.to_bytes();
//! let uint16_le_bytes = uint16_le.to_bytes();
//! let uint32_le_bytes = uint32_le.to_bytes();
//!
//! let mut bytes = uint16_be_bytes.chain(uint16_le_bytes.chain(uint32_le_bytes));
//!
//! assert_eq!(vec![0x0A, 0x0B, 0x0D, 0x0C, 0x04, 0x03, 0x02, 0x01], bytes.collect::<Vec<u8>>())
//! ```
//!
//! ### How to serialize a custom type which contains different endinesses and types
//!
//! **TBD**
//!
//! ### How to serialize a custom type which contains types which also implent the ByteView trait
//!
//! **TBD**

/// The ByteView trait allows a type to provide a continues byte view of itself.
/// # Example(s)
/// ```rust
/// use tobytes::ByteView;
/// use tobytes::ToBytes;
/// use std::fmt::Pointer;
/// use std::marker::Sized;
///
/// struct Foo {
///     field1: u8,
///     field2: u16,
/// }
///
/// impl ByteView for Foo {
///     fn byte_at(&self, index: usize) -> Option<u8> {
///         if index < ByteView::byte_size(self) {
///             match index {
///                 0 => self.field1.byte_at(index),
///                 1..=2 => self.field2.byte_at(index -1),
///                 _ => None
///             }       
///         }           
///         else {
///            None
///         }   
///     }
///
///     fn byte_size(&self) -> usize {
///         ByteView::byte_size(&self.field1) + ByteView::byte_size(&self.field2)
///     }
/// }
///
/// let foo = Foo {field1: 0xFF, field2: 0xAABBu16.to_be()};
/// let bytes = foo.to_bytes().collect::<Vec<u8>>();
///
/// assert_eq!(3, foo.byte_size());
/// assert_eq!(vec![0xFF, 0xAA, 0xBB], bytes);
/// ```
pub trait ByteView {
    /// Get the byte at a specific index/location, if the index is out of bounce None should be returned.
    fn byte_at(&self, index: usize) -> Option<u8>;

    /// Gets the size of the type when represented as ByteView.
    /// For indexes `0..bytes_size` the ByteView needs to yield a valid byte `Some(byte)`.
    fn byte_size(&self) -> usize;
}

/// Implements an iterator over the bytes of a ByteView.
pub struct Bytes<'a, T: ByteView> {
    pos: usize,
    view: &'a T,
}

impl<'a, T: ByteView> Bytes<'a, T> {
    pub fn new(view: &'a T) -> Self {
        Bytes { pos: 0, view }
    }
}

impl<'a, T: ByteView> Iterator for Bytes<'a, T> {
    type Item = u8;

    fn next(&mut self) -> Option<Self::Item> {
        let value = self.view.byte_at(self.pos);
        self.pos += 1;
        value
    }
}

/// Trait which converts a Sized type which is implementing the ByteView trait into a Bytes object.
pub trait ToBytes<T: ByteView + Sized = Self> {
    /// If T implements [ByteView](trait.ByteView.html) trait and it is [Sized](trait.Sized.html)
    /// then the default implementation is sufficient for T.
    fn to_bytes(&self) -> Bytes<T>;
}

impl<'a, T: Sized + ByteView> ToBytes for T {
    fn to_bytes(&self) -> Bytes<T> {
        Bytes::new(&self)
    }
}

/// Implements the [ByteView](trait.ByteView.html) trait for types which provide a `to_ne_bytes` method.
/// (for more details on `to_ne_bytes` check e.g. `U8, U16, U32, ...`.
macro_rules! implement_byte_view_for {
    ($t:ty) => {
        impl ByteView for $t {
            fn byte_at(&self, index: usize) -> Option<u8> {
                if index < ByteView::byte_size(self) {
                    Some(self.to_ne_bytes()[index])
                } else {
                    None
                }
            }

            fn byte_size(&self) -> usize {
                core::mem::size_of::<Self>()
            }
        }
    };
}

implement_byte_view_for!(u8);
implement_byte_view_for!(i8);
implement_byte_view_for!(u16);
implement_byte_view_for!(i16);
implement_byte_view_for!(u32);
implement_byte_view_for!(i32);
implement_byte_view_for!(u64);
implement_byte_view_for!(i64);
implement_byte_view_for!(u128);
implement_byte_view_for!(i128);
implement_byte_view_for!(f32);
implement_byte_view_for!(f64);

// TODO: add implement macro or impl. for types which can be converted into a slice of bytes

// TODO's: Implement ByteView for
// * [u8; T]
// * Vec<u8>
// * &[u8]
// ...

// TODO: Implement Derive Macro if all members implement ByteView

// Add test for all supported built in types

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn u8_to_bytes() {
        let value: u8 = 0xAA;
        assert_eq!(vec![0xAAu8], value.to_bytes().collect::<Vec<u8>>());
    }

    #[test]
    fn i8_to_bytes() {
        let value: i8 = -1;
        assert_eq!(vec![0xFF], value.to_bytes().collect::<Vec<u8>>());
    }

    #[test]
    fn u16_to_bytes() {
        let value: u16 = 0xAABBu16;
        let value_be: u16 = value.to_be();
        let value_le: u16 = value.to_le();
        assert_eq!(
            vec![0xAAu8, 0xBBu8],
            value_be.to_bytes().collect::<Vec<u8>>()
        );
        assert_eq!(
            vec![0xBBu8, 0xAAu8],
            value_le.to_bytes().collect::<Vec<u8>>()
        );
    }

    #[test]
    fn i16_to_bytes() {
        let value = 0x0A0Bi16;
        let value_be: i16 = value.to_be();
        let value_le: i16 = value.to_le();
        assert_eq!(
            vec![0x0Au8, 0x0Bu8],
            value_be.to_bytes().collect::<Vec<u8>>()
        );
        assert_eq!(
            vec![0x0Bu8, 0x0Au8],
            value_le.to_bytes().collect::<Vec<u8>>()
        );
    }

    #[test]
    fn u32_to_bytes() {
        let value: u32 = 0xAABBCCDD;
        let value_be: u32 = value.to_be();
        let value_le: u32 = value.to_le();
        assert_eq!(
            vec![0xAAu8, 0xBBu8, 0xCCu8, 0xDDu8],
            value_be.to_bytes().collect::<Vec<u8>>()
        );
        assert_eq!(
            vec![0xDDu8, 0xCCu8, 0xBBu8, 0xAAu8],
            value_le.to_bytes().collect::<Vec<u8>>()
        );
    }

    #[test]
    fn i32_to_bytes() {
        let value: i32 = 0x0A0B0C0D;
        let value_be: i32 = value.to_be();
        let value_le: i32 = value.to_le();
        assert_eq!(
            vec![0x0Au8, 0x0Bu8, 0x0Cu8, 0x0Du8],
            value_be.to_bytes().collect::<Vec<u8>>()
        );
        assert_eq!(
            vec![0x0Du8, 0x0Cu8, 0x0Bu8, 0x0Au8],
            value_le.to_bytes().collect::<Vec<u8>>()
        );
    }

    #[test]
    fn chain_bytes() {
        let value1: u8 = 0xAA;
        let value2: u16 = 0xAABBu16.to_be();
        let value3: u32 = 0xAABBCCDDu32.to_be();
        assert_eq!(
            vec![0xAAu8, 0xAAu8, 0xBBu8, 0xAAu8, 0xBBu8, 0xCCu8, 0xDDu8],
            value1
                .to_bytes()
                .chain(value2.to_bytes().chain(value3.to_bytes()))
                .collect::<Vec<u8>>()
        );
    }
}
