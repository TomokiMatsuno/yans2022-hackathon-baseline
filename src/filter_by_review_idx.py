# {"marketplace":"JP","product_title":"ニューヨークの恋人 期間限定スペシャルプライス [DVD]","product_category":"Video DVD","star_rating":4,"helpful_votes":1,"vine":"N","verified_purchase":"Y","review_headline":"素敵なラブストーリー","review_body":"時空を超えてきた貴族とキャリアな現代女性の恋物語。うっとりと見てしまいました。ヒュージャックマンが貴族で、Xマンの野性的な役とは真逆な紳士。私はこっちのほうが適役だと思います。","review_date":"2014-01-14","review_idx":190830,"product_idx":36452,"customer_idx":116421,"sets":"training-train"}

import json
import sys
import argparse

arg_parser = argparse.ArgumentParser()
arg_parser.add_argument('--review_idx_to_skip_file', type=argparse.FileType('r'), default=None)
args = arg_parser.parse_args()

review_idx_to_skip = set()

for line in args.review_idx_to_skip_file:
    review_idx = int(line.rstrip('\n'))
    review_idx_to_skip.add(review_idx)

for line in sys.stdin:
    line = line.rstrip('\n')
    d = json.loads(line)
    review_idx = d['review_idx']
    if review_idx not in review_idx_to_skip:
        print(json.dumps(d, ensure_ascii=False), file=sys.stdout)

