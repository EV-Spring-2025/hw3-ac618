from PIL import Image
import glob
import argparse, os
import numpy as np

def calculate_psnr(orig_dir: str, new_dir: str, frame_type: str="png") -> float:
    """
    Calculate the PSNR (Peak Signal-to-Noise Ratio) between two directories of images.
    The images should be named in a way that they can be matched correctly (e.g., 0000.png, 0001.png, ...).
    """
    orig_images = sorted(glob.glob(os.path.join(orig_dir, f"*.{frame_type}")))
    new_images = sorted(glob.glob(os.path.join(new_dir, f"*.{frame_type}")))
    if not orig_images or not new_images:
        raise ValueError("Both directories must contain images.")
    if len(orig_images) != len(new_images):
        raise ValueError("The number of images in both directories must be the same.")

    psnr_values = []
    
    for orig_img_path, new_img_path in zip(orig_images, new_images):
        orig_img = Image.open(orig_img_path)
        new_img = Image.open(new_img_path)

        if orig_img.size != new_img.size:
            raise ValueError(f"Image sizes do not match: {orig_img.size} vs {new_img.size}")

        orig_data = np.array(orig_img)
        new_data = np.array(new_img)

        mse = np.mean((orig_data - new_data) ** 2)

        if mse == 0:
            psnr = float('inf')  # If MSE is zero, PSNR is infinite
        else:
            psnr = 20 * np.log10(255.0 / np.sqrt(mse))

        psnr_values.append(psnr)

    return sum(psnr_values) / len(psnr_values) if psnr_values else 0.0

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Calculate PSNR between two directories of images.")
    parser.add_argument("orig_dir", type=str, help="Directory containing the original images.")
    parser.add_argument("new_dir", type=str, help="Directory containing the new images to compare against.")
    parser.add_argument("--frame_type", type=str, default="png", help="Type of image frames (default: png).")
    
    args = parser.parse_args()

    psnr_value = calculate_psnr(args.orig_dir, args.new_dir, args.frame_type)
    print(f"Average PSNR: {psnr_value:.2f} dB")