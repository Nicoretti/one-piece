# Brickster
Help you to do integration testing for command line tools, 
either with rust or using it's DSL.

## Acknowledgements
Inspiration was drawn from various already existing tools and crates I am a fan of:
cram, assert_cli, assert_cmd, asert_file.

## Example usage within rust code
```rust
fn brickster_example_integration_test() {
    
   let mut integration_test = IntegrationTest::new()
       .environment(|env| {
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
       .working_directory(|cwd| {
           // make sure temporary test dir is backed up after test run
           cwd.backup("/home/user/test_backup/", BackupType::Zip);
           
           cwd.touch("empty_file.txt");
           cwd.add_file("data.db", db);
           cwd.add_directory("sub1", |subdir| {
               subdir.touch("empty_file.txt");
               subdir.add_file("subdb1.db", sub_db1);
               subdir.add_file("subdb2.db", sub_db2);
           });
           cwd.add_directory("sub2/sub3/sub4", |subdir| {
               subdir.add_file("yet_another_db.db", yadb_db);
               subdir.add_directory("sub5", |ssubdir| {
                   ssubdir.touch("empty_file_3.txt");
               });
           }) ;
       })
       .command(|cmd| {
          cmd.bin("/path/to/binary");
          cmd.args(&["-c", "2", "--ip", "127.0.0.1"]);
          cmd.stdin(Read);
       })
       .into();
    
        integration_test.execute(|result, working_dir| {
            assert_eq(result.exit_code, 0);
            assert(result.stdout.contains("Foobar"));
            assert(result.stderr.contains("loading ..."));
            assert(working_dir.file_exits("results.txt"));
        });
    
        let expectations : Expectation = [
            Box::new(ReturnCode::new(0)),
            Box::new(Stdout::new("Foobar")),
            Box::new(Stderr::new("loading ...")),
            Box::new(FileExists::new("results.txt")),
        ];
    
        integration_test.assert(expectations);
}
```