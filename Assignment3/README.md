## Logistic Regression

# Task 1: Environment Setup

For this task, I set up a Docker container-based development environment. I downloaded the dataset from Kaggle and stored it in a location accessible from my application code.

# Task 2: Data Preprocessing

Dropping Columns

I dropped some columns that I deemed unnecessary for predicting the Click Through Rate (CTR) of ads.
Handling Missing Data

I addressed missing data by either imputing values or dropping rows/columns with missing data, depending on the context.
Handling Noisy Data

I applied techniques such as outlier detection and removal to handle noisy data.
Data Transformation

I transformed categorical variables into numerical representations using techniques like one-hot encoding.
Orchestration with Dagster

All data preprocessing transformations were orchestrated using Dagster to ensure reproducibility and traceability.

# Task 3: Logistic Regression

Logistic Regression Implementation

I implemented logistic regression using Stochastic Gradient Descent (SGD) from scratch.
Equations of the Gradient

The gradient of the logistic loss function with respect to the parameters is calculated as follows: 

grad = np.dot(X.T, (predictions - y)) / m

Explanation of Processing

    Initialize the weights and biases.
    Compute the logits using the dot product of features and weights.
    Apply the sigmoid function to the logits to get the predictions.
    Compute the loss using the logistic loss function.
    Compute the gradient of the loss with respect to the parameters.
    Update the weights and biases using gradient descent.
    Repeat steps 2-6 until convergence or a predefined number of iterations.

Performance Enhancements

To improve performance, I applied techniques such as mini-batch gradient descent, regularization, and feature scaling.

# Task 4: Performance Results

Precision vs Recall Curve

I plotted the final precision vs recall curve of the classifier.
Tradeoff Explanation

The precision-recall curve illustrates the tradeoff between precision (the ability of the classifier not to label a negative sample as positive) and recall (the ability of the classifier to find all positive samples).

The shape of the curve shows how the precision and recall change with varying classification thresholds. Typically, as the threshold decreases, recall increases while precision decreases, resulting in a convex curve. The point of the curve represents the optimal balance between precision and recall.

Overall, the precision-recall curve provides valuable insights into the performance of the classifier across different thresholds.