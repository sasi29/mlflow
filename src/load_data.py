from get_data import read_params,get_data
import argparse

def load_and_save(config_path):
    config= read_params(config_path)
    data= get_data(config_path)
    new_cols= [cols.replace(" ","_") for cols in data.columns]
    raw_dataset_csv=config['load_data']['raw_dataset_csv']
    data.to_csv(raw_dataset_csv,index=False, header=new_cols)

if __name__=="__main__":
    args= argparse.ArgumentParser()
    args.add_argument("--config",default="E:/simple_app/params.yaml")
    parsed_args=args.parse_args()
    load_and_save(config_path=parsed_args.config)