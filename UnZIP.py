import os
import sys
import logging
from pathlib import Path
import zipfile as zip_module

# Simplified logging setup
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def validate_target_file(target_path):
    target = Path(target_path)
    if not target.exists() or not target.is_file() or target.suffix.lower() != '.zip':
        logger.error(f"Invalid target file: {target_path}")
        return False
    logger.info(f"Target file '{target_path}' validated.")
    return True

def list_zip_contents(zip_file_obj):
    contents = zip_file_obj.namelist()
    logger.info(f"ZIP contains {len(contents)} items:")
    for item in contents:
        logger.info(f"  - {item}")
    return contents

def create_destination_folder(dest_folder):
    dest_path = Path(dest_folder).absolute()
    dest_path.mkdir(parents=True, exist_ok=True)
    logger.info(f"Destination: {dest_path}")
    return dest_path

def extract_zip_file(zip_file_obj, dest_folder):
    try:
        zip_file_obj.extractall(dest_folder)
        logger.info(f"Extraction successful to '{dest_folder}'.")
        return True
    except Exception as e:
        logger.error(f"Extraction failed: {e}")
        return False

def main():
    target_file = "demo.zip"
    destination_folder = "unzip"
    
    logger.info("=== Starting ZIP Unzipper ===")
    
    if not validate_target_file(target_file):
        sys.exit(1)
    
    zip_file = None
    try:
        zip_file = zip_module.ZipFile(target_file, 'r')
        logger.info("ZIP opened.")
        list_zip_contents(zip_file)
        dest_path = create_destination_folder(destination_folder)
        if not extract_zip_file(zip_file, dest_path):
            sys.exit(1)
        logger.info("All done!")
    
    except Exception as e:
        logger.error(f"Error: {e}")
        sys.exit(1)
    finally:
        if zip_file:
            zip_file.close()
            logger.info("ZIP closed.")
    
    logger.info("=== Completed ===")

if __name__ == "__main__":
    main()
