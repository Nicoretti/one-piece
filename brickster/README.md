# Brickster
Integration test command line tools, using rust code and/or the Brickster DSL.

## Acknowlegements
Inspiration was drawn from: assert_cmd, assert_file, cram, ..

## Example usage within rust code
```rust
fn integration_test_cli_xyz() {
    let env = TestEnvironment::new()
        // directory in which the test(s) will be executed
        .cwd()
            // creates a temporary directory for the test run
            .tmp_directory()
            // add a file to the test directory
            .add_file(File, String, Cursor, Read, ...)
            // add a directory to the test directory
            .add_directory(Path, Directory, Zip, ..)
            // set an already existing directory as test dir
            // no automatic cleanup will be done
            .set(Path, ...)
        .env()
            // add an environment variable to the env
            .add("HOME", "~/foo/bar")
            .add("MISC", "barundso")
            // extend an existing environment variable
            .append("HOME", ":/path/to/xyz")
            // remove an existing environment variable
            .remove("HOME")
            // clone the current env before executing the test
            .clone()
            // clear all environment variables
            .clear()
        // transform the builder into an TestEnvironment type
        .into();
    
    let cmd = Command::new()
        // transform the builder into a Command object.
        .into();
    
   IntegrationTest::new(env).run(cmd, |result| {
       assert_eq(result.exit_code, 0);
       assert(result.stdout.contains("Foobar"));
       assert(result.stderr.contains("loading ..."));
   })
}
```