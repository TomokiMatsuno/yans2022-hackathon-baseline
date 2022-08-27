import json
import sys
import re
import argparse

arg_parser = argparse.ArgumentParser()
arg_parser.add_argument('-training_file', type=argparse.FileType('r'))
arg_parser.add_argument('-src_info', type=argparse.FileType('r'))
arg_parser.add_argument('-trans_result', type=argparse.FileType('r'))
arg_parser.add_argument('-out_file', type=argparse.FileType('w'))
arg_parser.add_argument('--review_indices_to_skip_file', type=argparse.FileType('r'), default=None)
args = arg_parser.parse_args()

review_indices_to_skip = set()

#if args.review_indices_to_skip_file is not None:
#    review_indices_to_skip = set([int(l) for l in args.review_indices_to_skip_file])
#
#def write_info(sents, review_idx=None):
#    line = args.training_file.readline()
#    d = json.loads(line)
##    if line is None or len(line) == 0:
##        return
##    #d = json.loads(line)
##    try:
##        d = json.loads(line)
##    except:
##        print(review_idx, line, len(line))
##        exit()
#    while d['review_idx'] in review_indices_to_skip:
#        d = json.loads(args.training_file.readline())
#    assert review_idx is None or d['review_idx'] == int(review_idx), "src_info review_idx:{} training_file review_idx:{}".format(review_idx, d['review_idx'])
#    sents = [''.join(e) for e in sents]
#    d['review_body'] = '<br />'.join(sents)
#    print(json.dumps(d, ensure_ascii=False), file=args.out_file)




review_idx2trans = dict()
sents = [[]]
for line_src_info, line_trans in zip(args.src_info, args.trans_result):
    review_idx, sent_idx, _, _ = line_src_info.rstrip('\n').split('\t')

    if (len(sents[-1]) > 0 and int(sent_idx) == 0):
        review_idx2trans[int(prev_review_idx)] = sents

        #write_info(sents, review_idx)
        #d = json.loads(args.training_file.readline())
        #d['review_body'] = '<br />'.join(sents)
        #print(json.dumps(d), file=args.out_file)
        sents = [[]]
        
    sents[-1].append(line_trans.rstrip('\n'))
    prev_review_idx = review_idx

for line in args.training_file:
    d = json.loads(line)
    if d['review_idx'] not in review_idx2trans:
        continue
    sents = review_idx2trans[d['review_idx']]
    sents = [''.join(e) for e in sents]
    d['review_body'] = '<br />'.join(sents)
    print(json.dumps(d, ensure_ascii=False), file=args.out_file)


#write_info(sents, review_idx)

