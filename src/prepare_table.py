import argparse
from collections import namedtuple
import pandas as pd
import numpy as np

arg_parser = argparse.ArgumentParser()

arg_parser.add_argument('-customer', type=str)
arg_parser.add_argument('-product', type=str)
arg_parser.add_argument('-review', type=str)
arg_parser.add_argument('-pred_score', type=str)
arg_parser.add_argument('-outfile', type=str)
arg_parser.add_argument('--mode', default='training')

args = arg_parser.parse_args()

df_customer = pd.read_csv(args.customer, sep='\t')
df_product = pd.read_csv(args.product, sep='\t')
df_review = pd.read_csv(args.review, sep='\t', low_memory=False)
df_pred_score = pd.read_csv(args.pred_score, sep='\t')

df = pd.merge(df_review, df_pred_score, on='review_idx', how='inner', suffixes=['', '_'])
df = pd.merge(df, df_product, on='product_idx', how='inner', suffixes=['', '_product'])
df = pd.merge(df, df_customer, on='customer_idx', how='inner', suffixes=['', '_customer'])
columns = ['review_idx', 'review_datedelta', 'nth_review', 'star_rating', 'vine', 'verified_purchase', 'stars1', 'stars2', 'stars3', 'stars4', 'stars5', 'mean_votes', 'sd_votes', 'stars1_customer', 'stars2_customer', 'stars3_customer', 'stars4_customer', 'stars5_customer', 'pred', 'helpful_votes']

#na_helpful_votes = df['helpful_votes'].notna()
#df[na_helpful_votes] = df['helpful_votes'][0]
#df['helpful_votes'] = np.log(df['helpful_votes']  + 1)
#df[na_helpful_votes] = None

if args.mode == 'training':
    df = df[df['pred'].notna()]

df = df[columns]
df.to_csv(args.outfile, sep='\t')


