# Source - https://stackoverflow.com/a/42929351
# Posted by Michael Dorner, modified by community. See post 'Timeline' for change history
# Retrieved 2026-10-26, License - CC BY-SA 4.0

import argparse

parser = argparse.ArgumentParser("simple_example")
parser.add_argument("counter", help="An integer will be increased by 1 and printed.", type=int)
args = parser.parse_args()
print(args.counter + 1)
