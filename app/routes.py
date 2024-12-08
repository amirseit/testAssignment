from flask import Flask, request, jsonify
from app.database import get_templates
from app.utils import detect_field_type, validate_form_data

app = Flask(__name__)

@app.route("/get_form", methods=["POST"])
def get_form():
    form_data = request.form.to_dict()
    templates = get_templates()

    for template in templates:
        try:
            validate_form_data(template["fields"], form_data)
            return jsonify({"template_name": template["name"]})
        except ValueError:
            continue

    # If no match, return detected field types
    detected_types = {key: detect_field_type(value) for key, value in form_data.items()}
    return jsonify(detected_types), 400
