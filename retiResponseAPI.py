from flask import Flask, request, jsonify
from fillerLaboratory import FillerLaboratory
from placerLaboratory import PlacerLaboratory 
import json
import time

# Create a new Flask application
app = Flask(__name__)
app.config['JSON_SORT_KEYS'] = False

# Create an instance of FillerLaboratory and PlacerLaboratory
filler_lab = FillerLaboratory()
placer_lab = PlacerLaboratory()

# Define a parameter to test the timeout
test_timeout = False  # Set to True to enable timeout
timeout = 15

# Define the Error Handling procedure
def handle_error(error_message, status_code=404):
    response = {"error": error_message}
    return jsonify(response), status_code

# Define a method to process the incoming request with a custom processing function
def process_request(data, processing_function):
    """
    Process a request by calling the specified processing function.

    Args:
        data: The data to be processed.
        processing_function: The function to be called for processing the data.

    Returns:
        A tuple containing the response and status code.

    Raises:
        ValueError: If the JSON format is invalid.
        Exception: If an error occurs during processing.
    """
    try:
        response = None
        if test_timeout:  # If timeout testing is enabled
            time.sleep(timeout)  # Simulate a delay of 20 seconds
            
        response = processing_function(data)
        status_code = 200
        if response == None:
            status_code = 404
            raise Exception("No response was generated.")
        
        return jsonify(response), status_code

    except Exception as e:
        return handle_error(f"Error processing request: {str(e)}")

@app.route('/', methods=['GET', 'POST'])
def hello_world():
    try:
        if request.method == 'GET':
            # Handle GET request
            response = {
                "property1": "Hello from Flask!",
                "property2": "This is a GET request",
                "property3": "If you're seeing this message, the application is running correctly."
            }
            return jsonify(response)
        elif request.method == 'POST':
            # Get the raw JSON data from the request
            request_data_raw = request.data.decode('latin-1')

            # Prettify the incoming POST bodies for improved readability and to avoid potential errors
            prettified_data = json.dumps(json.loads(request_data_raw), indent=4)

            # Extract the data from the prettified JSON
            request_data = json.loads(prettified_data)
            # Handle POST request
            #data = request.json
            response = {
                "property1": "Hello from Flask!",
                "property2": "This is a POST request",
                "property3": "If you're seeing this message, the application is running correctly",
                **request_data  # Using the unpacking operator
            }
            return jsonify(response)
        else:
            # Handle unsupported methods
            return handle_error("Method not allowed. Only GET and POST are supported.", 405) 

    except ValueError as ve:
        return handle_error(f"Invalid JSON format: {str(ve)}", 400)

    except Exception as e:
        return handle_error(f"Error processing request: {str(e)}", 500)

@app.route('/SendNewRequestToES', methods=['POST'])
def handle_new_request_accept():
    # Get the raw JSON data from the request
    request_data_raw = request.data.decode('latin-1')

    # Prettify the incoming POST bodies for improved readability and to avoid potential errors
    prettified_data = json.dumps(json.loads(request_data_raw), indent=4)

    # Extract the data from the prettified JSON
    request_data = json.loads(prettified_data)
    return process_request(request_data, filler_lab.fillerLabAcceptsAllRequest)

@app.route('/ESrejectsAllRequests', methods=['POST'])
def handle_new_request_reject_all():
    # Get the raw JSON data from the request
    request_data_raw = request.data.decode('latin-1')

    # Prettify the incoming POST bodies for improved readability and to avoid potential errors
    prettified_data = json.dumps(json.loads(request_data_raw), indent=4)

    # Extract the data from the prettified JSON
    request_data = json.loads(prettified_data)
    return process_request(request_data, filler_lab.fillerLabRejectsAllRequest)

@app.route('/ESAcceptsRandomRequests', methods=['POST'])
def handle_new_request_accept_random():
    # Get the raw JSON data from the request
    request_data_raw = request.data.decode('latin-1')

    # Prettify the incoming POST bodies for improved readability and to avoid potential errors
    prettified_data = json.dumps(json.loads(request_data_raw), indent=4)

    # Extract the data from the prettified JSON
    request_data = json.loads(prettified_data)
    return process_request(request_data, filler_lab.fillerLabAcceptsRandomRequests)

@app.route('/ERreceivesForward', methods=['POST'])
def handle_forward_request():

    # Retrieve HTTP headers
    headers = request.headers
    
    # Check if a specific header was passed
    if 'TestTimeout' in headers:
        header_value = headers.get('TestTimeout')
        print(f"TestTimeout': {header_value}")
        global test_timeout  # Declare 'test_timeout' as a global variable
        test_timeout = False  # Modify the global variable
    else:
        print("The 'TestTimeout' header was not passed in the request.")

    # Get the raw JSON data from the request
    request_data_raw = request.data.decode('latin-1')

    # Prettify the incoming POST bodies for improved readability and to avoid potential errors
    prettified_data = json.dumps(json.loads(request_data_raw), indent=4)

    # Extract the data from the prettified JSON
    request_data = json.loads(prettified_data)
    return process_request(request_data, placer_lab.placerSendsPositiveACK)

@app.route('/ESreceivesCancellationReq', methods=['POST'])
def handle_cancellation_request():
    # Get the raw JSON data from the request
    request_data_raw = request.data.decode('latin-1')

    # Prettify the incoming POST bodies for improved readability and to avoid potential errors
    prettified_data = json.dumps(json.loads(request_data_raw), indent=4)

    # Extract the data from the prettified JSON
    request_data = json.loads(prettified_data)
    return process_request(request_data, filler_lab.fillerSendsCancellationResponse)

@app.route('/ESreceivesModificationReq', methods=['POST'])
def handle_modification_request():
    # Get the raw JSON data from the request
    request_data_raw = request.data.decode('latin-1')

    # Prettify the incoming POST bodies for improved readability and to avoid potential errors
    prettified_data = json.dumps(json.loads(request_data_raw), indent=4)

    # Extract the data from the prettified JSON
    request_data = json.loads(prettified_data)
    return process_request(request_data, filler_lab.fillerSendsModificationResponse)

@app.route('/ERreceivesNotification', methods=['POST'])
def handle_checkIn_notification():
    # Get the raw JSON data from the request
    request_data_raw = request.data.decode('latin-1')

    # Prettify the incoming POST bodies for improved readability and to avoid potential errors
    prettified_data = json.dumps(json.loads(request_data_raw), indent=4)

    # Extract the data from the prettified JSON
    request_data = json.loads(prettified_data)
    return process_request(request_data, placer_lab.placerSendsCheckInOutResponse)

@app.route('/ERreceivesResultsOrReport', methods=['POST'])
def handle_results():
    # Get the raw JSON data from the request
    request_data_raw = request.data.decode('latin-1')

    # Prettify the incoming POST bodies for improved readability and to avoid potential errors
    prettified_data = json.dumps(json.loads(request_data_raw), indent=4)

    # Extract the data from the prettified JSON
    request_data = json.loads(prettified_data)
    return process_request(request_data, placer_lab.placerManageResultsAndReports)

@app.route('/generateError', methods=['POST'])
def generate_error():
    # Return an HTTP error
    response = {
        "property1": "Hello from Flask!",
        "property2": "If you're seeing this message, the application is running correctly.",
        "property3": "An error was returned by purpose in order to test how this response is processed."
    }
    status_code = 500
    return jsonify(response), status_code

#main driver function
if __name__ == '__main__':
    # run() method of Flask class runs the application 
    # on the local development server
    app.run()
