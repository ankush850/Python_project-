import os
import img2pdf
import logging

def images_to_pdf(image_folder_path, output_pdf_path='Output.pdf'):
    """
    Converts all images in the specified folder to a single PDF file.

    Parameters:
    - image_folder_path (str): Path to the folder containing images.
    - output_pdf_path (str): Path where the output PDF will be saved. Default is 'Output.pdf'.

    Returns:
    - None
    """

    # Set up logging to provide detailed debug information
    logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

    logging.info(f"Starting PDF conversion for images in folder: {image_folder_path}")

    # Check if the provided folder path exists and is a directory
    if not os.path.exists(image_folder_path):
        logging.error(f"The specified folder path does not exist: {image_folder_path}")
        return
    if not os.path.isdir(image_folder_path):
        logging.error(f"The specified path is not a directory: {image_folder_path}")
        return

    # Supported image extensions
    supported_extensions = ('.jpg', '.jpeg', '.png', '.gif', '.bmp', '.tiff')

    # List all files in the directory and filter by supported image extensions
    try:
        all_files = os.listdir(image_folder_path)
        logging.debug(f"Files found in directory: {all_files}")
    except Exception as e:
        logging.error(f"Error reading directory contents: {e}")
        return

    images = [file for file in all_files if file.lower().endswith(supported_extensions)]

    if not images:
        logging.warning(f"No images found in the folder with supported extensions: {supported_extensions}")
        return

    # Sort images alphabetically to maintain order in PDF
    images.sort()
    logging.info(f"Images to be processed (sorted): {images}")

    # List to hold image bytes
    images_bytes = []

    # Read each image file as bytes
    for image_name in images:
        image_path = os.path.join(image_folder_path, image_name)
        try:
            with open(image_path, 'rb') as img_file:
                img_data = img_file.read()
                images_bytes.append(img_data)
                logging.debug(f"Read image file: {image_name} ({len(img_data)} bytes)")
        except Exception as e:
            logging.error(f"Failed to read image {image_name}: {e}")
            # Optionally continue processing other images or return here
            return

    # Convert image bytes to PDF bytes
    try:
        pdf_bytes = img2pdf.convert(images_bytes)
        logging.info(f"Successfully converted {len(images_bytes)} images to PDF bytes")
    except Exception as e:
        logging.error(f"Failed to convert images to PDF: {e}")
        return

    # Write the PDF bytes to the output file
    try:
        with open(output_pdf_path, 'wb') as pdf_file:
            pdf_file.write(pdf_bytes)
            logging.info(f"PDF file successfully written to: {output_pdf_path}")
    except Exception as e:
        logging.error(f"Failed to write PDF file: {e}")
        return

    logging.info("Image to PDF conversion completed successfully.")

# Example usage:
if __name__ == "__main__":
    # Replace this with your actual folder path containing images
    folder_path = "/path/to/your/image/folder"
    output_pdf = "MyImagesOutput.pdf"
    images_to_pdf(folder_path, output_pdf)
