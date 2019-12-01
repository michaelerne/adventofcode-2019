# Advent of Code 2019

My solutions for Advent of Code 2019 in Python

## Getting started
This project uses [`direnv`](https://direnv.net/) and [`nix`](https://nixos.org/nix/). Both must be installed.
```bash
git clone https://github.com/michaelerne/adventofcode-2019
cd adventofcode-2019
direnv allow
```

## Running
This project uses [`advent-of-code-data`](https://pypi.org/project/advent-of-code-data/) to automatically fetch the input and submit the answers. For this to work set [`AOC_SESSION`](https://github.com/wimglenn/advent-of-code-wim/issues/1) in your environment.
```bash
export AOC_SESSION=cafef00db01dfaceba5eba11deadbeef
```

Then, execute the individual days:
```bash
python day_01.py
```

Or run them via the provided `Makefile`:
```bash
make run
```

## Development
To lint this project, run:
```bash
make lint
```
