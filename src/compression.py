import os
import cv2
from PIL import Image
from natsort import natsorted
import concurrent.futures

def compress_image(index, input_folder, output_folder, image_file):
    input_image_path = os.path.join(input_folder, image_file)
    output_image_path = os.path.join(output_folder, os.path.splitext(image_file)[0] + '.png')
    
    with Image.open(input_image_path) as img:
        img.save(output_image_path, format='PNG', optimize=True)
    
    print(f"Compressed {image_file} and saved as {output_image_path}")
    return index, image_file

def compress_images(input_folder, output_folder):
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    image_files = natsorted([file for file in os.listdir(input_folder) if file.lower().endswith(('png', 'jpg', 'jpeg', 'tiff', 'bmp'))])

    # Use concurrent futures for parallel processing
    with concurrent.futures.ThreadPoolExecutor() as executor:
        futures = [executor.submit(compress_image, idx, input_folder, output_folder, image_file) for idx, image_file in enumerate(image_files)]
        results = [future.result() for future in concurrent.futures.as_completed(futures)]

    # Sort results by the original index to maintain order
    results.sort(key=lambda x: x[0])
    compressed_files = [result[1] for result in results]
    return compressed_files

# Exemple d'utilisation 
input_folder = "./10k"
output_folder = "./compressed_images"

compress_images(input_folder, output_folder)
