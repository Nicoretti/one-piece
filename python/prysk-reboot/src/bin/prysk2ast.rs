use pest::{iterators::Pair, Parser};
use std::fs;

use prysk_core::parser::prysk2spaces::{Rule, PryskParser};

use pest::iterators::Pairs;

fn pretty_print(pairs: Pairs<Rule>, indent: usize) {
    for pair in pairs {
        let inner_pairs = pair.clone().into_inner();
        let indent_str = "  ".repeat(indent);  // Adjust the indentation
        println!("{}{:?}: {}", indent_str, pair.as_rule(), pair.as_str());

        if inner_pairs.peek().is_some() {
            pretty_print(inner_pairs, indent + 1);
        }
    }
}

fn main() {
    // Specify your Prysk file path here
    //let file_path = "/home/nicoretti/projects/one-piece/python/prysk-reboot/t.t";
    let file_path = "/home/nicoretti/projects/prysk/examples/test.t";
    let file_contents = fs::read_to_string(file_path).expect("Unable to read file");


    match PryskParser::parse(Rule::File, &file_contents) {
        Ok(pairs) => {
            pretty_print(pairs, 2);
        }
        Err(e) => eprintln!("{:?}", e),
    }
}

fn to_ast(pair: Pair<Rule>) -> PestAstNode {
    PestAstNode {
        rule: pair.as_rule(),
        token: pair.as_str().to_string(),
        children: pair.into_inner().map(to_ast).collect(),
    }
}

#[derive(Debug)]
struct PestAstNode {
    rule: Rule,
    token: String,
    children: Vec<PestAstNode>,
}
