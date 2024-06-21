import matplotlib
from datetime import datetime
import pyrebase
import csv
matplotlib.use('Agg')


def database_connection():
    print("connecting to firebase...")
    # Config to connect to the firebase
    config = {
        # provide the following to upload in your firebase database
        # "apiKey": "",
        # "projectId": "",
        # "authDomain": "",
        # "databaseURL": "",
        # "storageBucket": "",
        # "messingSenderId": "",
        # "appId": "",
        # "measurementId": ""
    }

    firebase = pyrebase.initialize_app(config)
    print("connected to firebase")
    storage = firebase.storage()  # to access the storage
    return firebase, storage


# Function to open CSV file and write contents along with current date and time
def write_to_csv(filename, data):
    # Get the current date and time
    current_datetime = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # Append the current date and time to the data
    data_with_datetime = [current_datetime] + data

    # Open the CSV file in append mode
    with open(filename, 'a', newline='') as csvfile:
        # Create a CSV writer object
        csv_writer = csv.writer(csvfile)

        # Write the data to the CSV file
        csv_writer.writerow(data_with_datetime)


def yolo_csv_download(firebase, day):
    try:
        firebase.storage().child(f"csv_files/yolo_csv/yolo_{day}.csv").download("", filename="yolo_database.csv")
        print("file downloaded")
    except Exception:
        print("No YOLO database csv file is found! New file is created")
        # Open the file in 'w' mode (write mode) to create an empty file
        with open("yolo_database.csv", 'w', newline='') as csv_file:
            # Create a CSV writer object
            csv_writer = csv.writer(csv_file)


def yolo_csv_upload(firebase, day):
    firebase.storage().child(f"csv_files/yolo_csv/yolo_{day}.csv").put("yolo_database.csv")
    print("file uploaded")


def ann_csv_download(firebase, day):
    try:
        firebase.storage().child(f"csv_files/pattern_csv/ann_{day}.csv").download("", filename="ann_database.csv")
        print("file downloaded")
    except Exception:
        print("No ANN database csv file is found! New file is created")
        # Open the file in 'w' mode (write mode) to create an empty file
        with open("ann_database.csv", 'w', newline='') as csv_file:
            # Create a CSV writer object
            csv_writer = csv.writer(csv_file)


def ann_csv_upload(firebase, day):
    firebase.storage().child(f"csv_files/pattern_csv/ann_{day}.csv").put("ann_database.csv")
    print("file uploaded")

