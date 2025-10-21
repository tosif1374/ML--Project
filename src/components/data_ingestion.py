import os
import sys
from src.exception import CustomException
from src.logger import logging
import pandas as pd

from sklearn.model_selection import train_test_split
from dataclasses import dataclass

from src.components.data_transformation import DataTransformation
from src.components.data_transformation import DataTransformationConfig

from src.components.model_trainer import ModelTrainerConfig
from src.components.model_trainer import ModelTrainer

@dataclass
class DataIngestionConfig:
    train_data_path: str=os.path.join('artifacts',"train.csv")
    test_data_path: str=os.path.join('artifacts',"test.csv")
    raw_data_path: str=os.path.join('artifacts',"data.csv")

class DataIngestion:
    def __init__(self):
        self.ingestion_config=DataIngestionConfig()

    def initiate_data_ingestion(self):
        logging.info("Entered the data ingestion method or component")
        try:
            # FIX 1: Use raw string for file path
            csv_path = r'notebook\study.csv'
            logging.info(f"Attempting to read CSV from: {csv_path}")
            
            # FIX 2: Check if file exists first
            if not os.path.exists(csv_path):
                logging.error(f"CSV file not found at: {csv_path}")
                # Try to find the file
                project_root = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
                logging.info(f"Project root: {project_root}")
                raise FileNotFoundError(f"CSV file not found at: {csv_path}")
            
            df=pd.read_csv(csv_path)
            logging.info('Read the dataset as dataframe')
            logging.info(f"Dataset shape: {df.shape}")

            os.makedirs(os.path.dirname(self.ingestion_config.train_data_path),exist_ok=True)

            df.to_csv(self.ingestion_config.raw_data_path,index=False,header=True)
            logging.info(f"Saved raw data to: {self.ingestion_config.raw_data_path}")

            logging.info("Train test split initiated")
            train_set,test_set=train_test_split(df,test_size=0.2,random_state=42)

            train_set.to_csv(self.ingestion_config.train_data_path,index=False,header=True)
            test_set.to_csv(self.ingestion_config.test_data_path,index=False,header=True)
            
            logging.info(f"Saved train data to: {self.ingestion_config.train_data_path}")
            logging.info(f"Saved test data to: {self.ingestion_config.test_data_path}")

            logging.info("Ingestion of the data is completed")

            return(
                self.ingestion_config.train_data_path,
                self.ingestion_config.test_data_path
            )
        except Exception as e:
            # FIX 3: Add proper error logging
            logging.error(f"Exception occurred at data ingestion stage: {str(e)}")
            raise CustomException(e,sys)
        
if __name__=="__main__":
    try:
        logging.info("=== Starting data ingestion pipeline ===")
        
        obj=DataIngestion()
        train_data,test_data=obj.initiate_data_ingestion()
        logging.info(f"Data ingestion successful: {train_data}, {test_data}")

        data_transformation=DataTransformation()
        train_arr,test_arr,_=data_transformation.initiate_data_transformation(train_data,test_data)
        logging.info("Data transformation completed")

        modeltrainer=ModelTrainer()
        result = modeltrainer.initiate_model_trainer(train_arr,test_arr)
        logging.info(f"Model training result: {result}")
        
    except Exception as e:
        logging.error(f"Pipeline failed: {str(e)}")
        print(f"ERROR: {e}")