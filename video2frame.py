import cv2
import os

def extract_frames(video_path, output_folder, frame_rate=1):
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)
    
    vidcap = cv2.VideoCapture(video_path)
    if not vidcap.isOpened():
        print("Error: Could not open video.")
        return
    
    total_frames = int(vidcap.get(cv2.CAP_PROP_FRAME_COUNT))
    fps = vidcap.get(cv2.CAP_PROP_FPS)
    print(f"Total frames: {total_frames}, FPS: {fps}")
    
    count = 0
    success = True
    
    while success:
        success, image = vidcap.read()
        if success and count % (int(fps) // frame_rate) == 0:
            frame_id = count // (int(fps) // frame_rate)
            output_path = os.path.join(output_folder, f"framettn7_{frame_id:04d}.jpg")
            cv2.imwrite(output_path, image)
            print(f"Saved frame {frame_id} to {output_path}")
        count += 1
    
    vidcap.release()
    print("Finished extracting frames.")

video_path= 'video/TNN16_20240624_173000.mp4'
output_folder='frame'
extract_frames(video_path,output_folder,frame_rate=1)
