from .base_validator import BaseValidator

class Validator(BaseValidator):
    """
    Validator for PIN codes.
    Assumes that the PIN column is determined by column_name.
    """
    def __init__(self, config):
        super().__init__(config)
        # Optionally override the valid pins file from parameters if needed.
        self.valid_pins_file = self.params.get("valid_pins_file", "valid_pins.txt")
    
    def validate(self, data, valid_pins):
        invalid_cells = []
        # Find the column index for the PIN based on header match (case-insensitive).
        headers = [h.lower() for h in data[0]]
        try:
            col_idx = headers.index(self.column_name.lower())
        except ValueError:
            return invalid_cells  # Column not found; skip validation.
        
        for row_idx, row in enumerate(data[1:], start=2):
            # Make sure the row has the expected column.
            if col_idx < len(row):
                pin = row[col_idx].strip()
                if pin and pin not in valid_pins:
                    # Convert col_idx to letter (assuming 0 -> A, etc.)
                    cell = f"{chr(65 + col_idx)}{row_idx}"
                    invalid_cells.append(cell)
        return invalid_cells
