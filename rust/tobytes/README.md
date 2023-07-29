The main goal of this crate is to simplify serialization of type's and structures to bytes.

# Why?
If one works with binary formats/protocols a lot of time is spent implementing
decoding and encoding types and structures of the format/protocol in order to further
process the contained data.

For decoding parsers generators like [nom](https://github.com/Geal/nom) are very helpful and easy the implmentation.
This create tries to provide a lightweight encoding/output conbinator by just introducing 2 new traits
which in turn then can make use of the iterator facilites to crate the desired output chain of bytes.

## Why this extra step with the trait's

1. By introducing such a trait complex (compsites) structures in a lot of cases can be implemented
   by just encoding and chaining the childs in order

2. The fileds of a type still can be used for encoding but there is no hard dependency
   on their order nor their actual size

   e.g. a protocol field size with the encoded size of 2 Bytes (u16), still can
   be represented e.g. as usize withn the structures/type which save quite some
   converting and casting.

3. There is no need of a type to provide a specific amount of memory in order
   to be serialized (the serialization of a type or a type could be 100% computational)

   e.g.: assume this protocol type/structure   (Packet)
    ```shell
    +-----------------+-------------------+-----------------+
    | field1 (1 Byte) | reserved (7 Byte) | filed2 (8 Byte) |
    +-----------------+-------------------+-----------------+
    ```

   internally it could be represented and implemented like this

   ```rust
   use tobytes::ByteView;
   use tobytes::ToBytes;

   struct Packet {
   field1: u8,
   field2: u64
   }

   impl Packet {
      const RESERVED : u8 = 0x00;
   }

   impl ByteView for Packet {


       fn byte_at(&self, index: usize) -> Option<u8> {
           if index < ByteView::byte_size(self) {
               match index {
                   0 => self.field1.byte_at(index),
                   1..=7 => Some(Packet::RESERVED),
                   8..=15 => self.field2.byte_at(index -7),
                   _ => None
               }       
           }           
           else {
              None
           }   
       }

       fn byte_size(&self) -> usize {
       ByteView::byte_size(&self.field1) + 7usize + ByteView::byte_size(&self.field2)
       }
   }

   let field1 = 0xaau8;
   let field2 = 0xaabbccddeeff11u64.to_be();
   let p = Packet {field1, field2};
   let mut bytes = p.to_bytes();

   assert_eq!(16usize, p.byte_size());

   assert_eq!(
       vec![0xaa, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0xaa, 0xbb, 0xcc, 0xdd, 0xee, 0xff, 0x11],
       bytes.collect::<Vec<u8>>()
   );
   ```

# How? (Usage)

## Example(s)

### How to serialize integers of different endianess and size

```rust
use tobytes::ByteView;
use tobytes::ToBytes;

let uint16_be : u16 = 0x0A0Bu16.to_be();
let uint16_le : u16 = 0x0C0Du16.to_le();
let uint32_le : u32 = 0x01020304u32.to_le();

let uint16_be_bytes = uint16_be.to_bytes();
let uint16_le_bytes = uint16_le.to_bytes();
let uint32_le_bytes = uint32_le.to_bytes();

let mut bytes = uint16_be_bytes.chain(uint16_le_bytes.chain(uint32_le_bytes));

assert_eq!(vec![0x0A, 0x0B, 0x0D, 0x0C, 0x04, 0x03, 0x02, 0x01], bytes.collect::<Vec<u8>>())
```

### How to serialize a custom type which contains different endinesses and types

**TBD**

### How to serialize a custom type which contains types which also implent the ByteView trait

**TBD**


# Todo's
* [x] Implement ByteView for built in integer and float types
* [ ] Implement ByteView for slice like types
* [ ] Implement derive macro for ByteView
* [ ] Make the create no_std / add no_std support
