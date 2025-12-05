import sys

from polyominoes import ominoes_dict

if len(sys.argv) < 2:
    sys.exit()

n = sys.argv[1]

if n not in ominoes_dict:
    print("Not avaiable!")
    sys.exit()

print(len(ominoes_dict[int(n)]))
