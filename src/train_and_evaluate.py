import os
import warnings
import sys
import pandas as pd
import numpy as np
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
from sklearn.model_selection import train_test_split
from sklearn.linear_model import ElasticNet
from urllib.parse import  urlparse
from get_data import  read_params
import argparse,joblib,json

def eval_metrics(test_y,prediction):
    rmse=mean_squared_error(test_y,prediction)
    r2score=r2_score(test_y,prediction)
    mae_score=mean_absolute_error(test_y,prediction)
    return rmse,mae_score,r2score

def train_and_evaluate(config_path):
    config=read_params(config_path)
    train_data_path=config['split_data']['train_path']
    test_data_path=config['split_data']['test_path']
    random_state=config['base']['random_state']
    model_dir=config['model_dir']
    alpha=config['estimators']['ElasticNet']['params']['alpha']
    l1_ration=config['estimators']['ElasticNet']['params']['l1_ratio']
    target=[config['base']['target_col']]
    train=pd.read_csv(train_data_path)
    test=pd.read_csv(test_data_path)
    train_x=train.drop(target,axis=1)
    test_x=test.drop(target,axis=1)
    train_y=train[target]
    test_y=test[target]
    lr=ElasticNet(alpha=alpha,l1_ratio=l1_ration,random_state=random_state)
    lr.fit(train_x,train_y)
    prediction=lr.predict(test_x)
    (rmse,mae,r2score)=eval_metrics(test_y,prediction)
    print("ElasticNet model",(alpha,l1_ration))
    print("RMSE:",rmse)
    print("mae:",mae)
    print("r2_score:",r2score)
    scores_file=config['reports']['scores']
    params_file=config['reports']['params']
    with open(scores_file,"w") as f:
        scores={
            "rmse":rmse,
            "mae":mae,
            "r2_score":r2score
        }
        json.dump(scores,f,indent=4)
    with open(params_file,"w") as f:
        params={
            "alpha":alpha,
            "l1_ratio":l1_ration,
        }
        json.dump(params,f,indent=4)
    os.makedirs(model_dir,exist_ok=True)
    model_path=os.path.join(model_dir,"model.joblib")
    joblib.dump(lr,model_path)

if __name__=="__main__":
    args = argparse.ArgumentParser()
    args.add_argument("--config", default="E:/simple_app/params.yaml")
    parsed_args = args.parse_args()
    train_and_evaluate(config_path=parsed_args.config)
