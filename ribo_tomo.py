import os
import mrcfile
import numpy as np
from skimage import exposure
from skimage.transform import resize
import cv2
from tqdm import tqdm
from PIL import Image

def normalize_slice(slice_data):
    # Normalize the slice
    normalized_slice = exposure.rescale_intensity(slice_data, in_range='image', out_range=(0, 1))
    return normalized_slice

def divide_into_pieces(slice_data, piece_shape=(480, 480), subpiece_shape=(224, 224)):
    # Divide each slice into a 2x2 grid of subimages and resize each subimage to subpiece_shape
    pieces = []
    height, width = slice_data.shape
    h_subpiece, w_subpiece = height // 2, width // 2
    for i in range(0, height, h_subpiece):
        for j in range(0, width, w_subpiece):
            subimage = slice_data[i:i+h_subpiece, j:j+w_subpiece]
            resized_subimage = cv2.resize(subimage, subpiece_shape, interpolation=cv2.INTER_LINEAR)
            pieces.append(resized_subimage)
    return pieces

def save_pieces(output_dir, mrc_name, pieces, depth):
    # Save each piece as an image
    for i, piece in enumerate(pieces):
        piece_name = f"{mrc_name}_{depth}_{i}.png"
        piece_path = os.path.join(output_dir, piece_name)
        piece = np.uint8(piece * 255)  # Convert to uint8 for saving as grayscale image
        piece = np.squeeze(piece)  # Remove singleton dimension if present
        img = Image.fromarray(piece)
        img.save(piece_path)

def process_mrc_files(input_dir, output_dir):
    # Process each MRC file in the directory
    for filename in tqdm(os.listdir(input_dir)):
        if filename.endswith('.mrc'):
            with mrcfile.open(os.path.join(input_dir, filename), permissive=True) as mrc:
                mrc_name = os.path.splitext(filename)[0]
                depth_data = mrc.data[60:181]  # Extract slices from depth 50 to 180
                for depth, slice_data in enumerate(depth_data, start=60):
                    normalized_slice = normalize_slice(slice_data)
                    pieces = divide_into_pieces(normalized_slice)
                    save_pieces(output_dir, mrc_name, pieces, depth)

# Example usage:
input_directory = "../tomos/tomograms_denoised"
output_directory = "../tomos/sliced/train/1"

process_mrc_files(input_directory, output_directory)
