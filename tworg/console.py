""" CLI for tworg """
import argparse
import os

from .tworg import Convertor

def run():
    parser = argparse.ArgumentParser(
        description='Convert .tid TiddlyWiki files into Org Mode files.')
    parser.add_argument('tiddler', type=str, nargs='+',
                        help='Tiddlers to convert')
    parser.add_argument('-o', '--output', type=str, nargs=1, required=False,
                        default='./', help='Directory to write org files to')
    args = parser.parse_args()

    for fp in args.tiddler:
        print(fp)
        # Ignore system tiddlers
        if not fp.split('/')[-1].startswith('$_'):
            c = Convertor()
            with open(fp, 'r') as f:
                c.load(f)
            if c.metadata['title']:
                with open(os.path.join(
                        args.output[0],
                        c.metadata['title'].replace('/', '_') + '.org'),
                          'w') as f:
                    print(c, file=f)
