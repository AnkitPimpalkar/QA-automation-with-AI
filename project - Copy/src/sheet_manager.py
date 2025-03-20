import gspread
import logging
from oauth2client.service_account import ServiceAccountCredentials

SCOPES = [
    "https://spreadsheets.google.com/feeds",
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive.file",
    "https://www.googleapis.com/auth/drive"
]

def connect_to_sheet(credentials_path, sheet_url):
    """Establish connection to Google Sheets API."""
    try:
        credentials = ServiceAccountCredentials.from_json_keyfile_name(credentials_path, SCOPES)
        client = gspread.authorize(credentials)
        return client.open_by_url(sheet_url).sheet1
    except Exception as e:
        logging.error(f"Sheet connection failed: {str(e)}")
        return None

def process_sheet(sheet, validators, valid_pins):
    """
    Process the Google Sheet and validate data using provided validators.
    Highlights cells based on the highlight color returned by each validator.
    Also writes updated cell values back to the sheet.
    
    Args:
        sheet: A gspread.Worksheet object.
        validators: A list of validator objects.
        valid_pins: A set of valid PIN codes.
        
    Returns:
        The total number of invalid cells found.
    """
    data = sheet.get_all_values()
    if not data:
        logging.warning("No data found in sheet")
        return 0

    # Dictionary to group cell references by highlight color.
    highlight_groups = {}  # e.g., { "yellow": ["E2", "E5"], "red": ["B3", "D5"] }

    # Run each validator on the sheet data.
    for validator in validators:
        # Each validator should return either:
        #   - A cell reference string (e.g., "B2"), or
        #   - A tuple (cell reference, highlight color) (e.g., ("E2", "yellow"))
        result = validator.validate(data, valid_pins)
        for item in result:
            if isinstance(item, tuple):
                cell_ref, color = item
            else:
                cell_ref, color = item, "red"  # Default invalid cells highlighted in red.
            highlight_groups.setdefault(color, []).append(cell_ref)

    # Write the updated data (with corrected call notes) back to the sheet.
    sheet.update('A1', data)
    
    total_invalid = 0
    # Process each group of cells and apply formatting.
    for color, cell_list in highlight_groups.items():
        total_invalid += len(cell_list)
        if color == "yellow":
            fmt = {"backgroundColor": {"red": 1.0, "green": 1.0, "blue": 0.0}}  # Yellow highlight.
        elif color == "red":
            fmt = {"backgroundColor": {"red": 1.0, "green": 0.8, "blue": 0.8}}  # Light red highlight.
        else:
            fmt = {"backgroundColor": {"red": 1.0, "green": 0.8, "blue": 0.8}}  # Default.
        logging.info(f"Highlighting {len(cell_list)} cells in {color}")
        for cell in cell_list:
            sheet.format(cell, fmt)
    
    return total_invalid

