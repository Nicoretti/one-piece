use xxd;

fn main() {
    let mut v: Vec<u8> = Vec::new();
    for i in 0..255 {
        v.push(i as u8);
    }
    let data = std::io::Cursor::new(v);
    let it = xxd::LineIterator::new(data);

    for l in it {
        println!("{}", l);
    }
}
