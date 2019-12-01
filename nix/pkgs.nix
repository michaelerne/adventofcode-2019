let
  fetch = { rev, sha256 }:
    builtins.fetchTarball {
      url = "https://github.com/NixOS/nixpkgs/archive/${rev}.tar.gz";
      sha256 = sha256;
    };

  pkgsPath = fetch {
    rev = "d5291756487d70bc336e33512a9baf9fa1788faf";

    # Generate the SHA256 hash for this revision's tarball.
    #
    #   $ nix-prefetch-url --unpack --type sha256 \
    #   >   https://github.com/NixOS/nixpkgs/archive/${rev-defined-above}.tar.gz
    #
    # Example:
    #   $ nix-prefetch-url --unpack --type sha256 \
    #   >   https://github.com/NixOS/nixpkgs/archive/c2d01c0dd5a3dca943827bc53743492fff2b3cfc.tar.gz
    #
    sha256 = "0mhqhq21y5vrr1f30qd2bvydv4bbbslvyzclhw0kdxmkgg3z4c92";
  };

in { pkgs = import pkgsPath {}; }
