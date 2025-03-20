import re
import logging
from .base_validator import BaseValidator

class Validator(BaseValidator):
    """
    Validator that uses regex patterns for email validation.
    """
    def __init__(self, config):
        super().__init__(config)
        self.highlight_color = "red"  # Invalid entries marked in red
        
        # Email validation pattern
        # This pattern follows RFC 5322 standard
        self.email_pattern = r'''(?:[a-z0-9!#$%&'*+/=?^_`{|}~-]+(?:\.[a-z0-9!#$%&'*+/=?^_`{|}~-]+)*|"(?:[\x01-\x08\x0b\x0c\x0e-\x1f\x21\x23-\x5b\x5d-\x7f]|\\[\x01-\x09\x0b\x0c\x0e-\x7f])*")@(?:(?:[a-z0-9](?:[a-z0-9-]*[a-z0-9])?\.)+[a-z0-9](?:[a-z0-9-]*[a-z0-9])?|\[(?:(?:(2(5[0-5]|[0-4][0-9])|1[0-9][0-9]|[1-9]?[0-9]))\.){3}(?:(2(5[0-5]|[0-4][0-9])|1[0-9][0-9]|[1-9]?[0-9])|[a-z0-9-]*[a-z0-9]:(?:[\x01-\x08\x0b\x0c\x0e-\x1f\x21-\x5a\x53-\x7f]|\\[\x01-\x09\x0b\x0c\x0e-\x7f])+)\])'''
        
        # Compile pattern for efficiency
        self.regex = re.compile(self.email_pattern, re.IGNORECASE)
        
        # Common email domains for additional validation
        self.common_domains = {
            'gmail.com', 'yahoo.com', 'hotmail.com', 'outlook.com', 
            'aol.com', 'icloud.com', 'protonmail.com', 'zoho.com'
        }

    def _is_valid_email(self, email: str) -> bool:
        """
        Validate email with additional checks beyond regex
        """
        if not email or not isinstance(email, str):
            return False
            
        # Basic regex check
        if not self.regex.fullmatch(email):
            return False
            
        # Split email into local and domain parts
        try:
            local, domain = email.rsplit('@', 1)
        except ValueError:
            return False
            
        # Additional validation rules
        if len(local) > 64:  # Local part length check
            return False
        if len(domain) > 255:  # Domain length check
            return False
        if domain.endswith('.'):  # No trailing dot
            return False
            
        # Warning for uncommon domains (but still valid)
        if domain.lower() not in self.common_domains:
            logging.info(f"Uncommon email domain found: {domain}")
            
        return True

    def validate(self, data, valid_pins):
        """Validate email addresses in the data"""
        invalid_cells = []
        if not data or len(data) < 1:
            return invalid_cells
            
        try:
            headers = [str(h).strip().lower() for h in data[0]]
            col_idx = next(
                (i for i, h in enumerate(headers)
                if h in ["email", "e-mail", "email address", "e-mail address"]
                ),
                None
            )
            
            if col_idx is None:
                logging.warning("Email column not found")
                return invalid_cells
                
            for row_idx, row in enumerate(data[1:], start=2):
                if col_idx >= len(row):
                    continue
                    
                email = str(row[col_idx]).strip()
                if not email:  # Skip empty cells
                    continue
                    
                if not self._is_valid_email(email):
                    cell_ref = f"{chr(65 + col_idx)}{row_idx}"
                    invalid_cells.append((cell_ref, self.highlight_color))
                    logging.info(f"Invalid email found in {cell_ref}: {email}")
                    
        except Exception as e:
            logging.error(f"Email validation error: {e}")
            
        return invalid_cells
