import numpy as np
from coweighed_semantic_convolutional_feature_38p.normalizer import normalize_vector



def get_b_for_an_image(Omega, Height, Width, num_channels, p = 2):


    b=np.zeros(num_channels)
    
    for k in range( 0, num_channels ):
        b[k]=(Omega[k]/(Height*Width))**p
        
    return b



def calculate_channel_weighting_vector(Omega, Height, Width, num_channels, p = 2, epsilon=1e-6):

    b_values = get_b_for_an_image(Omega, Height, Width, num_channels, p)
    
    B = np.log(((num_channels*epsilon) + np.sum(b_values, axis=0)) / (b_values + epsilon))
    
    return B

def get_beta_for_an_image(Omega, Height, Width, num_channels, p = 2, epsilon=1e-6):

    channel_weighting_vector = calculate_channel_weighting_vector(Omega, Height, Width, num_channels, p, epsilon)

    Omega = np.array(Omega,dtype='float32')

    return channel_weighting_vector * Omega

def get_normalized_beta_for_an_image(Omega, Height, Width, num_channels, p = 2, epsilon=1e-6):

    beta_values = get_beta_for_an_image(Omega, Height, Width, num_channels, p, epsilon)

    normalized_beta_values = normalize_vector(beta_values)

    return normalized_beta_values