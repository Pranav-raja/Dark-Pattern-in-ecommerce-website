import cv2
import time
import os


def frame_ex(path):
    print("################### Frame Extraction Begins ##################33")
    video = cv2.VideoCapture(path)
    fps = video.get(cv2.CAP_PROP_FPS)
    print('frames per second =', fps)

    total_frames = int(video.get(cv2.CAP_PROP_FRAME_COUNT))

    # Calculate the video duration in seconds
    try:
        duration = int(total_frames / fps)
    except:
        duration = total_frames
    print("Video duration", duration)

    output_folder = "output_frames"
    try:
        os.rmdir(output_folder)
        print(f"Directory '{output_folder}' removed successfully.")
    except FileNotFoundError:
        print(f"Directory '{output_folder}' not found.")
    except OSError as e:
        print(f"Error removing directory '{output_folder}': {e}")

    try:
        os.mkdir(output_folder)
        print(f"Directory '{output_folder}' created successfully.")
    except FileExistsError:
        print(f"Directory '{output_folder}' already exists.")

    for i in range(duration):
        # extracts frame per second
        frame_id = int(fps * (i))
        print('frame id =', frame_id)
        video.set(cv2.CAP_PROP_POS_FRAMES, frame_id)
        ret, frame = video.read()
        if ret:
            frame_filename = os.path.join(output_folder, f"frame_{i}.jpg")
            resized_img = cv2.resize(frame, (640, 640), interpolation=cv2.INTER_AREA)
            cv2.imwrite(frame_filename, resized_img)
            print(f"Frame {i} saved as {frame_filename}")
        else:
            print(f"Error reading frame {i}")
        # cv2.waitKey(0)
        time.sleep(0.2)
    print("######################## Frame Extraction Completed ###################")
    print("######################## Preprocessing is Completed ###################")
