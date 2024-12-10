import requests
import time

def wait_for_server(url, timeout=15):
    """Wait for the server to become available."""
    for _ in range(timeout):
        try:
            response = requests.get(url)  # Send a GET request to the root endpoint
            if response.status_code:  # Any status code indicates the server is up
                print(f"Server responded with status code: {response.status_code}")
                return True
        except requests.exceptions.RequestException as e:
            print(f"Server not available yet: {e}")
            time.sleep(1)
    raise TimeoutError("Server did not start in time.")


def make_request(input_data, expected_status=None, expected_response=None):
    """Send a POST request to the /get_form endpoint."""
    url = "http://127.0.0.1:5000/get_form"
    response = requests.post(url, data=input_data)
    print(f"Input: {input_data}")
    print(f"Response: {response.status_code} - {response.json()}")

    # If expected values are provided, validate them
    if expected_status is not None:
        assert response.status_code == expected_status, f"Expected {expected_status}, got {response.status_code}"
    if expected_response is not None:
        assert response.json() == expected_response, f"Expected {expected_response}, got {response.json()}"


if __name__ == "__main__":
    print("Waiting for the server to start...")

    try:
        # Wait for the server to start
        wait_for_server("http://127.0.0.1:5000")
        print("Server is running. Starting tests...")

        # Test cases
        test_cases = [
            # Valid full match
            {
                "input_data": {
                    "user_email": "test@example.com",
                    "user_phone": "+7 123 456 78 90",
                    "user_dob": "1990-01-01",
                    "user_name": "randomUsername",
                },
                "expected_status": 200,
                "expected_response": {"template_name": "User Registration Form"},
            },
            # Missing field
            {
                "input_data": {
                    "user_email": "test@example.com",
                    "user_phone": "+7 123 456 78 90",
                    "user_dob": "1990-01-01",
                },
                "expected_status": 200,
                "expected_response": {
                    "user_email": "email",
                    "user_phone": "phone",
                    "user_dob": "date",
                },
            },
            # Duplicate fields
            {
                "input_data": {
                    "user_email": ["test@example.com"],
                    "user_phone": ["+7 123 456 78 90", "+7 124 456 78 90"],
                },
                "expected_status": 200,
                "expected_response": {
                    "error": "Duplicate fields detected",
                    "duplicates": {"user_phone": ["+7 123 456 78 90", "+7 124 456 78 90"]},
                },
            },
            # Additional fields
            {
                "input_data": {
                    "user_email": "test@example.com",
                    "user_phone": "+7 123 456 78 90",
                    "user_dob": "1990-01-01",
                    "user_name": "randomUsername",
                    "extra_field": "extra_value",
                },
                "expected_status": 200,
                "expected_response": {"template_name": "User Registration Form"},
            },
            # Empty input
            {
                "input_data": {},
                "expected_status": 200,
                "expected_response": {},
            },
            # Invalid field values
            {
                "input_data": {
                    "user_email": "not_an_email",
                    "user_phone": "123-456-7890",
                    "user_dob": "not_a_date",
                    "user_name": "",
                },
                "expected_status": 200,
                "expected_response": {
                    "user_email": "text",
                    "user_phone": "text",
                    "user_dob": "text",
                    "user_name": "invalid",
                },
            },
            # Multiple matching templates (matches the first found in the database)
            {
                "input_data": {
                    "user_email": "test@example.com",
                    "user_phone": "+7 123 456 78 90",
                    "user_dob": "1990-01-01",
                    "user_name": "randomUsername",
                    "order_email": "order@example.com",
                    "order_phone": "+7 321 456 78 90",
                    "order_date": "1991-01-01",
                    "order_description": "Some text",
                },
                "expected_status": 200,
                "expected_response": {"template_name": "User Registration Form"},
            },
            # Large input data
            {
                "input_data": {f"field_{i}": f"value_{i}" for i in range(1000)},
                "expected_status": 200,
            },
            # Non-ASCII characters
            {
                "input_data": {
                    "user_email": "тест@example.com",
                    "user_phone": "+7 123 456 78 90",
                    "user_dob": "1990-01-01",
                    "user_name": "имяПользователя",
                },
                "expected_status": 200,
                "expected_response": {"template_name": "User Registration Form"},
            },
        ]

        # Execute the test cases
        for i, case in enumerate(test_cases, start=1):
            print(f"\nRunning test case {i}:")
            make_request(case["input_data"], case.get("expected_status"), case.get("expected_response"))

        # If all tests pass, print success message
        print("\nAll tests passed!")

    except TimeoutError as e:
        print(str(e))
    except AssertionError as e:
        print(f"\nTest failed: {e}")
