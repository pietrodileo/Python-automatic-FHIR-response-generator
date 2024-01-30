import requests
import json

# Define the URL to which the request is to be sent
url = 'http://127.0.0.1:5000'

# Load data from 'test_input.json'
with open('test_input.json', 'r') as file:
    data = json.load(file)

# Send POST request
response = requests.post(url, json=data)

# Check the response
if response.status_code == 200:
    print("Request was successful!")
    response_data = response.json()
    print("Response:", response_data)

    # Save the response to a JSON file
    with open('response_output.json', 'w') as output_file:
        json.dump(response_data, output_file, indent=2)
else:
    print("Request failed. Status code:", response.status_code)
    print("Response:", response.text)