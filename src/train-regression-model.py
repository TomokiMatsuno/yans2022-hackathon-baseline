import argparse
import pandas as pd
import numpy as np
import os
import pickle
from sklearn.model_selection import KFold
from lightgbm import LGBMRegressor
import torch

arg_parser = argparse.ArgumentParser()
arg_parser.add_argument('-infile', type=str)
#arg_parser.add_argument('-pred_result_file', type=argparse.FileType('w'))
arg_parser.add_argument('-outdir', type=str, default='output_training')
arg_parser.add_argument('--kfold', type=int, default=5)
arg_parser.add_argument('--cls_vectors', default=None)
args = arg_parser.parse_args()


os.makedirs(args.outdir)
pred_result_file = open(args.outdir + '/predict_result.tsv', 'w')
model_file = args.outdir + '/model_fold{i}.pkl'

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


kf = KFold(n_splits=args.kfold)
pred_results = []
review_indices = []

for fold_i, (train_index, test_index) in enumerate(kf.split(X)):
    test_review_indices = np_review_indices[test_index]
    X = X[:,1:]
    X_train, X_test = X[train_index], X[test_index]
    y_train, y_test = y[train_index], y[test_index]

    model = LGBMRegressor(boosting_type='gbdt', objective='regression',
                      n_estimators=10000)

    model.fit(X_train, y_train)
    y_pred = model.predict(X_test)
    pred_results += list(y_pred)
    review_indices += list(test_review_indices)
    with open(model_file.format(i=str(fold_i)), 'wb') as wf:
        pickle.dump(model, wf)


for pred, review_index in zip(pred_results, test_review_indices):
    print(review_index, pred, sep='\t', file=pred_result_file)


