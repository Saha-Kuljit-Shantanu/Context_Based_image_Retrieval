from PIL import Image
import numpy as np

def get_histogram_vector(horizontal_length,vertical_length,temp_histogram_vector,pixels) :

    for h in range(horizontal_length) :

        for v in range(vertical_length) :

            #Extracting color_scale from each pixel

            color_scale = pixels[h,v] 

            #Increasing the count for the extracted greayscale color

            temp_histogram_vector[color_scale] = temp_histogram_vector[color_scale] + 1 

    return temp_histogram_vector

def get_normalized_histogram_vector(histogram_vector) :

    total_pixel_value = 0

    #Add all pixel values in the histogram vector 

    for pixel_value in histogram_vector :

        total_pixel_value = total_pixel_value + pixel_value

    #For each pixel value in the histogram vector, find the normalized form
        
    for pixel_number in range ( len(histogram_vector) ) :

        histogram_vector[pixel_number] = histogram_vector[pixel_number] / total_pixel_value

    return histogram_vector

def extract_histogram_vector(imagepath) :

    #Get image by path

    img = Image.open(imagepath) 

    #Convert the image to greyscale

    img = img.convert("L") 

    #Get the greyScale image pixels as a numpy array

    pixels = np.asarray(img) 

    #Initiate the histogram vector of 256 cells

    temp_histogram_vector = [0]*256 

    #Update the histogram vector by analysing each pixel in rows and columns

    histogram_vector = get_histogram_vector(pixels.shape[0],pixels.shape[1],temp_histogram_vector,pixels) 

    #Normalize the histogram vector

    histogram_vector = get_normalized_histogram_vector(histogram_vector) 


    #Return the updated normalized histogram_vector

    return histogram_vector





