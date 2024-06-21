# Dark Pattern in ecommerce website and mobile applications
Implemented dark pattern categorization with YOLOv8 and uploaded results to Firebase for verification and tracking evolution.

**Dark Pattern Categorization using YOLOv8**

The goal of this project is to automate the identification and categorization of dark patterns in e-commerce websites and mobile applications. These patterns are manipulative tactics used to trick users into making unintended decisions.

**Working Process**

1. **Input**: The user needs to provide a screen recording of the e-commerce website or app they wish to analyze. This recording should be saved in the `video/` directory.
2. **Frame Extraction**: The screen recording is divided into individual frames, which allows the YOLOv8 model to process each frame separately, file is not presented then the code creates by its own.
3. **Detection**: The frames are fed into the YOLOv8 object detection model. This model has been trained on a custom dataset that contains various types of dark patterns.
4. **Output**: The YOLOv8 model outputs images with bounding boxes around the detected dark patterns. Each bounding box is labeled with the class of the dark pattern.
5. **Upload**: The identified dark pattern images, along with their class labels, are uploaded to Firebase for further verification and to track their evolution. Additionally, a CSV file containing the image ID and identified class labels is generated and uploaded.

**Dataset Creation**

- The dataset used to train the YOLOv8 model was created manually using Roboflow.
- Images were sourced from various e-commerce websites.
- Each image in the dataset was manually annotated to accurately label the dark patterns.

**Files and Directories**

- **trained_models/**: Contains the YOLOv8 model files, including weights and configuration files.
- **main**: Contains the Python scripts for frame extraction, object detection, and uploading results to Firebase.
- **output/**: Stores the output images with bounding boxes and class labels.
- **database.csv**: A CSV file that lists the image IDs and the identified class labels for each detected dark pattern.

**Installation Instructions**

1. Clone the repository to your local machine.
2. Install the required Python packages.

**Usage Instructions**

1. Place your screen recording file in the `video/` directory.
2. Run the `main.py` script with the appropriate input and output arguments.
3. The script will process the video, detect dark patterns, and save the results in the `output/` directory. The results will also be uploaded to Firebase.

**Contributing**

Contributions to this project are welcome. If you have improvements or new features to add, please fork the repository and submit a pull request. Excepting for User interface.
