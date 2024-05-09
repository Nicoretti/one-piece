use clap;
use anyhow::{anyhow, Result};
use pest::iterators::Pairs;
use pest::Parser;
use prysk_core::parser::prysk2spaces::PryskParser as PryskParser2;
use prysk_core::parser::prysk2spaces::Rule as RulePrysk2;
use prysk_core::parser::prysk4spaces::PryskParser as PryskParser4;
use prysk_core::parser::prysk4spaces::Rule as RulePrysk4;
use std::{fs, path::PathBuf};

/// Parse prysk/cram (*.t) and output parsing rule matches
#[derive(clap::Parser, Debug)]
#[command(version, about, long_about=None)]
struct Args {
    /// Path to cram/prysk file to parse.
    file: PathBuf,
    // add indent configuration 2/4 - Spaces
}

fn pretty_print<R: pest::RuleType>(pairs: Pairs<R>, indent: usize) {
    use console::Style;
    let color = [
        Style::new().green(),
        Style::new().blue(),
        Style::new().magenta(),
        Style::new().yellow(),
        Style::new().cyan(),
    ];
    for pair in pairs {
        let color = color[indent % 5].clone();
        let inner_pairs = pair.clone().into_inner();
        let indent_str = " ".repeat(indent);
        println!(
            "{}{:35}{:?}",
            indent_str,
            format!("{:?}", color.apply_to(pair.as_rule())),
            color.apply_to(pair.as_str())
        );

        if inner_pairs.peek().is_some() {
            pretty_print(inner_pairs, indent + 1);
        }
    }
}

fn main() {
    use clap::Parser;
    let args = Args::parse();
    let file_contents = fs::read_to_string(args.file).expect("Unable to read file");
    let spaces = 2;
    let result = match spaces {
        _ => PryskParser2::parse(RulePrysk2::File, &file_contents),
        //_ => PryskParser4::parse(RulePrysk4::File, &file_contents),
        //_ => Err(anyhow!("Unsupported indent with")),
    };
    match result {
        Ok(pairs) => {
            pretty_print(pairs, 0);
        }
        Err(e) => eprintln!("{:?}", e),
    }
}
