import os
import logging
from datetime import datetime
from src.config_loader import get_sheet_url, load_valid_pins
from src.sheet_manager import connect_to_sheet, process_sheet
from src.validator_loader import load_validators
 
DEFAULT_CREDENTIALS_PATH = "config/credentials.json"
VALID_PINS_FILE = "config/valid_pins.txt"
VALIDATORS_CONFIG_FILE = "config/validators_config.json"

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def main():
    logging.info("Starting validation process")

    sheet_url = get_sheet_url()
    if not sheet_url:
        raise ValueError("Sheet URL is required")

    sheet = connect_to_sheet(DEFAULT_CREDENTIALS_PATH, sheet_url)
    if not sheet:
        raise ConnectionError("Failed to connect to Google Sheets")

    valid_pins = load_valid_pins(VALID_PINS_FILE)
    validators = load_validators(VALIDATORS_CONFIG_FILE)

    start_time = datetime.now()
    invalid_count = process_sheet(sheet, validators, valid_pins)
    duration = datetime.now() - start_time

    logging.info(f"Validation completed\nInvalid entries: {invalid_count}\nDuration: {duration.total_seconds():.2f} seconds")

if __name__ == "__main__":
    main()
