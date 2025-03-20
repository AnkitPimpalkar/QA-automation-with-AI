import json
import importlib
import logging

def load_validators(config_file):
    """
    Dynamically load validators from configuration.
    Each validator receives its configuration dictionary.
    """
    validators = []
    try:
        with open(config_file, 'r') as f:
            config = json.load(f)
        
        for v_conf in config.get("validators", []):
            validator_type = v_conf.get("validator_type")
            # Assuming module name follows a convention, e.g., "pin" -> "pin_validator"
            module_name = f"src.validators.{validator_type}_validator"
            try:
                module = importlib.import_module(module_name)
                # Pass the entire config for the validator, including column_name and params.
                validator_instance = module.Validator(v_conf)
                validators.append(validator_instance)
            except Exception as e:
                logging.error(f"Error loading validator for type '{validator_type}': {e}")
        
        return validators
    except Exception as e:
        logging.error(f"Failed to load validators: {e}")
        return []
