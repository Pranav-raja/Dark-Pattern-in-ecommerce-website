import concurrent.futures
import time
from datetime import datetime

import firebase_connection
import frame_extraction
import yolov8
import ocr_ann


def run_yolo(path, user_id, firebase, storage, day):
    yolov8.predicting(path, user_id, firebase, storage, day)
    return "completed yolo"


def run_ocr_ann(folder_path, user_id, firebase, storage, day):
    ocr_ann.folder_to_images(folder_path, user_id, firebase, storage, day)
    return "completed ocr"


def main():
    print("################# Execution Begins ##################")
    # home_path = "C:\\Users\\prana\\PycharmProjects\\Dark_Pattern"
    video_path = "video/Flipkart.mp4"  # Actual path to your input video
    folder_path = "output_frames"
    user_id = "1001"
    day = datetime.now().strftime("%Y-%m-%d")
    # get the firebase and storage
    firebase, storage = firebase_connection.database_connection()

    # Extraction of frames from video. One frame per second is extracted
    frame_extraction.frame_ex(video_path)
    # Run YOLO and OCR/ANN in parallel
    with concurrent.futures.ThreadPoolExecutor() as executor:
        future_yolo = executor.submit(run_yolo, folder_path, user_id, firebase, storage, day)
        future_ocr_ann = executor.submit(run_ocr_ann, folder_path, user_id, firebase, storage, day)

    # # Get results from the parallel tasks
    result_yolo = future_yolo.result()
    result_ocr_ann = future_ocr_ann.result()
    #
    # Process and print the results
    print("YOLO Result:")
    print(result_yolo)

    print("OCR/ANN Result:")
    print(result_ocr_ann)
    print("################# Execution Completed ##################")

if __name__ == "__main__":
    main()
