from PIL import Image


import keras,os,cv2

from tensorflow.keras.models import Model
from keras.applications import vgg16
from collections import Counter
from coweighed_semantic_convolutional_feature_70p.Spacial_Matrix_Determination import extract_mask_for_an_image
from coweighed_semantic_convolutional_feature_70p.Spacial_Weight_Determination import get_Omega_for_an_image
from coweighed_semantic_convolutional_feature_70p.Channel_Weight_Determination import get_normalized_beta_for_an_image
from coweighed_semantic_convolutional_feature_70p.PCA_Whitening import apply_pca_whitening
import numpy as np
import pandas as pd
# import seaborn as sb
# import matplotlib.pyplot as plt



def make_model(model,layer):
    return Model(inputs=model.input, outputs=model.get_layer(layer).output)

def make_prediction(desired_layer_output_model,image):
    return desired_layer_output_model.predict(image)

def load_image(image_filename) :

    image = []
    
    img = cv2.imread(image_filename)
    img = cv2.resize(img, (224,224) )
  
    image.append(img)
    image = np.array(image)

    return image



# def get_pool(desired_layer_output):
#     return np.sum(desired_layer_output, axis=(1, 2))



def extract_feature_vector(image_filename, dataset) :
    
    vgg = vgg16.VGG16(weights = 'imagenet', 
                 include_top = False, 
                 input_shape = (224, 224, 3))

    print(vgg.summary())

    if dataset == "Oxford5k" :
        param_file_path = 'coweighed_semantic_convolutional_feature_70p\\Oxford5k\\parameters.xlsx'
        pca_transformation_matrix_path = 'coweighed_semantic_convolutional_feature_70p\\Oxford5k\\pca_transformation_matrix.csv'
        pca_explained_variance_path = 'coweighed_semantic_convolutional_feature_70p\\Oxford5k\\pca_explained_variance.csv'
        feature_mean_path = 'coweighed_semantic_convolutional_feature_70p\\Oxford5k\\feature_mean.csv'
        channel_frequency_path = 'coweighed_semantic_convolutional_feature_70p\\Oxford5k\\channel_frequency_map.csv'

    if dataset == "Paris6k" :
        param_file_path = 'coweighed_semantic_convolutional_feature_70p\\Paris6k\\parameters.xlsx'
        pca_transformation_matrix_path = 'coweighed_semantic_convolutional_feature_70p\\Paris6k\\pca_transformation_matrix.csv'
        pca_explained_variance_path = 'coweighed_semantic_convolutional_feature_70p\\Paris6k\\pca_explained_variance.csv'
        feature_mean_path = 'coweighed_semantic_convolutional_feature_70p\\Paris6k\\feature_mean.csv'
        channel_frequency_path = 'coweighed_semantic_convolutional_feature_70p\\Paris6k\\channel_frequency_map.csv'


    df = pd.read_excel(param_file_path)

    parameters = dict(zip(df['Parameters'], df['Value']))

    vgg_layer = parameters['Layer']  ##### Take from file


    # num_images = parameters['Number of Images']
    Height = parameters['Height']  ##### Take from file
    Width = parameters['Width']  ##### Take from file
    num_channels = parameters['Channel']  ##### Take from file


    desired_layer_output_model = make_model(vgg,vgg_layer) # chose blockf_conv3 as used in the paper 

   
    image = load_image(image_filename)

   
    desired_layer_output = make_prediction(desired_layer_output_model,image)

    
    # Read the CSV file into a DataFrame
    df_read = pd.read_csv(channel_frequency_path)

    # Convert the DataFrame back to a list of tuples
    channel_frequency_map = list(df_read.itertuples(index=False, name=None))



    zero_fmap = np.zeros((Height, Width))

    
    alpha_fraction = parameters['Alpha Fraction']  ##### Take from file

    I = extract_mask_for_an_image(desired_layer_output, channel_frequency_map, zero_fmap)

    omega = get_Omega_for_an_image(num_channels, desired_layer_output, I, alpha_fraction)

    p = parameters['p']  ##### Take from file

    epsilon = parameters['epsilon']   ##### Take from file

    num_features = parameters['Number of reduced features']

    beta = get_normalized_beta_for_an_image(omega, Height, Width, num_channels, p, epsilon)

    pca_transformation_matrix = pd.read_csv(pca_transformation_matrix_path).values

    pca_explained_variance = pd.read_csv(pca_explained_variance_path).values

    feature_mean = pd.read_csv(feature_mean_path).values

    beta_prime = apply_pca_whitening(pca_transformation_matrix, pca_explained_variance, feature_mean, beta)

    # print( num_features, beta_prime )
    # print(pca_transformation_matrix)

    return num_features, beta_prime

    # return num_channels, beta

# print(extract_feature_vector("D:\\ox_build\\all_souls_000013.jpg"))

    
    



    







