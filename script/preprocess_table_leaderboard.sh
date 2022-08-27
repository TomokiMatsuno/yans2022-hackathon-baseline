mkdir -p ./data/preprocessing_table/

MODE=training-regression
MODE=leader_board
PREDICT_RESULT=/home/tomoki/experiments/yans2022/yans2022-hackathon-baseline/data/predict/predict_helpful_votes/xlm-roberta-base-jaen/leader_board.jsonl
OUTFILE=data/preprocessing_table/leader_board-feats-for-training.xlm-roberta-jaen.tsv
PREDICT_RESULT=/home/tomoki/experiments/yans2022/pred_results/leader_board_predict_xlm-roberta_jaen_3epochs.jsonl
OUTFILE=/home/tomoki/experiments/yans2022/pred_results/leader_board_predict_xlm-roberta_jaen_3epochs.tsv

python src/prepare_review.py < <(cat data/dataset_shared_initial/{training-all,leader_board}.jsonl) > data/preprocessing_table/all-feats-review.tsv
python src/prepare_product.py < <(cat data/dataset_shared_initial/{training-all,leader_board}.jsonl) > data/preprocessing_table/all-feats-product.tsv
python src/prepare_customer.py < <(cat data/dataset_shared_initial/{training-all,leader_board}.jsonl) > data/preprocessing_table/all-feats-customer.tsv
echo -e "review_idx\tpred" > data/preprocessing_table/$MODE-feats-pred-score.tsv
perl -pe "s/^.*\"review_idx\":([0-9\.]+).*\"pred\":([\-0-9\.]+).*$/\1\t\2/" $PREDICT_RESULT >> data/preprocessing_table/$MODE-feats-pred-score.tsv

python src/prepare_table.py -review data/preprocessing_table/all-feats-review.tsv -product data/preprocessing_table/all-feats-product.tsv -customer data/preprocessing_table/all-feats-customer.tsv -pred_score data/preprocessing_table/${MODE}-feats-pred-score.tsv -outfile $OUTFILE --mode ${MODE}
#python src/predict-regression-model.py -infile data/preprocessing_table/leader_board-feats-for-training.tsv -pred_result_file leader_board_pred_0.tsv -model_file output_training/model_fold0.pkl
#python src/replace_pred_score.py -pred_score_file leader_board_pred_0.tsv  -old_submit_file data/evaluation/predict_helpful_votes/cl-tohoku_bert-base-japanese_lr1e-5/submit_leader_board.jsonl -new_submit_file submit_leader_board-model0.jsonl
