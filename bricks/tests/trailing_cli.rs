use anyhow::Result;
use assert_cmd::Command;
use assert_fs::prelude::*;
use std::env::temp_dir;
use std::io::Write;

const CONTENT_WITH_TRAILING_WS: &str = r#"
Lorem ipsum
Lorem ipsum Lorem   
Lorem ipsum   
Lorem
ipsum

    Lorem
"#;

const EXPECTED: &str = r#"
Lorem ipsum
Lorem ipsum Lorem
Lorem ipsum
Lorem
ipsum

    Lorem
"#;

#[test]
fn trailing_fail_check() {
    let tmp_dir = assert_fs::TempDir::new().unwrap();
    let testfile = tmp_dir.child("file.txt");
    testfile.write_str(CONTENT_WITH_TRAILING_WS);
    let testfile = tmp_dir.child("file.txt");

    let mut cmd = Command::cargo_bin("trailing").unwrap();
    cmd.arg("-c")
        .arg(testfile.to_str().unwrap())
        .assert()
        .failure();
}

#[test]
fn trailing_removes_all_trailing_ws() {
    let tmp_dir = assert_fs::TempDir::new().unwrap();
    let testfile = tmp_dir.child("file.txt");
    testfile.write_str(CONTENT_WITH_TRAILING_WS);
    let mut cmd = Command::cargo_bin("trailing").unwrap();
    let assert = cmd.arg(testfile.to_str().unwrap()).assert();
    assert.code(0).stdout(EXPECTED);
}
