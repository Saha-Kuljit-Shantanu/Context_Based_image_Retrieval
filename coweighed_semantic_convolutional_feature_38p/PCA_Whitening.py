import numpy as np
from coweighed_semantic_convolutional_feature_38p.normalizer import normalize_vector

def apply_pca_whitening(pca_transformation_matrix,pca_explained_variance,feature_mean, aggregated_features):

    aggregated_features_centered = aggregated_features - feature_mean.T
    # print(aggregated_features_centered.shape)
    transformed_features =  np.dot(pca_transformation_matrix, aggregated_features_centered.T)
    # print(transformed_features.shape)
    whitened_features = transformed_features/ np.sqrt(pca_explained_variance)
    # print(whitened_features.shape)
    return normalize_vector( whitened_features.flatten() )