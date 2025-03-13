import numpy as np
from coweighed_semantic_convolutional_feature_38p.Extract_Feature_Map import get_channel_feature_map

def get_Spatial_Weight_for_an_image(num_channels, desired_layer_output, I):
    
    
    

    S_i = np.zeros_like(I)

    for channel_index in range( 0, num_channels ):

        X = get_channel_feature_map(desired_layer_output,channel_index)
        #X = np.dot(X,I)
        X = X * I
        S_i = S_i + X
        
    return S_i

def get_Alpha(fraction,size):
    
    return int(fraction*size)

def get_Cetroid(alpha,s_):
    
    flat_indices = np.argsort(s_.ravel())[::-1]  # Sort values in descending order
    top_alpha_indices = flat_indices[:alpha]  # Get indices of top alpha values
    top_alpha_coords = np.array(np.unravel_index(top_alpha_indices, s_.shape)).T
    centroid = np.mean(top_alpha_coords, axis=0)  # Average of the top alpha coordinates
    return centroid

def get_Sigma(rightY,bottomX,centroid):
#     x, y = np.meshgrid(np.linspace(0, rightY-1, rightY),
#                    np.linspace(0, bottomX-1, bottomX))

    # Standard deviation for the Gaussian

    top_boundary_distance = centroid[0]  # Distance to the top boundary
    bottom_boundary_distance = bottomX - centroid[0]  # Distance to the bottom boundary
    left_boundary_distance = centroid[1]  # Distance to the left boundary
    right_boundary_distance = rightY - centroid[1]
    max_distance = max(top_boundary_distance, bottom_boundary_distance, left_boundary_distance, right_boundary_distance)

    sigma = max_distance/2
    return sigma

def get_Weight_Function_for_an_image(num_channels, desired_layer_output, I, alpha_fraction = 0.1 ):
    
    #S = []
    
    
    #S_ = get_Spacial_Weight(pooled_values,max_frequent_channel)
    
    
    
        
    S_ = get_Spatial_Weight_for_an_image(num_channels, desired_layer_output, I)
    alpha = get_Alpha(alpha_fraction, S_.size)
    rightY = S_.shape[1]
    bottomX = S_.shape[0]
    centroid = get_Cetroid(alpha,S_)
    sigma = get_Sigma(rightY,bottomX,centroid)
    x, y = np.meshgrid(np.linspace(0, rightY-1, rightY),
                   np.linspace(0, bottomX-1, bottomX))
    gaussian = (1 / (2 * np.pi * sigma**2)) * np.exp(-((x - centroid[1])**2 + (y - centroid[0])**2) / (2 * sigma**2))
    
        
    return gaussian

def get_Omega_for_an_image(num_channels, desired_layer_output, I, alpha_fraction = 0.1):
    

    omega = []
    
    
    S = get_Weight_Function_for_an_image(num_channels, desired_layer_output, I, alpha_fraction)
        
    for channel_index in range( 0, num_channels ):
            
        X = get_channel_feature_map(desired_layer_output,channel_index)
        X = I * S * X
        omega.append( np.sum(X) )
            
        
        
    return omega