import numpy as np
import cv2
from coweighed_semantic_convolutional_feature_before_pca.Extract_Feature_Map import get_feature_map
from scipy.ndimage import label, find_objects


def extract_threshold(spatial_matrix):
    flattened = spatial_matrix.flatten()
    sorted_array = np.sort(flattened)
    median = np.median(sorted_array)
    return median

def extract_mask_(spatial_matrix):
    tm = extract_threshold(spatial_matrix)
    spatial_mask_ = np.where(spatial_matrix < tm, 0, 1)
    return spatial_mask_

def extract_mask__(spatial_mask_):

    labeled_matrix, num_features = label(spatial_mask_)
    for i in range(1, num_features + 1):
    
        component_slice = find_objects(labeled_matrix == i)[0]

        component = labeled_matrix[component_slice] == i
    
    
        if np.sum(component) < 4:
        
            labeled_matrix[component_slice][component] = 0

    spatial_mask__ = np.where(labeled_matrix > 0, 1, 0)

    return spatial_mask__

def extract_mask(spatial_mask__):

    spatial_mask__ = spatial_mask__.astype(np.uint8)

    contours, _ = cv2.findContours(spatial_mask__, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)


    hull = [cv2.convexHull(c) for c in contours]


    convex_hull_matrix = np.zeros_like(spatial_mask__)


    cv2.drawContours(convex_hull_matrix, hull, -1, 1, thickness=-1)  # -1 to fill the hull with 1's

    return convex_hull_matrix

def extract_mask_for_an_image(desired_layer_output,max_frequent_channel):
    
    max_frequent_channel_feature_map = get_feature_map(desired_layer_output, max_frequent_channel)

    I_ = extract_mask_(max_frequent_channel_feature_map)
    I__ = extract_mask__(I_)
    I = extract_mask(I__)
    return I