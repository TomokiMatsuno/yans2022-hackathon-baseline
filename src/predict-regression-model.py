import argparse
import pandas as pd
import numpy as np
import torch
import os
import pickle
from sklearn.model_selection import KFold
from lightgbm import LGBMRegressor

arg_parser = argparse.ArgumentParser()
arg_parser.add_argument('-infile', type=str)
arg_parser.add_argument('-pred_result_file', type=argparse.FileType('w'))
arg_parser.add_argument('-model_file', type=argparse.FileType('rb'))
arg_parser.add_argument('--cls_vectors', default=None)
#arg_parser.add_argument('-model_file', type=str)
args = arg_parser.parse_args()


#pred_result_file = open(args.outdir + '/predict_result.tsv', 'w')
pred_result_file = args.pred_result_file
#model_file = args.outdir + '/model_fold{i}.pkl'

df = pd.read_csv(args.infile, sep='\t')
print(df.shape, df.columns)
np_review_indices = df['review_idx']
np_mtx = df.to_numpy()
#X = df.iloc[:,:-1].to_numpy
#y = df.iloc[:,-1].to_numpy

X = np_mtx[:,:-1]
y = np_mtx[:,-1]

if args.cls_vectors is not None:
    cls_vectors = torch.load(args.cls_vectors).to('cpu').detach().numpy().copy()
    X = np.concatenate((X, cls_vectors[:X.shape[0],:]), 1)

pred_results = []
review_indices = []
model = pickle.load(args.model_file)
X = X[:,1:]
pred_results = list(model.predict(X))
for pred, review_index in zip(pred_results, list(np_review_indices)):
    print(review_index, pred, sep='\t', file=pred_result_file)

