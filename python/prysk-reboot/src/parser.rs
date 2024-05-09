use pest_derive::Parser;

pub mod prysk2spaces {

    #[derive(super::Parser)]
    #[grammar = "prysk2spaces.pest"]
    pub struct PryskParser;
}

pub mod prysk4spaces {

    #[derive(super::Parser)]
    #[grammar = "prysk4spaces.pest"]
    pub struct PryskParser;
}

pub fn to_ast() {
}
