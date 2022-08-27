import sys
import json
import csv
from collections import Counter

"""
num_reviews
num_rating_[1-5]
"""

fields = ['product_idx', 'customer_idx', 'stars1', 'stars2', 'stars3', 'stars4', 'stars5']
writer = csv.writer(sys.stdout, delimiter='\t')
writer.writerow(fields)

prod_idx2num_rating = dict()
for line in sys.stdin:
    d = json.loads(line)
    star_rating = d['star_rating']
    product_idx = d['product_idx']
    customer_idx = d['customer_idx']
    if product_idx not in prod_idx2num_rating:
        prod_idx2num_rating[product_idx] = Counter()
    prod_idx2num_rating[product_idx][star_rating] += 1

for prod_idx, cnt in prod_idx2num_rating.items():
    writer.writerow([prod_idx, customer_idx] + [cnt[i] for i in range(1, 6)])


