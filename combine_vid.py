import cv2
import os
import glob

# === CONFIGURATION ===
dir = "PhysGaussian/output"
input_dirs = [os.path.join(dir, d) for d in ['jelly', 'plasticine', 'sand', 'snow', 'metal', 'foam']]
titles = ['Jelly', 'Plasticine', 'Sand', 'Snow', 'Metal', 'Foam']
output_video = 'output_sequential.mp4'
fps = 25

# === GET FRAME SIZE FROM FIRST IMAGE ===
sample_img = cv2.imread(glob.glob(os.path.join(input_dirs[0], '*.png'))[0])
frame_height, frame_width = sample_img.shape[:2]

# === VIDEO WRITER SETUP ===
fourcc = cv2.VideoWriter_fourcc(*'mp4v')
out = cv2.VideoWriter(output_video, fourcc, fps, (frame_width, frame_height))

# === FONT SETTINGS ===
font = cv2.FONT_HERSHEY_SIMPLEX
font_scale = 1
font_color = (0, 0, 0)
thickness = 2

# === GO THROUGH EACH DIRECTORY SEQUENTIALLY ===
for dir_path, title in zip(input_dirs, titles):
    frames = sorted(glob.glob(os.path.join(dir_path, '*.png')))
    print(f"Writing {len(frames)} frames from {title}...")

    for frame_path in frames:
        img = cv2.imread(frame_path)
        if img is None:
            print(f"Warning: Could not read image {frame_path}")
            continue

        # Add title overlay
        labeled_img = img.copy()
        cv2.putText(labeled_img, title, (10, 30), font, font_scale, font_color, thickness, cv2.LINE_AA)

        # Write to video
        out.write(labeled_img)

        # Show for debugging
        cv2.imshow('Debug View', labeled_img)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            print("Stopped early by user.")
            out.release()
            cv2.destroyAllWindows()
            exit()

# === CLEANUP ===
out.release()
cv2.destroyAllWindows()
print(f"Video saved to {output_video}")
