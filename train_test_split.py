import os
import shutil
from sklearn.model_selection import train_test_split

def split_images_into_train_test(input_directory, train_ratio=0.85, random_seed=42):
    # Create output directories if they don't exist
    train_directory = os.path.join(input_directory, "train/1")
    test_directory = os.path.join(input_directory, "test/1")
    
    os.makedirs(train_directory, exist_ok=True)
    os.makedirs(test_directory, exist_ok=True)

    # List to store all image file names
    all_images = []

    # Iterate over each image in the directory
    for filename in os.listdir(input_directory):
        if filename.endswith(".png") or filename.endswith(".jpg"):  # Adjust the file extensions as needed
            all_images.append(filename)

    # Use train_test_split to split the list of image file names
    train_images, test_images = train_test_split(all_images, test_size=1 - train_ratio, random_state=random_seed)

    # Copy images to the train directory
    for image in train_images:
        source_path = os.path.join(input_directory, image)
        destination_path = os.path.join(train_directory, image)
        shutil.copyfile(source_path, destination_path)

    # Copy images to the test directory
    for image in test_images:
        source_path = os.path.join(input_directory, image)
        destination_path = os.path.join(test_directory, image)
        shutil.copyfile(source_path, destination_path)

    print("Splitting completed.")

# Replace 'your_image_directory' with the actual path to your image directory
image_directory = 'klh_dataset_large'
split_images_into_train_test(image_directory, train_ratio=0.85)

