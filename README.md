## A installer that comes with my [`dotfiles`](https://github.com/jayfaza/dotfiles.git).
```
usage: Jayfaza's dotfiles master. [-h] [-d] [-q] (-u | -i)
options:
  -h, --help     show this help message and exit
  -d, --default
  -q, --quiet
  -u, --update
  -i, --install
```
## How to install:
  - Requirements: ``` pacman -S --needed base-devel ```
  - Installation:
      - ``` git clone https://github.com/jayfaza/dotsmaster.git ```
      - ``` cd dotsmaster ```
      - ``` makepkg -si ```

## Usage:
  - To install my dotfiles: ``` dotsmaster --install ```
  - To update: ``` dotsmaster --update ```
  - It also has flags like: -q/--quiet and -d/--default

## About
  Dotsmaster was built in python because I had an opinion
  that python is good in that kind of stuff like a installation 
  scripting and I've started building that installer and it came
  so far I'd better do this in rust because python can't know
  will everything broke or not. In rust case you can prevent
  almost all problems before it panic, only if it's not a logical
  problem. So thank you to coming here, for now it's everything.
