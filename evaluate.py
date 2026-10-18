import os

import matplotlib.pyplot as plt
import mlflow
import numpy as np
import pandas as pd
import torch
from torch.utils.data import random_split

DATA_URL = "https://raw.githubusercontent.com/mlflow/mlflow/master/tests/datasets/winequality-white.csv"

# Load data exactly as in train.ipynb
data = pd.read_csv(DATA_URL, header=0, delimiter=";")
features = data.drop("quality", axis=1).astype(np.float32)
labels = data["quality"].values

# Recreate the same 75/25 split (same seed, same lengths -> same indices as training)
generator = torch.Generator().manual_seed(42)
_, test_split = random_split(range(len(data)), [0.75, 0.25], generator=generator)
test_idx = list(test_split.indices)

X_test = features.iloc[test_idx]
y_test = labels[test_idx]

# Load the same model the API serves
model = mlflow.pyfunc.load_model("model_artifacts")
y_pred = np.asarray(model.predict(X_test)).ravel()

rmse = np.sqrt(np.mean((y_pred - y_test) ** 2))
mae = np.mean(np.abs(y_pred - y_test))
baseline_rmse = np.sqrt(np.mean((y_test.mean() - y_test) ** 2))
print(f"Test samples: {len(y_test)}")
print(f"Test RMSE: {rmse:.3f}   Test MAE: {mae:.3f}")
print(f"Baseline RMSE (always predict the mean): {baseline_rmse:.3f}")

# Quality is an integer score, so show the spread of predictions for each true score
scores = sorted(np.unique(y_test))
groups = [y_pred[y_test == s] for s in scores]

fig, ax = plt.subplots(figsize=(7, 5))
ax.boxplot(groups, positions=scores, widths=0.6)
ax.plot([min(scores), max(scores)], [min(scores), max(scores)], "--", label="Perfect prediction")
ax.set_xlabel("Actual quality")
ax.set_ylabel("Predicted quality")
ax.set_title(f"Test set: predicted vs actual (RMSE {rmse:.2f})")
ax.legend()
fig.tight_layout()

os.makedirs("images", exist_ok=True)
fig.savefig("images/pred_vs_actual.png", dpi=150)
print("Saved images/pred_vs_actual.png")