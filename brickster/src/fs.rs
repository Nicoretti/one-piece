use std::fs::File;
use std::io::{Cursor, Read, Write};
use std::path::{Path, PathBuf};
use tempfile::TempDir;

#[derive(Debug)]
pub struct DirBuilder {
    root: TempDir,
    backup: Option<PathBuf>,
}

struct Data<R: Read + Sized> {
    src: R,
}

impl<R: Read + Sized> Read for Data<R> {
    fn read(&mut self, buf: &mut [u8]) -> std::io::Result<usize> {
        self.src.read(buf)
    }
}

impl From<Cursor<Vec<u8>>> for Data<std::io::Cursor<Vec<u8>>> {
    fn from(c: Cursor<Vec<u8>>) -> Self {
        Data { src: c }
    }
}

impl DirBuilder {
    pub fn new() -> Self {
        Self {
            root: tempfile::Builder::new()
                .prefix("brickster")
                .tempdir()
                .expect("Could not create temporary directory"),
            backup: None,
        }
    }

    pub fn add_file<R: Read + Sized>(&mut self, path: &Path, data: R)
    where
        Data<R>: From<R>,
    {
        let data: Data<R> = data.into();
        let path = self.root.path().join(path);
        let mut file =
            File::create(&path).expect(&format!("Could not create test file {:?}", &path));
        std::io::copy::<Data<R>, Write>(&mut data.into(), &mut file)
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

impl Drop for DirBuilder {
    fn drop(&mut self) {
        if let Some(path) = &self.backup {
            // TODO: Check result, on error print warning/info to stderr
            fs_extra::copy_items(&[&self.root], path, &fs_extra::dir::CopyOptions::new());
        }
    }
}

#[cfg(test)]
mod tests {
    use std::io::Cursor;
    use std::path::Path;

    #[test]
    fn smoke_test() {
        let tmpdir = super::DirBuilder::new().configure(|dir| {
            let p = Path::new("test.txt");
            let data: Vec<u8> = vec![0x65, 0x65, 0x65, 0x65];
            let c = Cursor::new(data);
            dir.add_file(p, c);
            dir.backup("/Users/nicoretti/");
        });
    }
}
