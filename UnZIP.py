
import os
import sys
import logging
from pathlib import Path
import zipfile as zip_module  # Renamed to avoid conflict with variable names


# Configure logging for better output and debugging
def setup_logging(log_level=logging.INFO):
    """
    Sets up the logging configuration for the script.
    
    Args:
        log_level (int): The logging level (default: INFO).
    
    Returns:
        logging.Logger: The configured logger instance.
    """
    logging.basicConfig(
        level=log_level,
        format='%(asctime)s - %(levelname)s - %(message)s',
        handlers=[
            logging.StreamHandler(sys.stdout),
            logging.FileHandler('unzip_script.log')
        ]
    )
    return logging.getLogger(__name__)


# Global logger instance
logger = setup_logging()


def validate_target_file(target_path):
    """
    Validates if the target ZIP file exists and is a valid file.
    
    Args:
        target_path (str or Path): Path to the target ZIP file.
    
    Returns:
        bool: True if valid, False otherwise.
    
    Raises:
        ValueError: If the path is invalid or not a file.
    """
    target = Path(target_path)
    if not target.exists():
        logger.error(f"Target file '{target_path}' does not exist.")
        return False
    if not target.is_file():
        logger.error(f"Target path '{target_path}' is not a file.")
        return False
    if not target.suffix.lower() == '.zip':
        logger.warning(f"Target file '{target_path}' does not have .zip extension.")
    logger.info(f"Target file '{target_path}' validated successfully.")
    return True


def list_zip_contents(zip_file_obj):
    """
    Lists the contents of the ZIP file without extracting.
    
    Args:
        zip_file_obj (zipfile.ZipFile): Open ZIP file object.
    
    Returns:
        list: List of file names in the ZIP.
    """
    contents = zip_file_obj.namelist()
    logger.info(f"ZIP file contains {len(contents)} items:")
    for item in contents:
        logger.info(f"  - {item}")
    return contents


def create_destination_folder(dest_folder):
    """
    Creates the destination folder if it doesn't exist.
    
    Args:
        dest_folder (str or Path): Path to the destination folder.
    
    Returns:
        Path: The absolute path to the created/verified folder.
    """
    dest_path = Path(dest_folder)
    dest_path.mkdir(parents=True, exist_ok=True)
    logger.info(f"Destination folder '{dest_path.absolute()}' is ready.")
    return dest_path.absolute()


def extract_zip_file(zip_file_obj, dest_folder):
    """
    Extracts the contents of the ZIP file to the destination folder.
    
    Args:
        zip_file_obj (zipfile.ZipFile): Open ZIP file object.
        dest_folder (str or Path): Path to the destination folder.
    
    Returns:
        bool: True if extraction successful, False otherwise.
    """
    try:
        zip_file_obj.extractall(dest_folder)
        logger.info(f"Extraction completed successfully to '{dest_folder}'.")
        return True
    except zipfile.BadZipFile as e:
        logger.error(f"Invalid ZIP file: {e}")
        return False
    except PermissionError as e:
        logger.error(f"Permission denied during extraction: {e}")
        return False
    except Exception as e:
        logger.error(f"Unexpected error during extraction: {e}")
        return False


def main():
    """
    Main function to orchestrate the unzipping process.
    
    This function handles the high-level flow:
    1. Configuration
    2. Validation
    3. Listing contents
    4. Extraction
    5. Cleanup and reporting
    """
    # Configuration section
    target_file = "demo.zip"  # Can be made configurable via args or config file
    destination_folder = "unzip"  # Default destination
    
    logger.info("=== Starting ZIP Unzipper Script ===")
    
    # Step 1: Validate target file
    if not validate_target_file(target_file):
        logger.error("Aborting due to invalid target file.")
        sys.exit(1)
    
    # Step 2: Open the ZIP file with error handling
    zip_file = None
    try:
        zip_file = zip_module.ZipFile(target_file, 'r')
        logger.info("ZIP file opened successfully.")
        
        # Step 3: List contents (optional but informative)
        list_zip_contents(zip_file)
        
        # Step 4: Prepare destination
        dest_path = create_destination_folder(destination_folder)
        
        # Step 5: Extract
        if extract_zip_file(zip_file, dest_path):
            logger.info("All operations completed successfully!")
        else:
            logger.error("Extraction failed. Aborting.")
            sys.exit(1)
    
    except FileNotFoundError:
        logger.error(f"Target file '{target_file}' not found.")
        sys.exit(1)
    except zipfile.BadZipFile:
        logger.error(f"Target file '{target_file}' is not a valid ZIP file.")
        sys.exit(1)
    except Exception as e:
        logger.error(f"Unexpected error: {e}")
        sys.exit(1)
    finally:
        # Step 6: Cleanup - Close the ZIP file if opened
        if zip_file:
            zip_file.close()
            logger.info("ZIP file closed.")
    
    logger.info("=== ZIP Unzipper Script Completed ===")


# Entry point for the script
if __name__ == "__main__":
    main()
