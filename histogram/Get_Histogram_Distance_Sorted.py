import csv
from math import sqrt

Oxford5k_file = 'histogram\\Oxford5k\\Histogram_file.csv'
Paris6k_file = 'histogram\\Paris6k\\Histogram_file.csv'

# path = 'D:\\context_based_image_retrieval\\image-query\\public\\Data\\'

oxford_path = 'D:\\context_based_image_retrieval\\image-query\\public\\Oxford5k\\'
paris_path = 'D:\\context_based_image_retrieval\\image-query\\public\\Paris6k\\'

def get_histogram_distance_sorted(query_histogram_vector, dataset) :

    #Initialize an empty list of histogram distance

    histogram_distance_list = list()

    if dataset == "Oxford5k" : 
        filename = Oxford5k_file
        path = oxford_path
    if dataset == "Paris6k" : 
        filename = Paris6k_file
        path = paris_path

    with open(filename) as csvfile:

        csv_reader = csv.reader(csvfile)

        #Read each row from the csv file
        for row in csv_reader:

            #Initialize histogram distance

            histogram_distance = 0

            #Loop for each histogram cell in the row to the Query histogram vector

            for i in range(0,256,1): 

                #Update histogram distance
                    
                histogram_distance = histogram_distance + (query_histogram_vector[i] - float( row [i+1] ))* (query_histogram_vector[i] - float( row [i+1] ))

            #Update histogram distance
                
            histogram_distance = sqrt(histogram_distance)

            #Create a tuple of image path and histogram distance from the query image

            image_tuple = (path + row[0], histogram_distance, row[0])
            

            #Append the tuple to the histogram list

            histogram_distance_list.append(image_tuple)

    #Sort the list and return to the back end

    histogram_distance_list.sort(key = lambda tup: tup[1])

    return histogram_distance_list
        