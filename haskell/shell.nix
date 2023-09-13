with (import <nixpkgs> {});

mkShell {
  LOCALE_ARCHIVE_2_27 = "${glibcLocales}/lib/locale/locale-archive";
  buildInputs = [
    ghc
    ihaskell
  ];
  shellHook = ''
  '';
}
