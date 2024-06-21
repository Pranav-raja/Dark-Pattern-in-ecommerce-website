import matplotlib
from ultralytics import YOLO
import cv2
import csv
from datetime import datetime
import pyrebase
import firebase_connection

matplotlib.use('Agg')


def predicting(folder_path, user_id, firebase, storage, day):

    firebase_connection.yolo_csv_download(firebase, day)
    csv_filename = "yolo_database.csv"

    # --------------------necessary path----------------

    model_location = "trained_models/best.pt"
    image_folder = folder_path
    cloud_folder = datetime.now().strftime("%Y-%m-%d") + "/"
    current_time = user_id + "_" + datetime.now().strftime("%H-%M-%S") + "_"

    # Load your trained YOLOv8 model
    model = YOLO(model_location)
    print("\nyolo model is loaded\n")
    results = model.predict(source=image_folder, conf=0.5)
    frame = 0
    for result in results:
        img = result.orig_img
        result_box = result.obb
        ptr1 = 0
        ptr2 = 0
        ptr3 = 0
        upload = 0
        image_path = f"{image_folder}/frame_{frame}.jpg"
        for i in result_box:
            b = i.xyxy[0]  # get box coordinates in (left, top, right, bottom) format
            c = i.cls
            # print(f"boxes: {b}")
            # print(type(c))
            # print(f"class: {c}")
            print("upload - frame", frame)
            fin_cloudpath = cloud_folder + current_time + f"img_{frame}.jpg"
            if upload == 0 and c in [0,1,2]:
                firebase.storage().child(fin_cloudpath).put(image_path)
                upload = 1

            if int(c) == 0 and ptr1 == 0:
                data_to_write = [fin_cloudpath, i.xyxy[0], "da"]
                firebase_connection.write_to_csv(csv_filename, data_to_write)
                ptr1 = 1
            if int(c) == 1 and ptr2 == 0:
                data_to_write = [fin_cloudpath, i.xyxy[0], "fp"]
                firebase_connection.write_to_csv(csv_filename, data_to_write)
                ptr2 = 1
                pass
            if int(c) == 2 and ptr3 == 0:
                data_to_write = [fin_cloudpath, i.xyxy[0], "fu"]
                firebase_connection.write_to_csv(csv_filename, data_to_write)
                ptr3 = 1
            box = list(i.xyxy[0])
            pt1 = (int(float(box[0])), int(float(box[1])))
            pt2 = (int(float(box[2])), int(float(box[3])))
            img = cv2.rectangle(img, pt1, pt2, (0, 0, 255), 2)
        frame += 1

    firebase_connection.yolo_csv_upload(firebase, day)
