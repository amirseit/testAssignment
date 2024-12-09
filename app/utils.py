from email_validator import validate_email, EmailNotValidError
import re

def detect_field_type(value: str) -> str:
    """Detect the type of a field based on its value."""
    # Strict regex for phone number in the format: +7 xxx xxx xx xx
    value = value.strip()  # Remove leading/trailing spaces
    if re.match(r"^\+7 \d{3} \d{3} \d{2} \d{2}$", value):
        return "phone"
    elif re.match(r"^\d{4}-\d{2}-\d{2}$", value) or re.match(r"^\d{2}\.\d{2}\.\d{4}$", value):
        return "date"
    try:
        # Validate email using email-validator
        validate_email(value, check_deliverability=False)
        return "email"
    except EmailNotValidError:
        pass

    # Explicitly check for text type (non-empty string)
    if isinstance(value, str) and value.strip():
        return "text"
    return "invalid"

def validate_form_data(template_fields, form_data):
    """Validate incoming form data against a template."""
    for field_name, field_type in template_fields.items():
        if field_name not in form_data:
            raise ValueError(f"Missing field: {field_name}")
        
        detected_type = detect_field_type(form_data[field_name])
        
        if detected_type == "invalid":
            raise ValueError(f"Field '{field_name}' has an invalid value.")
        if detected_type != field_type:
            raise ValueError(
                f"Field '{field_name}' is of type '{detected_type}', expected '{field_type}'"
            )