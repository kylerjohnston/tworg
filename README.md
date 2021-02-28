# tworg

This is a small program to convert [TiddlyWiki](https://tiddlywiki.com/) tiddler (`*.tid`) files into [Org Mode](https://orgmode.org/) files.

This is not at all production-ready and was written as a one-off thing to convert my TiddlyWiki into a set of org files. As such, it makes a few assumptions:

- The only metadata it preserves in the org files are `TITLE`, `AUTHOR`, and `TAGS`.
- It replaces links to other tiddlers with Org-roam links. Thus, it assumes you are using [Org-roam](https://www.orgroam.com/).
- Definitely not 100% coverage of the TiddlyWiki markup syntax.

## Usage

``` shell
usage: tworg [-h] [-o OUTPUT] tiddler [tiddler ...]

Convert .tid TiddlyWiki files into Org Mode files.

positional arguments:
  tiddler               Tiddlers to convert

optional arguments:
  -h, --help            show this help message and exit
  -o OUTPUT, --output OUTPUT
                        Directory to write org files to
```

Example, converting all TiddlyWiki files in `~/tiddlywiki/` to Org Mode files in `~/org/`:

``` shell
tworg -o ~/org/ ~/tiddlywiki/*.tid
```

