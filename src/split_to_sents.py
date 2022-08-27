import json
import sys
import re

for line in sys.stdin:
    d = json.loads(line)
    review_body = d['review_body']
    review_idx = d['review_idx']
    sent_i = 0
    line_i = 0

    for line in review_body.split('<br />'):
        if len(line) == 0:
            line_i += 1
            continue
        line =  re.sub(r'。+', "。", line)
        sents = line.split('。')
        sents = [sent + ("。" if i < len(sents) - 1 else "") for i, sent in enumerate(sents)]
        for sent in sents:
            if len(sent) == 0:
                sent_i += 1
                continue

            print("{review_idx}\t{line_i}\t{sent_i}\t{sent}".format(review_idx=review_idx, line_i=line_i, sent_i=sent_i, sent=sent), file=sys.stdout)
            sent_i += 1
        line_i += 1

