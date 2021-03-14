use serde::{Deserialize, Serialize};

#[derive(Serialize, Deserialize)]
pub enum ColorModel {
    Rgb { red: u8, green: u8, blue: u8 },
    Lab { l: f32, a: f32, b: f32 },
    Cmyk { c: f32, m: f32, y: f32, k: f32 },
    Grey(f32),
}

#[derive(Serialize, Deserialize)]
pub struct Color {
    name: String,
    pallet: String,
    color: ColorModel,
}

fn main() {
    {
        let c = Color {
            pallet: String::from("MyPallet"),
            name: String::from("MyColor"),
            color: ColorModel::Rgb {
                red: 255,
                green: 0,
                blue: 100,
            },
        };

        println!("{}", serde_json::to_string(&c).unwrap());
    }
    {
        let c = Color {
            pallet: String::from("MyPallet"),
            name: String::from("MyColor"),
            color: ColorModel::Cmyk {
                c: 255.0,
                m: 0.0,
                y: 110.0,
                k: 1.0,
            },
        };

        println!("{}", serde_json::to_string(&c).unwrap());
    }
    {
        let c = Color {
            pallet: String::from("MyPallet"),
            name: String::from("MyColor"),
            color: ColorModel::Lab {
                l: 255.0,
                a: 0.0,
                b: 100.0,
            },
        };

        println!("{}", serde_json::to_string(&c).unwrap());
    }
    {
        let c = Color {
            pallet: String::from("MyPallet"),
            name: String::from("MyColor"),
            color: ColorModel::Grey(10.0),
        };

        println!("{}", serde_json::to_string(&c).unwrap());
    }
}

#[cfg(test)]
mod tests {}
