FORMAT=$1
GOLD_FILE=$2
PREDICTION_FILE=$3
java -cp bc5cdr_eval.jar ncbi.bc5cdr_eval.Evaluate relation CID $FORMAT $GOLD_FILE $PREDICTION_FILE | grep -v INFO
# java -cp bc5cdr_eval.jar ncbi.bc5cdr_eval.Evaluate relation CID $FORMAT $GOLD_FILE $PREDICTION_FILE

