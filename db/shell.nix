with (import <nixpkgs> {});

mkShell {
  buildInputs = [
    usql
    sqlite 
    sqldiff
    sqlite-utils 
  ];
  shellHook = ''
  '';
}
