import json
import sys
import argparse
# {"product_idx":22,"pred_list":[{"review_idx":155312,"pred_score":0.3928122092},{"review_idx":177288,"pred_score":6.1447102056},{"review_idx":3631,"pred_score":1.4159906345},{"review_idx":113220,"pred_score":2.1017274552},{"review_idx":150184,"pred_score":8.1052927688},{"review_idx":115705,"pred_score":8.3365587328},{"review_idx":149366,"pred_score":3.4408372941},{"review_idx":86796,"pred_score":0.9264311629},{"review_idx":140831,"pred_score":1.3132524427},{"review_idx":4329,"pred_score":3.5229258127},{"review_idx":24602,"pred_score":2.1331098286}]}

arg_parser = argparse.ArgumentParser()
arg_parser.add_argument('-pred_score_file', type=argparse.FileType('r'))
arg_parser.add_argument('-old_submit_file', type=argparse.FileType('r'))
arg_parser.add_argument('-new_submit_file', type=argparse.FileType('w'))
args = arg_parser.parse_args()

rev2score = dict()
for line in args.pred_score_file:
    review_idx, score = line.rstrip('\n').split('\t')
    rev2score[int(review_idx)] = float(score)


for line in args.old_submit_file:
    d = json.loads(line)
    d["pred_list"] = [{"review_idx": e["review_idx"], "pred_score": rev2score[e["review_idx"]]} if e["review_idx"] in rev2score else e for e in d["pred_list"]]
    print(json.dumps(d), file=args.new_submit_file)


