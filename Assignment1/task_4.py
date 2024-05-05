import pandas as pd
from dagster import pipeline, solid, ModeDefinition, execute_pipeline, OutputDefinition, Output
# Using bayesian_regression_house_price_prediction dataset from Kaggle make sure to install it first for program execution
# Define your solid functions for data transformation
@solid(output_defs=[OutputDefinition(pd.DataFrame)])
def read_raw_data(context):
    
    raw_data = pd.read_csv('bayesian_regression_house_price_prediction.csv')
    return raw_data

@solid(output_defs=[OutputDefinition(pd.DataFrame)])
def clean_data(context, raw_data: pd.DataFrame):
    
    cleaned_data = raw_data.dropna() 
    return cleaned_data

@solid(output_defs=[OutputDefinition(pd.DataFrame)])
def preprocess_data(context, cleaned_data: pd.DataFrame):
    
    preprocessed_data = cleaned_data.copy() 
    
    numerical_features = ['housing_median_age', 'total_rooms', 'total_bedrooms', 'population', 'households', 'median_income']
    preprocessed_data[numerical_features] = (preprocessed_data[numerical_features] - preprocessed_data[numerical_features].mean()) / preprocessed_data[numerical_features].std()
    return preprocessed_data
@solid(output_defs=[OutputDefinition(pd.DataFrame)])
def feature_engineering(context, preprocessed_data: pd.DataFrame):
    
    engineered_data = preprocessed_data.copy()
    return engineered_data

@solid(output_defs=[OutputDefinition(pd.DataFrame)])
def prepare_training_data(context, engineered_data: pd.DataFrame):
    
    X = engineered_data.drop(columns=['median_house_value'])
    y = engineered_data['median_house_value']
    return X, y

# Define the pipeline
@pipeline(mode_defs=[ModeDefinition(name="default", resource_defs={})])
def house_price_prediction_pipeline():
    raw_data = read_raw_data()
    cleaned_data = clean_data(raw_data)
    preprocessed_data = preprocess_data(cleaned_data)
    engineered_data = feature_engineering(preprocessed_data)
    training_data = prepare_training_data(engineered_data)


if __name__ == "__main__":
    result = execute_pipeline(house_price_prediction_pipeline)
