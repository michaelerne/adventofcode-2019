let
  fetch = { rev, sha256 }:
    builtins.fetchTarball {
      url = "https://github.com/NixOS/nixpkgs/archive/${rev}.tar.gz";
      sha256 = sha256;
    };

  pkgsPath = fetch {
    rev = "074f4444e28566498303c396000c6cb898965cd4";

    # Generate the SHA256 hash for this revision's tarball.
    #
    #   $ nix-prefetch-url --unpack --type sha256 \
    #   >   https://github.com/NixOS/nixpkgs/archive/${rev-defined-above}.tar.gz
    #
    # Example:
    #   $ nix-prefetch-url --unpack --type sha256 \
    #   >   https://github.com/NixOS/nixpkgs/archive/c2d01c0dd5a3dca943827bc53743492fff2b3cfc.tar.gz
    #
    sha256 = "13gwghkqhcz3a4kmm32lh0gdw7y3q0az88rqfqy0hf9gab245f0p";
  };

in { pkgs = import pkgsPath {}; }
