{ pkgs ? import <nixpkgs> {} }:

pkgs.mkShell {
  buildInputs = with pkgs; [
    python313
    python313Packages.tkinter
    python313Packages.pandas
    python313Packages.numpy
  ];

  
  shellHook = ''
    echo "Development environment loaded"
    echo "Python: $(python --version)"
  '';
}