import pytest
from app.routes import app  # Assuming your Flask app is named `app` in app.py

# Setup a Flask test client
@pytest.fixture
def client():
    app.config["TESTING"] = True
    with app.test_client() as client:
        yield client


# Test cases
@pytest.mark.parametrize(
    "input_data, expected_status, expected_response",
    [
        # Valid full match
        (
            {
                "user_email": "test@example.com",
                "user_phone": "+7 123 456 78 90",
                "user_dob": "1990-01-01",
                "user_name": "randomUsername",
            },
            200,
            {"template_name": "User Registration Form"},
        ),
        # Missing field
        (
            {
                "user_email": "test@example.com",
                "user_phone": "+7 123 456 78 90",
                "user_dob": "1990-01-01",
            },
            200,
            {
                "user_email": "email",
                "user_phone": "phone",
                "user_dob": "date",
            },
        ),
        # Duplicate fields
        (
            {
                "user_email": ["test@example.com"],
                "user_phone": ["+7 123 456 78 90", "+7 124 456 78 90"],
            },
            200,
            {
                "error": "Duplicate fields detected",
                "duplicates": {"user_phone": ["+7 123 456 78 90", "+7 124 456 78 90"]},
            },
        ),
    ],
)
def test_get_form(client, input_data, expected_status, expected_response):
    response = client.post("/get_form", data=input_data)
    assert response.status_code == expected_status
    assert response.json == expected_response

