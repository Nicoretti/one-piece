//! # bricks
//!
//! Is a set of tools to keep your files clean. It provides various handy tools, and library code
//! to either fix or check for common irregularities in text files (e.g. trailing whitespaces).
//!
//! ## Tools
//!
//! - [x] **trailing**: remove or check for trailing whitespaces.
//! - [ ] **spaces**: replaces all tabs with spaces or checks if tabs are used for indentation.
//! - [ ] **seek**: skip/select only parts of a file (similar to `head` and `tail`).
//! - [ ] **mixed**: checks if the file uses mixed intendation (tabs and spaces).
//! - [ ] **inplace**:helper tool "execute" changes to a file "inplace".
use std::io::Read;
use std::io::Write;

pub mod cli {

    use anyhow::{anyhow, Error};
    use std::{
        convert::Into,
        path::{Path, PathBuf},
        str::FromStr,
    };

    #[derive(Debug)]
    pub enum Input {
        Stdin,
        File { path: PathBuf },
    }

    #[derive(Debug)]
    pub enum Output {
        Stdout,
        File { path: PathBuf },
    }

    impl Into<Box<dyn std::io::Read>> for Input {
        fn into(self) -> Box<dyn std::io::Read> {
            match self {
                Input::Stdin => Box::new(std::io::stdin()),
                Input::File { path } => Box::new(std::fs::File::open(path).unwrap()),
            }
        }
    }

    impl Into<Box<dyn std::io::Write>> for Output {
        fn into(self) -> Box<dyn std::io::Write> {
            match self {
                Output::Stdout => Box::new(std::io::stdout()),
                Output::File { path } => Box::new(std::fs::File::open(path).unwrap()),
            }
        }
    }

    impl FromStr for Input {
        type Err = Error;
        fn from_str(s: &str) -> Result<Self, Self::Err> {
            match s.to_lowercase().as_ref() {
                "-" => Ok(Input::Stdin),
                _ => {
                    let path = Path::new(s).to_path_buf();
                    if path.exists() {
                        Ok(Input::File { path })
                    } else {
                        Err(anyhow!("Could not find file {:?}", path))
                    }
                }
            }
        }
    }

    impl FromStr for Output {
        type Err = Error;
        fn from_str(s: &str) -> Result<Self, Self::Err> {
            match s.to_lowercase().as_ref() {
                "-" => Ok(Output::Stdout),
                _ => {
                    let path = Path::new(s).to_path_buf();
                    if !path.exists() {
                        Ok(Output::File { path })
                    } else {
                        Err(anyhow!("File already exists {:?}", path))
                    }
                }
            }
        }
    }
}

pub fn create_reader(path: &str) -> std::io::Result<Box<dyn std::io::Read>> {
    match path {
        "stdin" => Ok(Box::new(std::io::stdin())),
        _ => Ok(Box::new(std::fs::File::open(path)?)),
    }
}

pub fn process<R: ?Sized, W: ?Sized, F>(
    reader: &mut R,
    writer: &mut W,
    mut process: F,
) -> std::io::Result<usize>
where
    R: Read,
    W: Write,
    F: FnMut(&mut R, &mut W) -> std::io::Result<usize>,
{
    let bytes_written = process(reader, writer)?;
    Ok(bytes_written)
}

pub mod reporter {
    use std::io::BufRead;
    use std::io::Read;
    use std::io::Write;

    pub struct FileReporter {
        file_name: String,
    }

    impl FileReporter {
        pub fn new(file_name: &str) -> Self {
            FileReporter {
                file_name: String::from(file_name),
            }
        }

        // TODO: make it generic -> call it report and pass a closure for the work
        pub fn report_trailing_whitespaces<R: ?Sized, W: ?Sized>(
            &self,
            reader: &mut R,
            writer: &mut W,
        ) -> std::io::Result<usize>
        where
            R: Read,
            W: Write,
        {
            let mut reported_issues = 0usize;
            for (line_no, line) in std::io::BufReader::new(reader).lines().enumerate() {
                let l = line?;
                if l != l.trim_end() {
                    writer.write_fmt(format_args!(
                        "Trailing whitespace detected, File: {}, Line: {}\n",
                        self.file_name,
                        line_no + 1
                    ))?;
                    reported_issues += 1;
                }
            }
            Ok(reported_issues)
        }
    }
}

pub mod transformations {

    use std::io::BufRead;
    use std::io::Read;
    use std::io::Write;

    /// example
    ///
    /// ```
    /// let x = 1;
    /// assert_eq!(x, 1);
    ///
    /// ```
    pub fn remove_trailing_whitespaces<R: Read, W: Write>(
        reader: &mut R,
        writer: &mut W,
    ) -> std::io::Result<usize> {
        let mut bytes_written = 0usize;
        for line in std::io::BufReader::new(reader).lines() {
            let mut output_line = String::from(line?.trim_end());
            output_line.push('\n');
            writer.write_all(output_line.as_bytes())?;
            bytes_written += output_line.len();
        }
        Ok(bytes_written)
    }
}

#[cfg(test)]
mod tests {

    use super::*;
    use std::io::Cursor;

    #[test]
    fn remove_trailing_whitespaces_transformation_test() {
        let mut reader = Cursor::new(b"aa   \n    \n a\t\n".to_vec());
        let mut writer = Cursor::new(vec![0; 0]);
        let expected_data: Vec<u8> = b"aa\n\n a\n".to_vec();
        let expected_bytes_written = 7usize;
        let result = process(
            &mut reader,
            &mut writer,
            transformations::remove_trailing_whitespaces,
        );
        assert!(result.is_ok());
        assert_eq!(result.ok(), Some(expected_bytes_written));
        assert_eq!(writer.into_inner(), expected_data);
    }
    #[test]
    fn report_trailing_whitespaces() {
        let mut reader = Cursor::new(b"aa\n    a   \t\n".to_vec());
        let mut writer = Cursor::new(vec![0; 0]);
        let reporter = reporter::FileReporter::new("f.txt");
        let result = process(&mut reader, &mut writer, |mut reader, mut writer| {
            let reported_items = reporter.report_trailing_whitespaces(&mut reader, &mut writer)?;
            Ok(reported_items)
        });
        assert!(result.is_ok());
        assert_eq!(result.ok(), Some(1));
        assert_eq!(
            String::from_utf8_lossy(&writer.into_inner()),
            "Trailing whitespace detected, File: f.txt, Line: 2\n"
        );
    }
}
