from src.constants import *
from src.config.configuration import *
import os,sys
import opendatasets as od
import pandas as pd
import numpy as np
import shutil
from sklearn.model_selection import train_test_split
from dataclasses import dataclass
from src.logger import logging
from src.exception import CustomException
from src.components.data_transformation import Distribution_Outliers
@dataclass
class DataInjectionConfig:
    raw_train_file_path:str= RAW_TRAIN_DATASET_PATH
    raw_test_file_path:str=RAW_TEST_DATASET_PATH
    sample_submission:str=RAW_SS_DATASET_PATH
    raw_file_path:str=RAW_FILE_PATH
    train_file_path:str=TRAIN_FILE_PATH
    test_file_path:str=TEST_FILE_PATH
    api_username="kalehariprasad"
    api_key="9a694c8c79d80c1dff52f1e065905992"

class DataInjection:
    def __init__(self):
        self.data_injection_config=DataInjectionConfig
        


    def Initiate_data_injection(self):
        """
        this method is Resposible for injecting data from local machine
        to current working directory
        """
        try:
            logging.info('data injection started  with existing dataset')
            df=pd.read_csv(CURRENT_DATA_PATH)
            os.makedirs(os.path.dirname(self.data_injection_config.raw_file_path),exist_ok=True)
            df.to_csv(self.data_injection_config.raw_file_path)
            logging.info('splitting train and test data staretd')
            train_set,test_set=train_test_split(df,test_size=0.20,random_state=42)
            logging.info('splitting train and test data compleeted')
            os.makedirs(os.path.dirname(self.data_injection_config.train_file_path),exist_ok=True)
            train_set.to_csv(self.data_injection_config.train_file_path)
            logging.info(f'train head{train_set.head()}')
            logging.info('train data stored in artifacts /data_injection /injected data/train_data')
            os.makedirs(os.path.dirname(self.data_injection_config.test_file_path),exist_ok=True)
            test_set.to_csv(self.data_injection_config.test_file_path)
            test_set.head()
            logging.info('train data stored in artifacts /data_injection /injected data/test_data')

            return train_set, test_set
    
     

        except Exception as e:
            raise CustomException(e, sys)



        
if __name__ == "__main__":
    obj = DataInjection()
    out_liers=Distribution_Outliers()
    train_path, test_path=obj.Initiate_data_injection() 
    if isinstance(train_path, pd.DataFrame):

        out_liers.detect_and_visualize_outliers(train_path)
    else:
        print("train_data is not a DataFrame")

    if isinstance(test_path, pd.DataFrame):

        out_liers.detect_and_visualize_outliers(test_path)
    else:
        print("test_data is not a DataFrame")
    
    train_path,test_path=out_liers.outliers_removal(train_path),out_liers.outliers_removal(test_path)
   