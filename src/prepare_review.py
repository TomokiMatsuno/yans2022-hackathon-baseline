import sys
import json
from collections import defaultdict
from dateutil import parser
import numpy as np

fields = ['review_idx', 'customer_idx', 'product_idx', 'review_datedelta', 'nth_review', 'helpful_votes', 'star_rating', 'vine', 'verified_purchase']
#"star_rating":4,"helpful_votes":1,"vine":"N","verified_purchase":"Y"
prod_idx2review_info = defaultdict(list)
print('\t'.join(fields))

map_ny = {'N': 0, 'Y': 1}

for line in sys.stdin:
    d = json.loads(line)
    customer_idx = d['customer_idx']
    prod_idx = d['product_idx']
    helpful_votes = np.log(d['helpful_votes'] + 1) if 'helpful_votes' in d else None
    prod_idx2review_info[prod_idx].append((d['review_idx'], parser.parse(d['review_date']), helpful_votes, d['star_rating'], map_ny[d['vine']], map_ny[d['verified_purchase']]))

for prod_idx, review_idx_dates in prod_idx2review_info.items():
    review_idx_dates = sorted(review_idx_dates, key=lambda x:x[1])
    first_review_date = review_idx_dates[0][1]

    for nth_review , (review_idx, review_date, helpful_votes, star_rating, vine, verified_purchase) in enumerate(review_idx_dates):
        datedelta = review_date - first_review_date

        print(review_idx, customer_idx, prod_idx, datedelta.days, nth_review, helpful_votes, star_rating, vine, verified_purchase, sep='\t', file=sys.stdout)

