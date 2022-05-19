import json
import numpy as np
import pickle
from sklearn.linear_model import LogisticRegression
from sklearn import datasets

# Import and normalize data
X_digits, y_digits = datasets.load_digits(return_X_y=True)
X_digits = X_digits / X_digits.max()

n_samples = len(X_digits)

# Split data into training and test sets
X_train = X_digits[: int(0.9 * n_samples)]
y_train = y_digits[: int(0.9 * n_samples)]
X_test = X_digits[int(0.9 * n_samples) :]
y_test = y_digits[int(0.9 * n_samples) :]

# Train Model
logistic = LogisticRegression(max_iter=1000)
print(
    "LogisticRegression mean accuracy score: %f"
    % logistic.fit(X_train, y_train).score(X_test, y_test)
)

# save trained model
with open("weights/model_latest.pkl", "wb") as file:
    pickle.dump(logistic, file)

# Save small sample input to use for testing later
sample = X_test[:5].tolist()
with open("data/digits_sample.json", 'w') as out:
    json.dump(sample, out)