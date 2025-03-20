
# Google Sheet Validator

A robust Python application for validating data in Google Sheets against customizable validation rules, enhanced with artificial intelligence capabilities.

![GitHub license](https://img.shields.io/badge/license-MIT-blue.svg)

## Description

Google Sheet Validator is a powerful tool designed to automate the validation of data within Google Sheets. It connects to your spreadsheet, applies a set of configurable validation rules, and identifies invalid entries based on your criteria. Enhanced with AI capabilities, this tool goes beyond simple rule-based validation to provide intelligent data quality management. This solution is perfect for maintaining data quality, ensuring consistency, and identifying problematic entries in your spreadsheets.

## Features

- **Google Sheets Integration**: Seamlessly connects to Google Sheets via the Google API
- **Customizable Validators**: Define and configure validation rules via JSON configuration
- **PIN Validation**: Validates entries against a list of authorized PINs
- **Detailed Logging**: Comprehensive logging of the validation process
- **Performance Metrics**: Reports the number of invalid entries and processing time
- **Easy Configuration**: Simple setup via configuration files
- **AI-Powered Validation**: Intelligent validation beyond simple rule-based checks

## AI Capabilities

This project leverages artificial intelligence to enhance data validation processes:

- **Intelligent Pattern Recognition**: Uses machine learning to detect patterns and anomalies in your data that traditional rule-based validation might miss
- **Adaptive Learning**: Improves validation accuracy over time by learning from previously identified issues
- **Natural Language Processing**: Understands and validates text fields using NLP techniques for more accurate results
- **Contextual Validation**: Validates data points not just individually but in context with related fields
- **Anomaly Detection**: Identifies outliers and unusual data entries that may indicate errors
- **Fuzzy Matching**: Uses AI to detect near-matches and potential duplicates

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/google-sheet-validator.git
   cd google-sheet-validator
   ```

2. Install required dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Set up your Google API credentials:
   - Create a project in the [Google Cloud Console](https://console.cloud.google.com/)
   - Enable the Google Sheets API
   - Create OAuth credentials and download as JSON
   - Save the credentials file as `config/credentials.json`

## Configuration

### Google Sheet URL
Set your Google Sheet URL in one of the following ways:
- Environment variable: `SHEET_URL`
- Configuration file (see `src/config_loader.py` for details)

### Valid PINs
Create a file at `config/valid_pins.txt` with one PIN per line:
```
PIN123
PIN456
PIN789
```

### Validators Configuration
Create a JSON configuration file at `config/validators_config.json` to define your validation rules:

```json
[
  {
    "name": "EmailValidator",
    "enabled": true,
    "parameters": {
      "column": "Email",
      "regex": "^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\\.[a-zA-Z0-9-.]+$"
    }
  },
  {
    "name": "PhoneNumberValidator",
    "enabled": true,
    "parameters": {
      "column": "Phone",
      "format": "international"
    }
  }
]
```

## Usage

Run the validator with the following command:

```bash
python run.py
```

The program will:
1. Connect to the specified Google Sheet
2. Load validation rules and valid PINs
3. Process each row in the sheet against the validators and AI models
4. Mark invalid entries directly in the sheet (if configured)
5. Output a summary of validation results

## Project Structure

```
google-sheet-validator/
├── run.py                     # Main entry point
├── requirements.txt           # Python dependencies
├── src/
│   ├── config_loader.py       # Configuration loading utilities
│   ├── sheet_manager.py       # Google Sheets interaction
│   ├── validator_loader.py    # Validator loading and management
│   ├── ai_engine/             # AI model implementations
│   └── validators/            # Individual validator implementations
├── config/
│   ├── credentials.json       # Google API credentials
│   ├── valid_pins.txt         # List of valid PINs
│   └── validators_config.json # Validator configuration
└── README.md                  # This file
```

## Future AI Enhancements

- **Advanced Anomaly Detection**: Implement more sophisticated anomaly detection using deep learning models
- **Predictive Validation**: Anticipate potential data issues before they occur
- **Auto-correction**: Automatically correct common errors using AI suggestions
- **Sentiment Analysis**: Validate tone and sentiment in text fields for appropriate content
- **Image Validation**: Add support for validating images and embedded content
- **Multi-language Support**: Enhance validation with multilingual capabilities through AI translation
- **Knowledge Graph Integration**: Connect validation to knowledge graphs for semantic validation
- **Reinforcement Learning**: Implement feedback loops to continuously improve validation accuracy
- **Real-time Validation**: Process validation in real-time as data is entered
- **Voice-enabled Reports**: Generate audio summaries of validation issues
- **Large Language Model Integration**: Leverage LLMs for complex text validation and contextual understanding
- **Domain-specific Transfer Learning**: Train models on industry-specific data for better validation

## Future General Enhancements

- **Web Interface**: Add a web dashboard for configuration and monitoring
- **Scheduled Validation**: Implement automatic validation on a schedule
- **Email Notifications**: Send notifications when invalid data is detected
- **Custom Validation Rules**: Provide a UI for creating validation rules without coding
- **Batch Processing**: Support for processing multiple sheets or files
- **Export Reports**: Generate detailed validation reports in various formats
- **Validation Templates**: Pre-configured validation rule sets for common data types
- **Historical Tracking**: Track data quality metrics over time

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Contact

Name - Ankit Pimpalkar - ankitpimpalkar707@gmail.com

Project Link: [https://github.com/yourusername/google-sheet-validator](https://github.com/yourusername/google-sheet-validator)
