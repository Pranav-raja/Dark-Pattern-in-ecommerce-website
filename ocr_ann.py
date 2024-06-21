from datetime import datetime

import firebase_connection
import image_Text_recog
import pickle
from tensorflow.keras.models import load_model
ann_csv_filename = "ann_database.csv"

def processing(path):
    # ocr is used to extract the text from the image
    text = image_Text_recog.Text_recog(path)
    string = " ".join(text)
    return string


# get the frames stored in the folder one by one and perform the prediction task
def folder_to_images(folder_path,user_id, firebase, storage, day):
    # get the date
    firebase_connection.yolo_csv_download(firebase, day)

    # download the today database file
    firebase_connection.ann_csv_download(firebase, day)

    # folder where the image is stored
    cloud_folder = datetime.now().strftime("%Y-%m-%d") + "/"
    current_time = user_id + "_" + datetime.now().strftime("%H-%M-%S") + "_"

    model = load_model('trained_models/dark_pattern_ann.h5')
    print("model loaded")

    # Load the Tokenizer from the saved file
    with open('trained_models/tokenizer.pkl', 'rb') as tokenizer_file:
        loaded_tokenizer = pickle.load(tokenizer_file)

    cont = True
    frame = 0
    while cont:
        try:
            print(f"\n----------------------reading the image-{frame}--------------------\n")
            image_path = f"{folder_path}/frame_{frame}.jpg"
            text = processing(image_path)
            # Now, 'loaded_tokenizer' is a Tokenizer object loaded from the file
            text = loaded_tokenizer.texts_to_matrix([text])
            # print(text)
            text_labels = ['Forced Action', 'Misdirection', 'Obstruction', 'Scarcity', 'Sneaking', 'Social Proof', 'Urgency']
            # print(text_labels)
            pred = model.predict(text)
            print(pred)
            fin_cloudpath = cloud_folder + current_time + f"img_{frame}.jpg"
            flag = 1
            for i in range(7):
                if(pred[0][i]>0.95):
                    print(f"{i} - {text_labels[i]}")
                    data_to_write = [fin_cloudpath, text_labels[i]]
                    # write the data into the ann csv file
                    firebase_connection.write_to_csv(ann_csv_filename, data_to_write)
                    if flag == 1:
                        firebase.storage().child(fin_cloudpath).put(image_path)
                        flag = 0
            frame += 1
        except Exception:
            print("OCR and ANN execution completed")
            cont = False

    # finally upload the file
    firebase_connection.ann_csv_upload(firebase, day)


