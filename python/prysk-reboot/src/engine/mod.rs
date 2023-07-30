mod comparator;
mod input;
mod output;
mod runtime;
mod target;
mod test;

use std::collections::HashMap;
use std::path::PathBuf;

#[derive(PartialEq, Debug)]
pub struct Environment {
    working_dir: PathBuf,
    env: HashMap<String, String>,
}
