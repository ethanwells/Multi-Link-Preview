from PIL import Image
import os

def get_image_dimensions(image_paths):
    widths, heights = [], []

    for image_path in image_paths:
        with Image.open(image_path) as img:
            width, height = img.size
            widths.append(width)
            heights.append(height)

    return min(widths), min(heights)

def crop_images(image_paths, new_width, new_height):
    cropped_images = []

    for image_path in image_paths:
        with Image.open(image_path) as img:
            width, height = img.size

            # Calculate the area to crop
            left = (width - new_width)/2
            top = (height - new_height)/2
            right = (width + new_width)/2
            bottom = (height + new_height)/2

            # Crop the image
            img_cropped = img.crop((left, top, right, bottom))

            # Convert to RGB
            img_cropped = img_cropped.convert('RGB')

            cropped_images.append(img_cropped)

    return cropped_images

def create_canvas_and_fit_images(cropped_images, canvas_width, canvas_height):
    # Create the canvas with white background
    canvas = Image.new('RGB', (canvas_width, canvas_height), 'white')

    # Number of spaces required
    num_spaces = max(0, len(cropped_images) - 1)  # one space between each image

    # Calculate the width for the spaces
    total_space_width = num_spaces * 5  # 5px for each space

    # Calculate the width for each image
    image_width = (canvas_width - total_space_width) // len(cropped_images)

    for i, img in enumerate(cropped_images):
        # Crop image to the desired width (keep the aspect ratio)
        left = (img.width - image_width) / 2
        right = (img.width + image_width) / 2
        img_cropped = img.crop((left, 0, right, img.height))

        # Paste the image onto the canvas at the right position
        position = i * (image_width + 5)  # 5px space between each image
        canvas.paste(img_cropped, (position, 0))

    # Save the result
    canvas.save('multi-link-preview.jpg')

def run(jpgImageList):
    min_width, min_height = get_image_dimensions(jpgImageList)
    cropped_images = crop_images(jpgImageList, min_width, min_height)
    create_canvas_and_fit_images(cropped_images, 2*min_width, min_height)
