""" Converts .tid Tiddlywiki files into Org-Mode files """
import argparse
import os

from .tid2org import Convertor

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('tiddler', type=str, nargs='+',
                        help='Tiddlers to convert')
    parser.add_argument('-o', '--output', type=str, nargs=1, required=False,
                        default='./', help='Directory to write org files to')
    args = parser.parse_args()

    for fp in args.tiddler:
        c = Convertor()
        with open(fp, 'r') as f:
            c.load(f)
        if c.metadata['title']:
            with open(os.path.join(
                    args.output[0], c.metadata['title'] + '.org'), 'w') as f:
                print(c, file=f)
