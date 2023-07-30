//! # Problem:
//! Implement sort on a huge file (e.g. 1000 TB) which can't fit into "RAM"
//!
//! constrains: * Disk Space basically unlimited
//!             * Dedicated RAM to load file contents for sorting into is limited max 8 GB
//!
//! # Solution
//! 1. split the input file up into multiple processable chunks
//! 2. sort each individual chunk (file)
//! 3. merge the chunks

use std::fs::File;
use std::io::{BufRead, BufWriter, Read, Write};
use std::path::Path;

/// Chunks the contents of a reader into multiple files.
///
/// # Arguments
/// * `input` reader whose content shall be chunked.
/// * `path` base path which shall be used as prefix path for all resulting chunk files.
/// * `chunk_size` maximum size of a single chunk (file).
///
/// # Example
/// ```
/// // nothing to run yet
/// ```
/// This function will return a vec of strings which point to the chunk files.
/// TODO: * cleanup unwraps!
pub fn chunk_reader_into_files<R: Read>(input: R, path: &str, chunk_size: usize) -> Vec<String> {
    let buf_size: usize = 1024 * 1024; // Assumption: 1 MB Max line length (Bytes)
    let reader = std::io::BufReader::with_capacity(buf_size, input);
    let mut chunks: Vec<String> = Vec::new();
    let mut index: usize = 0;
    let mut current_size: usize = 0;
    let mut chunk_path: Option<String> = Some(format!("{}_{}.txt", path, index));
    let mut writer: Option<BufWriter<File>> = Some(BufWriter::with_capacity(
        buf_size,
        std::fs::File::create(chunk_path.as_ref().unwrap()).unwrap(),
    ));
    for l in reader.lines() {
        let line = l.unwrap();
        if current_size + line.len() > chunk_size {
            index += 1;
            current_size = 0;
            chunks.push(String::from(chunk_path.take().unwrap()));
            chunk_path = Some(format!("{}_{}.txt", path, index));
            writer = Some(BufWriter::with_capacity(
                buf_size,
                std::fs::File::create(chunk_path.as_ref().unwrap()).unwrap(),
            ));
        }
        current_size += line.len();
        writer.as_mut().unwrap().write(line.as_bytes()).unwrap();
    }
    chunks.push(String::from(chunk_path.take().unwrap()));
    chunks
}

#[cfg(test)]
mod tests {
    use crate::interview_tasks::huge_file::chunk_reader_into_files;
    use std::io::Cursor;

    #[test]
    fn test_chunking_function() {
        let chunk_size = 10usize;
        let line_count = 10usize;
        let huge_content: Cursor<Vec<u8>> = Cursor::new({
            let mut v: Vec<u8> = Vec::new();
            for i in 0..line_count {
                let mut s = String::new();
                for j in 0..chunk_size {
                    s.push((97 + ((i % 26) as u8)) as char);
                }
                s.push('\n');
                v.append(&mut s.clone().bytes().collect::<Vec<u8>>())
            }
            v
        });

        let result = chunk_reader_into_files(huge_content, "base_path", chunk_size);
        println!("{:?}", result);
        assert_eq!(line_count, result.len());
    }
}
