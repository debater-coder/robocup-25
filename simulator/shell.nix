with (import <nixpkgs> {});

pkgs.stdenv.mkDerivation rec {
  name = "dev-shell";

  buildInputs = with pkgs; [
    fontconfig
    mono6
    xorg.libX11
    xorg.libX11.dev
    zlib
  ];

  LD_LIBRARY_PATH = "${lib.makeLibraryPath buildInputs}";
}
