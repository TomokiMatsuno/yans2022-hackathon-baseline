mkdir -p ./data/preprocessing_table/

#MODE=training
MODE=training-regression
#MODE=leader_board

PREDICT_RESULT=data/predict/predict_helpful_votes/cl-tohoku_bert-base-japanese_lr1e-5/$MODE.jsonl
OUTFILE=data/preprocessing_table/${MODE}-feats-for-training.tsv

PREDICT_RESULT=/home/tomoki/experiments/yans2022/yans2022-hackathon-baseline/data/predict/predict_helpful_votes/xlm-roberta-base-jaen/training-regression.jsonl
OUTFILE=data/preprocessing_table/trainning-regression-feats-for-training.xlm-roberta-jaen.tsv

PREDICT_RESULT=/home/tomoki/experiments/yans2022/pred_results/training-regression_predict_xlm-roberta_jaen_3epochs.jsonl
OUTFILE=/home/tomoki/experiments/yans2022/pred_results/training-regression_predict_xlm-roberta_jaen_3epochs.tsv

python src/prepare_review.py < data/dataset_shared_initial/training-all.jsonl > data/preprocessing_table/training-all-feats-review.tsv
python src/prepare_product.py < data/dataset_shared_initial/training-all.jsonl > data/preprocessing_table/training-all-feats-product.tsv
python src/prepare_customer.py < data/dataset_shared_initial/training-all.jsonl > data/preprocessing_table/training-all-feats-customer.tsv
paste <(echo "review_idx") <(echo "pred") > data/preprocessing_table/$MODE-feats-pred-score.tsv
perl -pe "s/^.*\"review_idx\":([0-9\.]+).*\"pred\":([\-0-9\.]+).*$/\1\t\2/" $PREDICT_RESULT >> data/preprocessing_table/$MODE-feats-pred-score.tsv

python src/prepare_table.py -review data/preprocessing_table/training-all-feats-review.tsv -product data/preprocessing_table/training-all-feats-product.tsv -customer data/preprocessing_table/training-all-feats-customer.tsv -pred_score data/preprocessing_table/${MODE}-feats-pred-score.tsv -outfile $OUTFILE --mode ${MODE}
#python src/train-regression-model.py -infile data/preprocessing_table/training-regression-feats-for-training.tsv
