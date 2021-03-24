import argparse
from sklearn.model_selection import train_test_split
from get_data import read_params
import pandas as pd

def split_and_saved_data(config_path):
    config=read_params(config_path)
    test_data_path=config['split_data']['test_path']
    train_data_path=config['split_data']['train_path']
    raw_dataset_csv=config['load_data']['raw_dataset_csv']
    split_ratio=config['split_data']['test_size']
    random_state=config['base']['random_state']
    dataset=pd.read_csv(raw_dataset_csv)
    train_data,test_data=train_test_split(dataset,test_size=split_ratio,random_state=random_state)
    train_data.to_csv(train_data_path,index=False,sep=",")
    test_data.to_csv(test_data_path,index=False,sep=",")



if __name__=="__main__":
    args = argparse.ArgumentParser()
    args.add_argument("--config", default="E:/simple_app/params.yaml")
    parsed_args = args.parse_args()
    split_and_saved_data(config_path=parsed_args.config)