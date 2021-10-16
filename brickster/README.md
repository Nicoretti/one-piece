# Brickster
Integration test command line tools, using rust code and/or the Brickster DSL.

## Acknowlegements
Inspiration was drawn from: assert_cmd, assert_file, cram, ..

## Example usage within rust code
```rust
fn integration_test_cli_xyz() {
    
   let mut integration_test = IntegrationTest::new()
       .env_vars(|env| {
           // clone the current env before executing the test
           vars.clone();
           // clear all environment variables
           vars.clear();
           // add an environment variable to the env
           env["HOME"] =  "~/foo/bar";
           // extend an existing environment variable
           env["HOME"] = env["HOME"];
           // add
           env.add("MISC", "barundso");
           // remove an existing environment variable
           vars.remove("HOME");
       })
       .working_directory(|root| {
           root.add_file("/path", content);
           root.add_directory("/path/foo");
           root.add_file("/path", content);
           root.persists("/patht/to/save", Format::Zip);
       })
       .command(|cmd| {
          cmd.bin("/path/to/binary");
          cmd.args(&["-c", "2", "--ip", "127.0.0.1"]);
          cmd.stdin(Read);
       })
       .into();
    
        integration_test.execute(|result| {
            assert_eq(result.exit_code, 0);
            assert(result.stdout.contains("Foobar"));
            assert(result.stderr.contains("loading ..."));
        });
    
        let expectations : Expectation = [
            Box::new(ReturnCode::new(0)),
            Box::new(Stdout::new("Foobar")),
            Box::new(Stderr::new("loading ..."))
        ];
    
        integration_test.assert(expectations);
}
```