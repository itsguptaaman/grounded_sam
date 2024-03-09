
import hashlib
import os
import traceback

from PIL import Image
import tempfile
import shutil

def resize_image(image_path, target_size=(1280, 720)):
    try:
        ext = image_path.split(".")[-1]

        # Open the image file
        with Image.open(image_path) as img:
            # Get the original dimensions
            original_width, original_height = img.size
            
            # Calculate the aspect ratios
            original_aspect_ratio = original_width / original_height
            target_aspect_ratio = target_size[0] / target_size[1]

            # Resize the image while preserving the aspect ratio
            if original_aspect_ratio > target_aspect_ratio:
                # Scale based on width
                new_width = target_size[0]
                new_height = int(new_width / original_aspect_ratio)
            else:
                # Scale based on height
                new_height = target_size[1]
                new_width = int(new_height * original_aspect_ratio)
            
            resized_img = img.resize((new_width, new_height))

            # Create a new blank image with the target size
            final_img = Image.new("RGB", target_size)
            
            # Paste the resized image onto the blank image
            final_img.paste(resized_img, ((target_size[0] - new_width) // 2, (target_size[1] - new_height) // 2))

            # Save the resized image
            final_img.save(image_path)

            print("Image resized successfully.")
    except Exception as e:
        traceback.print_exc()
        print("Error:", e)



# Function to save image to the images folder
def save_uploaded_image(uploaded_image, IMAGES_PATH):
    # Create a temporary file to save the uploaded image
    with tempfile.NamedTemporaryFile(delete=False) as temp_file:
        # Write the uploaded image data to the temporary file
        for chunk in uploaded_image:
            temp_file.write(chunk)
    
    # Calculate MD5 hash of the temporary file
    md5_hash = hashlib.md5()
    with open(temp_file.name, "rb") as f:
        # Read the file in chunks to handle large files efficiently
        for chunk in iter(lambda: f.read(4096), b""):
            md5_hash.update(chunk)

    # Convert the MD5 hash to hexadecimal format
    md5_hex = md5_hash.hexdigest()
    
    # Get the file extension
    file_extension = os.path.splitext(uploaded_image.name)[1]
    
    # Save the image with the MD5 hash as its name
    img_name = md5_hex + file_extension
    img_path = os.path.join(IMAGES_PATH, img_name)
    
    # Move the temporary file to the final location, replacing the existing file if it exists
    if os.path.exists(img_path):
        os.remove(img_path)  # Remove the existing file
    shutil.move(temp_file.name, img_path)  # Move the temporary file to the final location
    
    return img_path



if __name__ == "__main__":
    # Provide the path to the image file
    # image_path = r"C:\Users\Aman\Downloads\images\6c90e6b429bd9cfcc3a718adcc0f0c78.jpg"
    image_path = "dog.jpeg"
    # Check if the file exists
    if os.path.exists(image_path):
        resize_image(image_path)
    else:
        print("Image file not found.")

