import os
import mrcfile
import numpy as np
from skimage import exposure
from skimage.transform import resize
from tqdm import tqdm
from PIL import Image
import cv2

def process_image(image):
    # Image restoration
    histeq_image = cv2.equalizeHist(image)
    restored_image = cv2.medianBlur(histeq_image, 3)
    
    # Adaptive Histogram Equalization
    clahe = cv2.createCLAHE(clipLimit=0.08, tileGridSize=(8, 8))
    adaptive_histeq_image = clahe.apply(restored_image)

    # Guided Filtering
    guided_filtered_image = cv2.ximgproc.guidedFilter(adaptive_histeq_image, adaptive_histeq_image, radius=10, eps=0.2)
    
    return guided_filtered_image


def adjust_contrast(slice_data):
    # # Calculate histogram
    # hist, _ = np.histogram(slice_data, bins=np.arange(0, 1.1, 0.1))

    # # Calculate contrast level
    # contrast = np.sum(hist[:-1] * np.diff(hist))
    # mean_contrast = np.mean(contrast)
    
    # # if debug:
    # #     print(mean_contrast)

    # # Adjust contrast dynamically
    # if mean_contrast < -20000000000.0:
    #     gamma = 2  # Low contrast, increase it
    # elif mean_contrast > -10000000000.0:
    #     gamma = 1.0  # High contrast, decrease it
    # else:
    #     gamma = 1.5  # Moderate contrast, keep it unchanged

    # Adjust the contrast of the slice
    contrast_adjusted_slice = exposure.adjust_gamma(slice_data, gamma=1.3)
    return contrast_adjusted_slice

def normalize_slice(slice_data):
    # Normalize the slice
    # normalized_slice = exposure.rescale_intensity(slice_data, in_range='image', out_range=(0, 1))
    normalized_slice = (slice_data - np.min(slice_data)) / (np.max(slice_data) - np.min(slice_data))
    return normalized_slice

def resize_slice(slice_data, target_shape=(480, 480)):
    # Resize the entire slice to the target shape
    resized_slice = resize(slice_data, target_shape, anti_aliasing=True)
    return resized_slice

def save_slice(output_dir, mrc_name, slice_data, depth):
    # Save the entire slice as an image
    slice_name = f"{mrc_name}_{depth}.png"
    slice_path = os.path.join(output_dir, slice_name)
    slice_data = np.uint8(slice_data * 255)  # Convert to uint8 for saving as grayscale image
    slice_data = np.squeeze(slice_data)  # Remove singleton dimension if present
    img = Image.fromarray(slice_data)
    img.save(slice_path)

def process_mrc_files(input_dir, output_dir):
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    # Process each MRC file in the directory
    for filename in tqdm(sorted(os.listdir(input_dir))):
        if filename.endswith('.mrc'):
            with mrcfile.open(os.path.join(input_dir, filename), permissive=True) as mrc:
                mrc_name = os.path.splitext(filename)[0]
                depth_data = mrc.data[80:151]  # Extract slices from depth 50 to 180
                for depth, slice_data in enumerate(depth_data, start=80):
                    image = slice_data.T
                    normalized_slice = normalize_slice(image)
                    # debug = (depth == 67 or depth == 70)                        
                    contrast_adjusted_image = adjust_contrast(normalized_slice)
                    resized_slice = resize_slice(contrast_adjusted_image)
                    save_slice(output_dir, mrc_name, resized_slice, depth)

# Example usage:
input_directory = "../tomos/tomograms_denoised"
output_directory = "../tomos/whole_preprocessed/train/1"

process_mrc_files(input_directory, output_directory)
