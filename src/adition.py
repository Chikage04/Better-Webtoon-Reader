import os
import numpy as np
import cv2  # Utilisation d'OpenCV pour des opérations d'image plus rapides
from natsort import natsorted
import concurrent.futures

def load_image(index, image_path):
    image = cv2.imread(image_path, cv2.IMREAD_UNCHANGED)
    return index, image

def load_images(folder_path):
    image_files = natsorted(os.listdir(folder_path))
    max_height = 0

    # Use concurrent futures for parallel loading
    with concurrent.futures.ThreadPoolExecutor() as executor:
        futures = [executor.submit(load_image, idx, os.path.join(folder_path, image_file)) for idx, image_file in enumerate(image_files)]
        results = [future.result() for future in concurrent.futures.as_completed(futures)]

    # Sort results by the original index to maintain order
    results.sort(key=lambda x: x[0])
    images = [result[1] for result in results]
    max_height = max(image.shape[0] for image in images)

    return images, max_height

def pad_image_to_max_height(image, max_height):
    height_diff = max_height - image.shape[0]
    if height_diff > 0:
        padding = np.zeros((height_diff, image.shape[1], image.shape[2]), dtype=np.uint8)
        image = np.vstack((image, padding))
    return image

def pad_images_to_max_height(images, max_height):
    # Use concurrent futures for parallel padding
    with concurrent.futures.ThreadPoolExecutor() as executor:
        padded_images = list(executor.map(lambda img: pad_image_to_max_height(img, max_height), images))
    return padded_images

def save_image_segments(concatenated_image, output_path, max_dimension=23000):
    total_height = concatenated_image.shape[0]
    num_segments = (total_height + max_dimension - 1) // max_dimension

    for i in range(num_segments):
        start_row = i * max_dimension
        end_row = min(start_row + max_dimension, total_height)
        segment = concatenated_image[start_row:end_row]
        segment_output_path = f"{os.path.splitext(output_path)[0]}_part{i+1}.jpg"
        cv2.imwrite(segment_output_path, segment)
        print(f"Saved segment {i+1} as {segment_output_path}")

def concatenate_images(folder_path, output_path):
    images, max_height = load_images(folder_path)
    padded_images = pad_images_to_max_height(images, max_height)
    concatenated_image = np.vstack(padded_images)
    save_image_segments(concatenated_image, output_path)

# Example usage
folder_path = "./upscaled"
output_path = "./10k/image_concatenated.jpg"

concatenate_images(folder_path, output_path)
