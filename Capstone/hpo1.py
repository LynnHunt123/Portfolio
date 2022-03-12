import numpy as np
import pandas as pd
import argparse
import os
import logging
import sys
import json
import xgboost as xgb
import pickle as pkl
from sklearn.model_selection import TimeSeriesSplit, cross_validate
from sklearn.metrics import mean_squared_error, make_scorer, accuracy_score, precision_score, f1_score

logger=logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
logger.addHandler(logging.StreamHandler(sys.stdout))

# Data split
# Since AWS Sagemaker using xgb uri cannot achieve time series split (not that I can find material of), we will split the data in here. 

# Load data from train and validation

def evaluate_model(model, X, y, train_size = 40):
    cv = TimeSeriesSplit(
                       n_splits=len(X)-args.train_size,
                       max_train_size= args.train_size
                      )
    scorer = make_scorer(precision_score, greater_is_better=True, squared=False)
    
    return cross_validate(model, X, y, cv=cv, 
                                  # scoring=scorer, 
                                  n_jobs=-1)['test_score']

def main():
    load_data = "csv"

    if load_data == 'csv':
        data = pd.read_csv(os.path.join(args.train, "train.csv"), 
                              header = None) # this should contain all data. 
        X = data.iloc[:,1:]
        logger.info("Logging X head")
        logger.info(X.head(5))
        y = data.iloc[:,0]
        logger.info("Logging y")
        logger.info(y)
        data = xgb.DMatrix(data = X, label = y)

    elif load_data == "dmatrix":
        data = xgb.DMatrix(os.path.join(args.train, "train.csv")+'?format=csv&label_column=0')

    logger.info(f"Data loaded. Loading method is {load_data}.")

    model = xgb.XGBClassifier(objective = args.objective, 
                             n_estimators = args.num_rounds, 
                             booster = 'gbtree', 
                             learning_rate = args.eta, 
                             use_label_encoder = False, 
                             eval_metric = "error", 
                             gamma = args.gamma, 
                             max_depth = args.max_depth, 
                             min_child_weight = 7,
                             reg_alpha = args.alpha)
    
    logger.info("Model defined. Evaluating using cross-validation. ")

    accuracy = evaluate_model(model, X, y).mean()
    
    logger.info(f"[0]#011validation-auc:"+str(accuracy))
#     logger.info(f"validation-auc:{accuracy}")
#     [0]#011 train-auc:0.988

# Note: if using sagemaker.XGBoost() estimator, can also extract booster from fitted model. 

# def model_fn(model_dir):
#     """Deserialize and return fitted model.
#     Note that this should have the same name as the serialized model in the _xgb_train method
#     """
#     model_file = "xgboost-model"
#     booster = pkl.load(open(os.path.join(model_dir, model_file), "rb"))
#     return booster

if __name__=='__main__':
    parser=argparse.ArgumentParser()
    
    # add model parser arguments
    parser.add_argument('--train_size', type=int, default = 40)
    parser.add_argument('--num_rounds', type=int, default = 200)
    parser.add_argument('--early_stopping_rounds', type=int, default = 50)
    parser.add_argument('--max_depth', type=int, default=2)
    parser.add_argument('--eta', type=float, default=0.01)
    parser.add_argument('--alpha', type=float, default = 0.2)
#     parser.add_argument('--lambda', type=float, default = 1)
    parser.add_argument('--gamma', type=float, default = 0.001)
    parser.add_argument('--objective', type=str, default='binary:logistic')
    
    # add sagemaker parser arguments
    parser.add_argument('--model_dir', type=str, default=os.environ.get('SM_MODEL_DIR'))
    parser.add_argument('--output_dir', type=str, default=os.environ['SM_OUTPUT_DATA_DIR'])
    parser.add_argument('--train', type=str, default=os.environ['SM_CHANNEL_TRAIN'])
#     parser.add_argument('--validation', type=str, default=os.environ['SM_CHANNEL_ ATION'])
    
    args = parser.parse_args()
    
#     X, y = load_data(args.train, args.validation)
    
    main()
    
#     model_location = args.model_dir + '/xgboost-model'
#     pkl.dump(bst, open(model_location, 'wb'))
#     logging.info("Stored trained model at {}".format(model_location))