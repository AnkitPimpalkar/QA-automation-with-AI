import os
import logging

def get_sheet_url():
    """Read sheet URL from config/sheet_url.txt"""
    try:
        url_path = os.path.join('config', 'sheet_url.txt')
        with open(url_path, 'r') as f:
            return f.read().strip()
    except Exception as e:
        logging.error(f"URL file error: {str(e)}")
        return None

def load_valid_pins(file_path):
    """Load valid PIN codes from a text file"""
    try:
        with open(file_path, 'r') as f:
            return {line.strip() for line in f if line.strip()}
    except IOError as e:
        logging.error(f"PIN file error: {str(e)}")
        return set()
