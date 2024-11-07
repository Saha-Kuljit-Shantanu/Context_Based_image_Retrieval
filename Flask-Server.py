from flask import Flask, send_from_directory,request,jsonify,render_template
from werkzeug.utils import secure_filename

from histogram import Image_Histogram_Extraction as feature_extractor_0
from histogram import Get_Histogram_Distance_Sorted as image_retriever_0

from coweighed_semantic_convolutional_feature_after_pca import Image_Feature_Extraction as feature_extractor_1a
from coweighed_semantic_convolutional_feature_after_pca import Get_Euclidian_Distance_Sorted as image_retriever_1a

from coweighed_semantic_convolutional_feature_before_pca import Image_Feature_Extraction as feature_extractor_1b
from coweighed_semantic_convolutional_feature_before_pca import Get_Euclidian_Distance_Sorted as image_retriever_1b
import os
#import os

app = Flask(__name__)

#dir_path = os.path.dirname(os.path.realpath(__file__))

#Connect Svelte public folder as root folder with Python Flask

@app.route("/")
def base():
    return send_from_directory('image-query/public', 'index.html')

@app.route("/<path:path>")
def home(path):
    return send_from_directory('image-query/public', path)

#Get image from route upload ,METHOD: POST

app.config['UPLOAD_FOLDER'] = 'uploads'
@app.route("/upload",methods = ['POST'])
def upload_file():

    try: 

        #Get uploaded image from route upload here (python flask) ,METHOD: POST

        file = request.files['image']

        algorithm = request.form['algorithm']

        dataset = request.form['dataset']
        
        #Give the image a filename and secure filename

        # original_filename = file.filename
        
        # filename = secure_filename(original_filename)

        # temp_path = os.path.join( 'image-query\\tmp',filename) 
        
        # file.save(temp_path)
        
        #Retrieve the feature vector from the collected image
        
        # num_features, my_feature_vector = extract_feature_vector(temp_path)    
        
        # my_feature_list = get_euclidian_distance_sorted(my_feature_vector, num_features) 

        print(algorithm)

        if algorithm == "Histogram":

            

            my_feature_vector = feature_extractor_0.extract_histogram_vector(file)  

            print(my_feature_vector)
        
            my_feature_list = image_retriever_0.get_histogram_distance_sorted(my_feature_vector, dataset) 



        if algorithm == "Coweighed Semantic Convolutional Feature (after PCA whitening)":

            original_filename = file.filename
        
            filename = secure_filename(original_filename)

            temp_path = os.path.join( 'image-query\\tmp',filename) 
        
            file.save(temp_path)

            num_features, my_feature_vector = feature_extractor_1a.extract_feature_vector(temp_path, dataset)  
        
            my_feature_list = image_retriever_1a.get_euclidian_distance_sorted(my_feature_vector, num_features, dataset) 

            

        if algorithm == "Coweighed Semantic Convolutional Feature (before PCA whitening)":

            original_filename = file.filename
        
            filename = secure_filename(original_filename)

            temp_path = os.path.join( 'image-query\\tmp',filename) 

            file.save(temp_path)

            num_features, my_feature_vector = feature_extractor_1b.extract_feature_vector(temp_path, dataset)    
        
            my_feature_list = image_retriever_1b.get_euclidian_distance_sorted(my_feature_vector, num_features, dataset) 

            

        
    
        #Return the part of the sorted list to display in front end

        my_fragmented_feature_list = my_feature_list[:]
        
        print( jsonify( {'image_list': my_feature_list} ) )

        return jsonify( {'image_list': my_fragmented_feature_list} )
    
    except:

        print("No file Uploaded")

        return jsonify( {'original_filename': None,
            'filename':  None} )

    


if __name__ == "__main__":
    app.run(debug=True)


#if(my_histogram_list[0][1] != 0):

    #file.save(os.path.join(dir_path + "\\image-query\\public\\Data",original_filename))