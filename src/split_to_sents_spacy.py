import json
import sys
import re
import spacy

nlp = spacy.load('ja_core_news_lg')

periods = ['！', '？', '\!', '\?', '笑', '。', '、', '」']

for line in sys.stdin:
    d = json.loads(line)
    review_body = d['review_body']
    review_idx = d['review_idx']
    sent_i = 0
    line_i = 0

    #text = '\n'.join(review_body.split('<br />'))
    text = ''.join(review_body.split('<br />'))

    for period in periods:
        text = re.sub('{period}+'.format(period=period), period, text)

    doc = nlp(text)

    text = '\n'.join([sent.text for sent in doc.sents])
    for period in periods:
        text = re.sub('\n{period}+'.format(period=period), period, text)

    for sent in text.split('\n'):
        text = sent.replace('\n', '')
        #for period in periods:
        #    text = re.sub('\n{period}+'.format(period=period), period, text)
        if sent_i > 0 and len(text) < 2:
            sent_i += 1
            continue
        print("{review_idx}\t{line_i}\t{sent_i}\t{sent}".format(review_idx=review_idx, line_i=line_i, sent_i=sent_i, sent=text), file=sys.stdout)
        sent_i += 1
        line_i += 1

