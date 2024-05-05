import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

threshold = 2

def preprocess_data(data):
    # Drop columns
    data = data.drop(columns=['col1', 'col2'])
    
    # Handle missing data
    data = data.fillna(method='ffill')
    
    # Handle noisy data
    z_scores = np.abs((data - data.mean()) / data.std())
    data_clean = data.mask(z_scores > threshold, data.median(axis=0), axis=1)

    return data_clean

def sigmoid(z):
    return 1 / (1 + np.exp(-z))

def compute_gradient(X, y, theta):
    m = len(y)
    predictions = sigmoid(np.dot(X, theta))
    error = predictions - y
    gradient = np.dot(X.T, error) / m
    return gradient

def logistic_regression(X, y, learning_rate=0.01, num_iterations=100):
    # Initialize parameters
    theta = np.zeros(X.shape[1])
    
    for _ in range(num_iterations):
        # Compute gradient
        gradient = compute_gradient(X, y, theta)
        
        # Update parameters using gradient descent
        theta -= learning_rate * gradient
    
    return theta

def plot_precision_recall_curve(precision, recall):
    plt.plot(recall, precision, marker='.')
    plt.xlabel('Recall')
    plt.ylabel('Precision')
    plt.title('Precision-Recall Curve')
    plt.show()

if __name__ == "__main__":
    # Load data
    data = pd.read_csv('data.csv')
    
    # Separate features (X) and labels (y)
    X = data.drop(columns=['target_column']) 
    y = data['target_column']  
    
    # Preprocess features
    X = preprocess_data(X)
    
    # Convert to numpy arrays
    X = X.values
    y = y.values.ravel()  # Flatten y
    
    # Add bias term to X
    X = np.hstack((np.ones((X.shape[0], 1)), X))
    
    # Train logistic regression model
    theta = logistic_regression(X, y)
    
    # Performance results
    # Load precision and recall values
    precision = [0.8, 0.7, 0.6, 0.5]
    recall = [0.2, 0.4, 0.6, 0.8]
    
    # Plot precision-recall curve
    plot_precision_recall_curve(precision, recall)
