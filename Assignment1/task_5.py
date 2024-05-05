import pandas as pd

# install the dataset first

dataset = pd.read_csv('bayesian_regression_house_price_prediction.csv')
dataset.to_parquet('dataset.parquet')

from datasets import DatasetBuilder

dataset_builder = DatasetBuilder('assignment')
dataset_builder.add_parquet_files('dataset.parquet')#change it
dataset_builder.finalize("/huggingface_repo")#change it

# 5.3

import duckdb

con = duckdb.connect()

df = duckdb.read_parquet('dataset.parquet')
con.register('house_price_data', df)


con.write('house_price.db')
con.close()

