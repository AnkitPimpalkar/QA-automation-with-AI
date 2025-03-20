import re
import logging
from .base_validator import BaseValidator

class Validator(BaseValidator):
    """Validates phone numbers in various formats"""
    
    def __init__(self, config):
        super().__init__(config)
        self.highlight_color = "red"  # Invalid entries marked in red
        
        # Supported formats:
        # +91 1234567890
        # (+91) 1234567890
        # +91-123-456-7890
        # 1234567890
        # 123-456-7890
        # (123) 456-7890
        self.phone_patterns = [
            r'^\+?91[-\s]?\d{10}$',  # Indian format with +91
            r'^\(\+?91\)[-\s]?\d{10}$',  # Indian format with (+91)
            r'^\+?91[-\s]?\d{3}[-\s]?\d{3}[-\s]?\d{4}$',  # Indian format with separators
            r'^\d{10}$',  # Plain 10 digits
            r'^\d{3}[-\s]?\d{3}[-\s]?\d{4}$',  # Format: 123-456-7890
            r'^\(\d{3}\)[-\s]?\d{3}[-\s]?\d{4}$'  # Format: (123) 456-7890
        ]
        
    def _is_valid_phone(self, phone: str) -> bool:
        """Check if phone number matches any valid pattern"""
        if not phone:
            return False
            
        # Remove all whitespace for consistent checking
        phone = phone.strip()
        
        # Try each pattern
        for pattern in self.phone_patterns:
            if re.match(pattern, phone):
                logging.debug(f"Phone {phone} matched pattern {pattern}")
                return True
        logging.debug(f"Phone {phone} did not match any patterns")
        return False
        
    def _clean_phone(self, phone: str) -> str:
        """Clean phone number by removing unnecessary characters except crucial ones"""
        if not phone:
            return ""
        
        # First preserve the structure we want to keep
        phone = phone.strip()
        # Keep the structure of (+91) intact
        if '(+91)' in phone:
            return phone
        # Keep the structure of +91 intact
        if '+91' in phone:
            return phone
        # For other numbers, keep only digits, plus sign, parentheses, and hyphens
        cleaned = re.sub(r'[^\d+()-]', '', phone)
        return cleaned

    def validate(self, data, valid_pins):
        """Validate phone numbers in the data"""
        invalid_cells = []
        if not data or len(data) < 1:
            return invalid_cells
            
        try:
            headers = [str(h).strip().lower() for h in data[0]]
            col_idx = next(
                (i for i, h in enumerate(headers)
                if h in ["phone", "phone number", "contact", "mobile", "cell"]
                ),
                None
            )
            
            if col_idx is None:
                logging.warning("Phone number column not found")
                return invalid_cells
                
            for row_idx, row in enumerate(data[1:], start=2):
                if col_idx >= len(row):
                    continue
                    
                phone = str(row[col_idx]).strip()
                if not phone:  # Skip empty cells
                    continue
                    
                cleaned_phone = self._clean_phone(phone)
                if not self._is_valid_phone(cleaned_phone):
                    cell_ref = f"{chr(65 + col_idx)}{row_idx}"
                    invalid_cells.append((cell_ref, self.highlight_color))
                    logging.info(f"Invalid phone number found in {cell_ref}: {phone}")
                    
        except Exception as e:
            logging.error(f"Phone validation error: {e}")
            
        return invalid_cells