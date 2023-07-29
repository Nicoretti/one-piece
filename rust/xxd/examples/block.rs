use xxd::DefaultBgColorMap;
use xxd::DefaultFgColorMap;

fn main() {
    let data = [0u8, 1u8, 2u8, 3u8, 4u8, 5u8, 6u8, 7u8];
    let fg_color_map = DefaultFgColorMap::new();
    let bg_color_map = DefaultBgColorMap::new();

    let b1 = xxd::Block::new(&data)
        .fg_colors(&fg_color_map)
        .bg_colors(&bg_color_map);
    let b2 = xxd::Block::new(&data)
        .fg_colors(&fg_color_map)
        .bg_colors(&bg_color_map);
    let b3 = xxd::Block::new(&data)
        .fg_colors(&fg_color_map)
        .bg_colors(&bg_color_map);
    let b4 = xxd::Block::new(&data)
        .fg_colors(&fg_color_map)
        .bg_colors(&bg_color_map);

    println!("Hex");
    println!("{:x}", b1);

    println!("Bin");
    println!("{:b}", b2);

    println!("Oct");
    println!("{:o}", b3);

    println!("Dez");
    println!("{}", b4);
}
