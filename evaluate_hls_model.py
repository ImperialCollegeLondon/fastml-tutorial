import os
import sys
import numpy as np
import hls4ml

# Load project name
PROJECT_NAME = sys.argv[1]
print("Project name:", PROJECT_NAME)

# Load test data
X_test = np.load(os.path.join(PROJECT_NAME, "X_test.npy"))

# Load model from project directory
hls_model = hls4ml.converters.link_existing_project(PROJECT_NAME)
print("--> Linked existing hls4ml project")

# Compile hls4ml model
hls_model.compile()
print("--> HLS model compiled")

# Evaluate hls_model on test data
y_hls_pred_probs = hls_model.predict(X_test)
print("--> HLS model predictions obtained")

# Save hls model prediction to project directory
np.save(os.path.join(PROJECT_NAME, "y_hls_pred_probs.npy"), y_hls_pred_probs)
print("--> HLS model predictions saved")