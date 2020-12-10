/// Contains structures to parse [Synalyze It](https://www.synalysis.net)/[Hexinator](https://hexinator.com) grammar files.
pub mod grammar {
    use serde::{Deserialize, Serialize};

    #[derive(Debug, Serialize, Deserialize, PartialEq)]
    pub struct Ufwb {
        version: std::string::String,
        grammar: Grammar,
    }

    #[derive(Debug, Serialize, Deserialize, PartialEq)]
    pub struct Grammar {
        name: std::string::String,
        start: std::string::String,
        author: std::string::String,
        email: Option<std::string::String>,
        complete: std::string::String,
        structure: RootStructure,
        description: std::string::String,
    }

    #[derive(Debug, Serialize, Deserialize, PartialEq)]
    #[serde(rename = "structure")]
    pub struct RootStructure {
        name: std::string::String,
        id: usize,
        encoding: std::string::String,
        endian: Endianess,
        signed: Signedness,
        #[serde(rename(deserialize = "$value"))]
        items: Option<Vec<StructureElement>>,
    }

    #[derive(Debug, Serialize, Deserialize, PartialEq)]
    pub struct Structure {
        name: std::string::String,
        id: usize,
        encoding: Option<std::string::String>,
        endian: Option<Endianess>,
        signed: Option<Signedness>,
        #[serde(rename(deserialize = "$value"))]
        items: Option<Vec<StructureElement>>,
    }

    #[derive(Debug, Serialize, Deserialize, PartialEq)]
    #[serde(rename_all = "lowercase")]
    pub enum StructureElement {
        Number(Number),
        String(String),
        Structure(Structure),
    }

    #[derive(Debug, Serialize, Deserialize, PartialEq)]
    pub struct String {
        name: std::string::String,
        id: usize,
        length: Option<usize>,
        r#type: StringType,
        delimiter: Option<std::string::String>,
    }

    #[derive(Debug, Serialize, Deserialize, PartialEq)]
    pub enum StringType {
        #[serde(rename = "fixed-length")]
        FixedLength,
        #[serde(rename = "zero-terminated")]
        ZeroTerminated,
        #[serde(rename = "delimiter-terminated")]
        DelimiterTerminated,
        #[serde(rename = "pascal")]
        PrefixedLength,
    }

    #[derive(Debug, Serialize, Deserialize, PartialEq)]
    pub enum NumberType {
        #[serde(rename = "float")]
        Float,
        #[serde(rename = "integer")]
        Integer,
    }

    #[derive(Debug, Serialize, Deserialize, PartialEq)]
    pub enum Unit {
        #[serde(rename = "bit")]
        Bit,
        #[serde(rename = "byte")]
        Byte,
    }

    #[derive(Debug, Serialize, Deserialize, PartialEq)]
    pub struct Number {
        name: std::string::String,
        id: usize,
        #[serde(rename = "type")]
        r#type: NumberType,
        length: usize,
        #[serde(rename = "lengthunit")]
        unit: Option<Unit>,
    }

    #[derive(Debug, Serialize, Deserialize, PartialEq)]
    #[serde(rename_all = "lowercase")]
    pub enum Endianess {
        Big,
        Little,
    }

    #[derive(Debug, Serialize, Deserialize, PartialEq)]
    #[serde(rename_all = "lowercase")]
    pub enum Signedness {
        #[serde(rename = "yes")]
        Signed,
        #[serde(rename = "no")]
        Unsigned,
    }

    #[cfg(test)]
    mod tests {
        use super::*;
        use quick_xml::de::{from_str, DeError};
        use crate::synalize::grammar::{Grammar, Endianess, Signedness};

        #[test]
        fn test_structure() -> Result<(), DeError> {
            let expected = RootStructure {
                name: std::string::String::from("struct1"),
                id: 1,
                encoding: std::string::String::from("ISO_8859-1:1987"),
                endian: Endianess::Big,
                signed: Signedness::Unsigned,
                items: None,
            };
            let xml = r#"
            <?xml version="1.0" encoding="UTF-8"?>
            <structure name="struct1" id="1" encoding="ISO_8859-1:1987" endian="big" signed="no"/>
            "#;
            let structrue: RootStructure = from_str(xml)?;
            assert_eq!(expected, structrue);
            Ok(())
        }

