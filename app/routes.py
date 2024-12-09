from flask import Flask, request, jsonify
from app.database import get_templates
from app.utils import detect_field_type

app = Flask(__name__)

@app.route("/get_form", methods=["POST"])
def get_form():
    form_data = request.form.to_dict(flat=False)  # Collect all values for each key
    print("Form data received:", form_data)  # Debugging

    # Check for duplicate keys
    duplicates = {key: values for key, values in form_data.items() if len(values) > 1}
    if duplicates:
        return jsonify({
            "error": "Duplicate fields detected",
            "duplicates": duplicates
        }), 200

    # Flatten the form data to use only single values
    form_data = {key: values[0] if isinstance(values, list) else values for key, values in form_data.items()}

    # Fetch all templates from the database
    templates = get_templates()

    for template in templates:
        template_fields = template["fields"]
        # Check if all required fields are present and types match
        if all(
            field in form_data and detect_field_type(form_data[field]) == expected_type
            for field, expected_type in template_fields.items()
        ):
            return jsonify({"template_name": template["name"]}), 200

    # If no match is found, return detected field types
    detected_types = {key: detect_field_type(value) for key, value in form_data.items()}
    return jsonify(detected_types), 200