use std::fs::File;
use std::io::{Cursor, Read, Write};
use std::path::{Path, PathBuf};
use tempfile::TempDir;

#[derive(Debug)]
pub struct DirectoryBuilder {
    root: TempDir,
    backup: Option<PathBuf>,
}

// TODO: Description if add_file shall be supported add conversion to FileContent
pub struct FileContent {
    src: Box<dyn Read>,
}

impl FileContent {
    /// Creates a new `FileContent` using the provided `std::io::Read`er
    /// as data source.
    pub fn new<R: 'static + Read>(src: R) -> Self {
        Self { src: Box::new(src) }
    }
}

impl Read for FileContent {
    fn read(&mut self, buf: &mut [u8]) -> std::io::Result<usize> {
        self.src.read(buf)
    }
}

impl From<Vec<u8>> for FileContent {
    fn from(data: Vec<u8>) -> Self {
        FileContent {
            src: Box::new(Cursor::new(data)),
        }
    }
}

impl From<&str> for FileContent {
    fn from(data: &str) -> Self {
        FileContent {
            src: Box::new(Cursor::new(
                data.as_bytes().iter().cloned().collect::<Vec<u8>>(),
            )),
        }
    }
}

impl From<String> for FileContent {
    fn from(data: String) -> Self {
        FileContent {
            src: Box::new(Cursor::new(data.into_bytes())),
        }
    }
}

fn add_content<W, D>(src: D, mut dst: W)
where
    W: Write,
    D: Into<FileContent>,
{
    let mut content: FileContent = src.into();
    std::io::copy(&mut content, &mut dst).expect("Could not write data");
}

impl DirectoryBuilder {
    pub fn new() -> Self {
        Self {
            root: tempfile::Builder::new()
                .prefix("brickster")
                .tempdir()
                .expect("Could not create temporary directory"),
            backup: None,
        }
    }

    pub fn add_file<R: Into<FileContent>>(&mut self, path: &Path, data: R) {
        let data: FileContent = data.into();
        let path = self.root.path().join(path);
        let mut file =
            File::create(&path).expect(&format!("Could not create test file {:?}", &path));
        std::io::copy::<FileContent, dyn Write>(&mut data.into(), &mut file)
            .expect(&format!("Failed to write data to test file {:?}", &path));
    }

    pub fn backup(&mut self, path: &str) {
        self.backup = Some(PathBuf::new().join(path));
    }

    pub fn configure<F>(mut self, mut closure: F) -> Self
    where
        F: FnMut(&mut Self),
    {
        closure(&mut self);
        self
    }
}

impl Drop for DirectoryBuilder {
    fn drop(&mut self) {
        if let Some(path) = &self.backup {
            // TODO: Check result, on error print warning/info to stderr
            fs_extra::copy_items(&[&self.root], path, &fs_extra::dir::CopyOptions::new());
        }
    }
}

#[cfg(test)]
mod tests {
    use crate::fs::{add_content, DirectoryBuilder, FileContent};
    use std::io::{Cursor, Seek};
    use std::io::{Read, Write};

    #[test]
    fn add_byte_vector_as_content() {
        let mut file = Cursor::new(Vec::<u8>::new());
        let content: Vec<u8> = (0..10).collect();

        add_content(content, &mut file);
        file.rewind().unwrap();

        let expected = (0..10).collect::<Vec<u8>>();
        assert_eq!(
            expected,
            file.bytes().filter_map(|r| r.ok()).collect::<Vec<u8>>()
        )
    }

    #[test]
    fn add_str_as_content() {
        let mut file = Cursor::new(Vec::<u8>::new());
        let content = "abcde";

        add_content(content, &mut file);
        file.rewind().unwrap();

        let expected = vec![97u8, 98u8, 99u8, 100u8, 101u8];
        assert_eq!(
            expected,
            file.bytes().filter_map(|r| r.ok()).collect::<Vec<u8>>()
        )
    }

    #[test]
    fn add_string_as_content() {
        let mut file = Cursor::new(Vec::<u8>::new());
        let content = String::from("abcde");

        add_content(content, &mut file);
        file.rewind().unwrap();

        let expected = vec![97u8, 98u8, 99u8, 100u8, 101u8];
        assert_eq!(
            expected,
            file.bytes().filter_map(|r| r.ok()).collect::<Vec<u8>>()
        )
    }
}