        #[test]
        fn test_fixed_length_string() -> Result<(), DeError> {
            let expected = String { name: std::string::String::from("FixedLengthString"), id: 8, r#type: StringType::FixedLength, length: Some(10), delimiter: None };
            let xml = r#"
            <?xml version="1.0" encoding="UTF-8"?>
            <string name="FixedLengthString" id="8" type="fixed-length" length="10"/>
            "#;
            let string: String = from_str(xml)?;
            assert_eq!(expected, string);
            Ok(())
        }

        #[test]
        fn test_zero_terminated_string() -> Result<(), DeError> {
            let expected = String { name: std::string::String::from("ZeroTerminated"), id: 10, r#type: StringType::ZeroTerminated, length: None, delimiter: None };
            let xml = r#"
            <?xml version="1.0" encoding="UTF-8"?>
            <string name="ZeroTerminated" id="10" type="zero-terminated"/>
            "#;
            let string: String = from_str(xml)?;
            assert_eq!(expected, string);
            Ok(())
        }

        #[test]
        fn test_delimiter_terminated_string() -> Result<(), DeError> {
            let expected = String { name: std::string::String::from("DelimiterTerminated"), id: 11, r#type: StringType::DelimiterTerminated, length: None, delimiter: Some(std::string::String::from("0A0A")) };
            let xml = r#"
            <?xml version="1.0" encoding="UTF-8"?>
            <string name="DelimiterTerminated" id="11" type="delimiter-terminated" delimiter="0A0A"/>
            "#;
            let string: String = from_str(xml)?;
            assert_eq!(expected, string);
            Ok(())
        }

        #[test]
        fn test_length_prefixed_string() -> Result<(), DeError> {
            let expected = String { name: std::string::String::from("LengthPrefixed"), id: 13, r#type: StringType::PrefixedLength, length: None, delimiter: None };
            let xml = r#"
            <?xml version="1.0" encoding="UTF-8"?>
            <string name="LengthPrefixed" id="13" type="pascal"/>
            "#;
            let string: String = from_str(xml)?;
            assert_eq!(expected, string);
            Ok(())
        }

        #[test]
        fn test_integer_number_with_byte_length() -> Result<(), DeError> {
            let expected = Number { name: std::string::String::from("IntegerWithByteLenght1"), id: 3, r#type: NumberType::Integer, length: 1, unit: None };
            let xml = r#"
            <?xml version="1.0" encoding="UTF-8"?>
            <number name="IntegerWithByteLenght1" id="3" type="integer" length="1"/>
            "#;
            let number: Number = from_str(xml)?;
            assert_eq!(expected, number);
            Ok(())
        }

        #[test]
        fn test_float_number_with_byte_length() -> Result<(), DeError> {
            let expected = Number { name: std::string::String::from("FloatingPointByteLength2"), id: 15, r#type: NumberType::Float, length: 2, unit: None };
            let xml = r#"
            <?xml version="1.0" encoding="UTF-8"?>
            <number name="FloatingPointByteLength2" id="15" type="float" length="2"/>
            "#;
            let number: Number = from_str(xml)?;
            assert_eq!(expected, number);
            Ok(())
        }

        #[test]
        fn test_integer_number_with_bit_length() -> Result<(), DeError> {
            let expected = Number { name: std::string::String::from("IntegerWithBitLength8"), id: 10, r#type: NumberType::Integer, length: 8, unit: Some(Unit::Bit) };
            let xml = r#"
            <?xml version="1.0" encoding="UTF-8"?>
            <number name="IntegerWithBitLength8" id="10" type="integer" length="8" lengthunit="bit"/>
            "#;
            let number: Number = from_str(xml)?;
            assert_eq!(expected, number);
            Ok(())
        }

        #[test]
        fn test_float_number_with_bit_length() -> Result<(), DeError> {
            let expected = Number { name: std::string::String::from("FloatingPointBitLength16"), id: 18, r#type: NumberType::Float, length: 16, unit: Some(Unit::Bit) };
            let xml = r#"
            <?xml version="1.0" encoding="UTF-8"?>
            <number name="FloatingPointBitLength16" id="18" type="float" length="16" lengthunit="bit"/>
            "#;
            let number: Number = from_str(xml)?;
            assert_eq!(expected, number);
            Ok(())
        }

        #[test]
        fn can_parse_ufwb_structure() -> Result<(), DeError> {
            let xml = r#"
            <?xml version="1.0" encoding="UTF-8"?>
            <ufwb version="1.17">
                <grammar name="TestGrammar" start="id:1" author="Nicola Coretti" email="nico.coretti@gmail.com" complete="yes">
                    <description>Some  basic grammar</description>
                    <structure name="struct1" id="1" encoding="ISO_8859-1:1987" endian="big" signed="no"/>
                </grammar>
            </ufwb>"#;

            let ufwb: Ufwb = from_str(xml)?;
            let expected = Ufwb {
                version: std::string::String::from("1.17"),
                grammar: Grammar {
                    name: std::string::String::from("TestGrammar"),
                    start: std::string::String::from("id:1"),
                    author: std::string::String::from("Nicola Coretti"),
                    email: Some(std::string::String::from("nico.coretti@gmail.com")),
                    complete: std::string::String::from("yes"),
                    structure: RootStructure {
                        name: std::string::String::from("struct1"),
                        id: 1,
                        encoding: std::string::String::from("ISO_8859-1:1987"),
                        endian: Endianess::Big,
                        signed: Signedness::Unsigned,
                        items: None,
                    },
                    description: std::string::String::from("Some  basic grammar"),
                },
            };
            assert_eq!(expected, ufwb);
            Ok(())
        }
    }
}


