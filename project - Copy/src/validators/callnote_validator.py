import logging
import openai
from openai import OpenAI
import json
import time
from typing import Tuple

class Validator:
    """Validates and formats call notes using OpenAI API"""
    
    def __init__(self, config):
        self.column_names = ["call note", "call notes", "callnotes"]
        self.highlight_color = "yellow"
        self.api_key = self._load_api_key()
        self._init_client()
        self.last_api_call = 0
        self.min_delay = 1  # Minimum 1 second between API calls
        
    def _load_api_key(self):
        """Load API key from config file"""
        try:
            with open('config/credentials.json') as f:
                return json.load(f)['openai_api_key']
        except Exception as e:
            logging.error(f"API key load failed: {e}")
            return None

    def _init_client(self):
        """Initialize OpenAI client"""
        if self.api_key:
            try:
                self.client = OpenAI(api_key=self.api_key)
            except Exception as e:
                logging.error(f"OpenAI init failed: {e}")
                self.client = None
        else:
            self.client = None

    def _rate_limit(self):
        """Implement rate limiting"""
        now = time.time()
        time_since_last_call = now - self.last_api_call
        if time_since_last_call < self.min_delay:
            time.sleep(self.min_delay - time_since_last_call)
        self.last_api_call = time.time()

    def process_call_note(self, text: str) -> Tuple[str, bool]:
        """Process call note with a single API call for both correction and formatting"""
        if not self.client or not text.strip():
            return text, False
            
        self._rate_limit()  # Apply rate limiting
            
        try:
            prompt = """You are a call note processor. Your task is to:
1. Correct any grammar or spelling errors
2. Format the text with clear structure, including:
   - Proper line breaks between sections
   - Correct punctuation and capitalization
   - Well-organized contact information
3. Preserve all technical terms and contact details exactly as provided

Return only the processed text without any additional comments."""

            response = self.client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": prompt},
                    {"role": "user", "content": text}
                ],
                temperature=0.3,
                max_tokens=500
            )
            processed_text = response.choices[0].message.content.strip()
            return processed_text, (processed_text != text)
        except openai.RateLimitError as e:
            logging.error(f"Rate limit exceeded: {e}")
            return text, False
        except openai.InsufficientQuotaError as e:
            logging.error(f"Quota exceeded: {e}")
            return text, False
        except Exception as e:
            logging.error(f"OpenAI error: {e}")
            return text, False

    def validate(self, data, valid_pins):
        """Process call notes validation"""
        modified_cells = []
        if not data or len(data) < 1:
            return modified_cells

        try:
            headers = data[0]
            col_idx = next(
                (i for i, h in enumerate(headers) 
                if str(h).strip().lower() in self.column_names
                ),
                None
            )
        except Exception as e:
            logging.error(f"Header error: {e}")
            return modified_cells

        if col_idx is None:
            logging.warning("Call Notes column not found")
            return modified_cells

        for row_idx, row in enumerate(data[1:], start=1):
            if len(row) <= col_idx:
                continue
                
            original = str(row[col_idx]).strip()
            if not original:
                continue

            try:
                processed_text, was_modified = self.process_call_note(original)
                if was_modified:
                    row[col_idx] = processed_text
                    cell_ref = f"{chr(65 + col_idx)}{row_idx + 1}"
                    modified_cells.append((cell_ref, self.highlight_color))
            except Exception as e:
                logging.error(f"Row {row_idx} error: {e}")

        return modified_cells