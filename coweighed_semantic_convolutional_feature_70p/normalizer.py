import numpy as np

def normalize_vector(vector):
    norm = np.sum(np.abs(vector))  # L1 norm (sum of absolute values)
    if norm == 0:
        return vector
    return vector / norm

# Normalize the aggregated features
def normalize_features(features):
    return np.array([normalize_vector(feature) for feature in features])
