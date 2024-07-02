import cv2
import os

def frames_to_video(input_folder, output_file, fps, target_width=None, target_height=None):
    # Get all the image files from the input folder
    images = [img for img in os.listdir(input_folder) if img.endswith(".png") or img.endswith(".jpg")]
    images.sort()  # Sort the images by filename to maintain the order

    # Read the first image to get the width and height
    first_image_path = os.path.join(input_folder, images[0])
    frame = cv2.imread(first_image_path)
    original_height, original_width, layers = frame.shape

    # Define the target dimensions for resizing
    if target_width is None or target_height is None:
        target_width = original_width
        target_height = original_height

    # Define the codec and create a VideoWriter object
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')  # Use 'XVID' for .avi files
    video = cv2.VideoWriter(output_file, fourcc, max(fps, 1), (target_width, target_height))

    if fps >= 1:
        for image in images:
            frame = cv2.imread(os.path.join(input_folder, image))
            frame_resized = cv2.resize(frame, (target_width, target_height))
            video.write(frame_resized)
    else:
        # Calculate the number of frames to write for each input frame
        frame_repeat_count = int(1 / fps)
        for image in images:
            frame = cv2.imread(os.path.join(input_folder, image))
            frame_resized = cv2.resize(frame, (target_width, target_height))
            for _ in range(frame_repeat_count):
                video.write(frame_resized)

    # Release the video writer object
    video.release()

    print(f"Video saved as {output_file}")

# Example usage
input_folder = 'frameinput'
output_file = 'output_video.mp4'
fps = 0.5  # Example: 2 sec per frame
target_width = 640  # Example: Resize all frames to width 640
target_height = 480  # Example: Resize all frames to height 480

frames_to_video(input_folder, output_file, fps, target_width, target_height)
