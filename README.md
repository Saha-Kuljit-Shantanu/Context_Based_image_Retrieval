# Context_Based_image_Retrieval

**Purpose :** Taking an image as input and retrieve images in a sequence of their distances with the Query image in ascending order for a chosen algorithm ( A little update to the **Image_Query_by_Analysing_Histogram_Distance** repository)

**Data Training :**
  - Will not be required as the models are pretrained by imageNet and fine-tuned for dataset **paris6k** and **oxford5k**

**Dataset Requirements :**
  - The Paris6k images must be kept in the folder **/image-query/public/Paris6k** and the Oxford5k images must be kept in **/image-query/public/Oxford5k** 
  - These images are already trained in kaggle and the learnt parametres and weights are stored in csv files


**How to run this Project ?**
  - Open the entire folder **Context_Based_Image_Retrieval** as a project in any text editor and navigate to this folder in terminal
  - If **Flask** is not installed, then it needs to be installed :
      - **pip install flask**
  - If **PIL (Python Image Library)** is not installed, then it needs to be installed :
      - **pip install PIL**
  - Open two terminals
  - In the first terminal put the following commands sequentially :
      - **cd image-query**
      - **npm install** (Only the first time to install dependencies)
      - **npm run dev**
  - In the second terminal run **/Flask-Server.py**
  - Navigate to the webpage **https://localhost:5000** ( The listening port might vary from device to device, the server port is the port displayed while running the python file **Flask-Server.py** )
  - Click **Upload** button and this will open a pop-up window with all files in the computer
  - Select the image from your local machine
  - Choose algorithm and dataset from the respective dropdowns
  - Click **Search** button and view the retrieved images
