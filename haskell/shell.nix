with (import <nixpkgs> {});

mkShell {
  buildInputs = [
    ghc
    ihaskell
    cabal-install
    haskell-language-server
  ];
  shellHook = ''
  '';
}
