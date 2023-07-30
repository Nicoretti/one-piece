use clap::{crate_authors, crate_description, crate_version, App, AppSettings, Arg, SubCommand};

pub fn create_arg_parser<'a, 'b>() -> App<'a, 'b> {
    App::new("A rust based clone of the all time classic xxd tool")
        .version(crate_version!())
        .author(crate_authors!())
        .about(crate_description!())
        .global_settings(&[AppSettings::ColoredHelp])
        .arg(Arg::with_name("outfile")
                 .short("o")
                 .long("output-file")
                 .required(false)
                 .takes_value(true)
                 .global(true)
                 .help("File to which the output will be written (default: stdout)"))
        .arg(Arg::with_name("seek")
                 .short("s")
                 .long("seek")
                 .required(false)
                 .takes_value(true)
                 .global(true)
                 .help("Offset in the file where to start reading"))
        .arg(Arg::with_name("length")
                 .short("l")
                 .long("length")
                 .required(false)
                 .takes_value(true)
                 .global(true)
                 .help("Amount of bytes which shall be read"))
        .subcommand(SubCommand::with_name("dump")
                        .about("Dumps an input file in the appropriate output format")
                        .arg(Arg::with_name("file")
                                 .required(false)
                                 .takes_value(true)
                                 .global(true)
                                 .help("Input file which shall be read (default: stdin)"))
                        .arg(Arg::with_name("plain_hexdump")
                                 .short("p")
                                 .long("plain-hexdump")
                                 .required(false)
                                 .help("output in postscript plain hexdump style."))
                        .arg(Arg::with_name("format")
                                 .short("f")
                                 .long("format")
                                 .required(false)
                                 .takes_value(true)
                                 .possible_value("Hex")
                                 .possible_value("hex")
                                 .possible_value("bin")
                                 .possible_value("oct")
                                 .possible_value("dec")
                                 .help("Specifies the output format for the value (default: hex)"))
                        .arg(Arg::with_name("group-size")
                                 .short("g")
                                 .long("group-size")
                                 .required(false)
                                 .takes_value(true)
                                 .help("Separate  the output of every <bytes> bytes (two hex characters or eight bit-digits each) by a whitespace."))
                        .arg(Arg::with_name("columns")
                                 .short("c")
                                 .long("columns")
                                 .required(false)
                                 .takes_value(true)
                                 .help("Specifies the amount of output columns")))
        .subcommand(SubCommand::with_name("generate")
                        .about("Generates a source file containing the specified file as array")
                        .arg(Arg::with_name("file")
                                 .required(false)
                                 .takes_value(true)
                                 .global(true)
                                 .help("Input file which shall be read (default: stdin)"))
                        .arg(Arg::with_name("template")
                                 .short("t")
                                 .long("template")
                                 .required(false)
                                 .takes_value(true)
                                 .possible_value("c")
                                 .possible_value("cpp")
                                 .possible_value("rust")
                                 .possible_value("python")
                                 .help("Specifies a template file which shall be used for \
                                        generation (default: c)"))
                 )
}