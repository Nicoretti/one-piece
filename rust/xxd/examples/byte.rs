use xxd::DefaultBgColorMap;
use xxd::DefaultFgColorMap;

fn main() {
    let values: [u8; 10] = [0, 33, 48, 58, 65, 91, 97, 123, 126, 128];
    let fg_color_map = DefaultFgColorMap::new();
    let bg_color_map = DefaultBgColorMap::new();

    println!("Hex  Bin        Oct   Dez");
    for i in values.iter() {
        let byte: xxd::Byte = xxd::ByteBuilder::new(*i, &fg_color_map, &bg_color_map).into();
        println!("{:x}   {:b}   {:o}   {}", byte, byte, byte, byte)
    }
}
