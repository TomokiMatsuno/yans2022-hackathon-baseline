import json
import sys

train_file = open(sys.argv[1], 'r')
overlaps = [int(l) for l in open(sys.argv[2], 'r')]


for line in train_file:
    line = line.rstrip('\n')
    d = json.loads(line)
    review_idx = int(d['review_idx'])

    if review_idx in overlaps:
        continue

    print(line)

