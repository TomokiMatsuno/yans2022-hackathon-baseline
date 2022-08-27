import sys
import json
import csv
import statistics
from collections import Counter, defaultdict


fields = ['customer_idx', 'mean_votes', 'sd_votes', 'stars1', 'stars2', 'stars3', 'stars4', 'stars5']
writer = csv.writer(sys.stdout, delimiter='\t')
writer.writerow(fields)

customer_idx2num_rating = dict()
customer_idx2votes = defaultdict(list)

for line in sys.stdin:
    d = json.loads(line)
    star_rating = d['star_rating']
    customer_idx = d['customer_idx']
    if customer_idx not in customer_idx2num_rating:
        customer_idx2num_rating[customer_idx] = Counter()
    customer_idx2num_rating[customer_idx][star_rating] += 1
    if 'helpful_votes' in d:
        customer_idx2votes[customer_idx].append(d['helpful_votes'])

for customer_idx, cnt in customer_idx2num_rating.items():
    votes = customer_idx2votes[customer_idx]
    mean_vote = sum(votes) / len(votes) if len(votes) > 0 else None
    sd_vote = statistics.stdev(votes) if len(votes) > 1 else None
    writer.writerow([customer_idx] + [mean_vote, sd_vote] + [cnt[i] for i in range(1, 6)])


