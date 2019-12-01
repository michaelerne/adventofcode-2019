let
    pkgs = (import ./pkgs.nix).pkgs;
in
    pkgs.mkShell {
        SOURCE_DATE_EPOCH="315532800";

        buildInputs = [
            pkgs.gnumake
            pkgs.python38
            pkgs.python38Packages.virtualenv
        ];
    }

