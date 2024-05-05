
import pandas as pd
import numpy as np

threshold = 3

def preprocess_data(data):
    # Drop columns
    data = data.drop(columns=['col1', 'col2'])
    
    # Handle missing data
    data = data.fillna(method='ffill')
    
    z_scores = np.abs((data - data.mean()) / data.std())

    # Replace outliers with median values
    data_clean = data.mask(z_scores > threshold, data.median(axis=0), axis=1)

    return data_clean
if __name__ == "__main__":
    # Load data
    data = pd.read_csv('data.csv')
    
    # Preprocess data
    processed_data = preprocess_data(data)
