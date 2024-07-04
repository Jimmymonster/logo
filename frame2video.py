import cv2
import os

def frames_to_video(input_folder, output_file, fps, target_width=None, target_height=None):
    images = [img for img in os.listdir(input_folder) if img.endswith(".png") or img.endswith(".jpg")]
    images.sort()  
    
    first_image_path = os.path.join(input_folder, images[0])
    frame = cv2.imread(first_image_path)
    original_height, original_width, layers = frame.shape

    if target_width is None or target_height is None:
        target_width = original_width
        target_height = original_height

    fourcc = cv2.VideoWriter_fourcc(*'mp4v')  
    video = cv2.VideoWriter(output_file, fourcc, max(fps, 1), (target_width, target_height))

    if fps >= 1:
        for image in images:
            frame = cv2.imread(os.path.join(input_folder, image))
            frame_resized = cv2.resize(frame, (target_width, target_height))
            video.write(frame_resized)
    else:
        frame_repeat_count = int(1 / fps)
        for image in images:
            frame = cv2.imread(os.path.join(input_folder, image))
            frame_resized = cv2.resize(frame, (target_width, target_height))
            for _ in range(frame_repeat_count):
                video.write(frame_resized)
    video.release()

    print(f"Video saved as {output_file}")

input_folder = 'frameinput'
output_file = 'output_video.mp4'
fps = 0.5  # 2 sec per frame
target_width = 640  # Resize all frames to width 640
target_height = 480  # Resize all frames to height 480

frames_to_video(input_folder, output_file, fps, target_width, target_height)
