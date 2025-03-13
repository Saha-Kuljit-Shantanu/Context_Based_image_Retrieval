import csv
from math import sqrt

Oxford5k_file = 'coweighed_semantic_convolutional_feature_44p_GS\\Oxford5k\\image_features_with_pca.csv'
Paris6k_file = 'coweighed_semantic_convolutional_feature_44p_GS\\Paris6k\\image_features_with_pca.csv'
# filename = 'image_features.csv'

#path = 'D:\\context_based_image_retrieval\\image-query\\public\\Data\\'

oxford_path = 'D:\\context_based_image_retrieval\\image-query\\public\\Oxford5k\\'
paris_path = 'D:\\context_based_image_retrieval\\image-query\\public\\Paris6k\\'

def get_euclidian_distance_sorted(query_vector, num_features, dataset) :

    #Initialize an empty list of euclidian distance

    if dataset == "Oxford5k" : 
        filename = Oxford5k_file
        path = oxford_path
    if dataset == "Paris6k" : 
        filename = Paris6k_file
        path = paris_path
    
    euclidian_distance_list = list()
    
    with open(filename) as csvfile:
        
        csv_reader = csv.reader(csvfile)

        next(csv_reader)
        
        #Read each row from the csv file
        for row in csv_reader:

            #Initialize euclidian distance

            euclidian_distance = 0
            
            #Loop for each feature cell in the row to the Query vector
          
            for i in range(0,num_features,1): 

                #Update euclidian distance
                
                euclidian_distance = euclidian_distance + (query_vector[i] - float( row [i+1] ))* (query_vector[i] - float( row [i+1] ))
                
            #Update euclidian distance
                
            euclidian_distance = sqrt(euclidian_distance)

            #Create a tuple of image path and euclidian distance from the query image

            image_tuple = (path + row[0], euclidian_distance, row[0])

            #Append the tuple to the histogram list

            euclidian_distance_list.append(image_tuple)

    #Sort the list and return to the back end

    euclidian_distance_list.sort(key = lambda tup: tup[1])

    return euclidian_distance_list
        