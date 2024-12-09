from flask import Flask, request, jsonify
from app.database import get_templates
from app.utils import detect_field_type, validate_form_data

app = Flask(__name__)

@app.route("/get_form", methods=["POST"])
def get_form():
    form_data = request.form.to_dict()
    print("Form data received:", form_data)  # Debugging

    templates = get_templates()
    for template in templates:
        try:
            validate_form_data(template["fields"], form_data)
            return jsonify({"template_name": template["name"]})
        except ValueError as e:
            print(f"Validation error: {e}")  # Log specific error

    detected_types = {key: detect_field_type(value) for key, value in form_data.items()}
    print("Detected types:", detected_types)  # Debugging
    return jsonify(detected_types), 400
