from PIL import Image
import glob
import argparse

def create_gif_from_frames(frames_dir:str, frame_type:str = "png", dt:int=4e-2, output:str = "output.gif"):
    """
    Create a GIF from a series of image frames stored in the 'frames' directory.
    The images should be named in a way that they can be sorted correctly (e.g., 0000.png, 0001.png, ...).
    """
    # Load all images (make sure they are sorted if needed)
    frames = [Image.open(frame) for frame in sorted(glob.glob(f"{frames_dir}/*.{frame_type}"))]
    if not frames:
        raise ValueError("No frames found in the specified directory.")
    # Save as GIF
    frames[0].save(output,
                   format='GIF',
                   append_images=frames[1:],
                   save_all=True,
                   duration=int(dt * 1000),  # Convert seconds to milliseconds
                   loop=0)  # 0 means infinite loop

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Create a GIF from a series of image frames.")
    parser.add_argument("frames_dir", type=str, help="Directory containing the image frames.")
    parser.add_argument("--frame_type", type=str, default="png", help="Type of image frames (default: png).")
    parser.add_argument("--dt", type=int, default=4e-2, help="Frames per second for the GIF (default: 30).")
    parser.add_argument("--output", type=str, default="output.gif", help="Output GIF file name (default: output.gif).")
    
    args = parser.parse_args()

    create_gif_from_frames(args.frames_dir, args.frame_type, args.dt, args.output)
    print(f"GIF created successfully as '{args.output}'.")