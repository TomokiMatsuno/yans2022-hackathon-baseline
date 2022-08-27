# {"marketplace":"JP","product_title":"ニューヨークの恋人 期間限定スペシャルプライス [DVD]","product_category":"Video DVD","star_rating":4,"helpful_votes":1,"vine":"N","verified_purchase":"Y","review_headline":"素敵なラブストーリー","review_body":"時空を超えてきた貴族とキャリアな現代女性の恋物語。うっとりと見てしまいました。ヒュージャックマンが貴族で、Xマンの野性的な役とは真逆な紳士。私はこっちのほうが適役だと思います。","review_date":"2014-01-14","review_idx":190830,"product_idx":36452,"customer_idx":116421,"sets":"training-train"}

import json
import sys
import argparse

arg_parser = argparse.ArgumentParser()
arg_parser.add_argument('--product_titles_file', type=argparse.FileType('r'), default=None)
arg_parser.add_argument('--review_headlines_file', type=argparse.FileType('r'), default=None)
args = arg_parser.parse_args()

review_idx2product_title = dict()

if args.product_titles_file is not None:
    for line in args.product_titles_file:
        review_idx, title = line.rstrip('\n').split('\t')
        review_idx2product_title[int(review_idx)] = title

review_idx2review_headline = dict()
if args.review_headlines_file is not None:
    for line in args.review_headlines_file:
        review_idx, title = line.rstrip('\n').split('\t')
        review_idx2review_headline[int(review_idx)] = title



SEP_TOKEN='</s>'
for line in sys.stdin:
    line = line.rstrip('\n')
    d = json.loads(line)
    review_idx = d['review_idx']

    product_title = review_idx2product_title[review_idx] if review_idx in review_idx2product_title else d['product_title']
    review_headline = review_idx2review_headline[review_idx] if review_idx in review_idx2review_headline else d['review_headline']

    text = SEP_TOKEN.join([product_title, review_headline, d['review_body']])
    d['review_body'] = text
    print(json.dumps(d, ensure_ascii=False), file=sys.stdout)

