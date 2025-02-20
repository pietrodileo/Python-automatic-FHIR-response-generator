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
global timeout # Declare 'test_timeout' and 'timeout' as global variables
timeout = 15 # default timeout before sending the response back if test_timeout == True

def determine_filler_lab_OMRLabCode(headers: dict) -> str:
    if headers.get('OMRLabCodeDestination') and headers.get('OMRLabCodePlacer'):
        return headers['OMRLabCodeDestination'] if headers['OMRLabCodePlacer'] != headers['OMRLabCodeDestination'] else headers['OMRLabCodePlacer']
    return ""  # Ensure a default value is returned

# Define the Error Handling procedure
def handle_error(error_message, status_code=500):
    response = {"error": error_message}
    return jsonify(response), status_code

# Define a method to process the incoming request with a custom processing function
def process_request(data, test_timeout, processing_function):
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
            time.sleep(timeout)  # Simulate a delay of n seconds
        # generate the response by calling the processing function passed as an argument
        response = processing_function(data)
        status_code = 200
        if response == None:
            status_code = 500
            raise Exception("No response was generated.")
        
        return jsonify(response), status_code

    except Exception as e:
        return handle_error(f"Error processing request: {str(e)}")

def extract_request_data(request):
    """
    Extract data from the incoming request and determine the OMR lab code of the filler lab using the headers.

    Args:
        request: The incoming request.

    Returns:
        The extracted data from the request.
    """
    # Get the raw JSON data from the request
    request_data_raw = request.data.decode('latin-1')

    # Prettify the incoming POST bodies for improved readability and to avoid potential errors
    prettified_data = json.dumps(json.loads(request_data_raw), indent=4)

    # Extract the data from the prettified JSON
    request_data = json.loads(prettified_data)
    
    # Define a list of the HTTP headers to be retrieved
    headers_list = ['OMRLabCodeDestination', 'OMRLabCodePlacer', 'TestTimeout']
    
    headers, request_data = extract_headers(request, request_data, headers_list)

    test_timeout = False
    # Check if a specific header was passed
    if request_data.get('TestTimeout') != None:
        print(f"'TestTimeout': {request_data.get('TestTimeout')}")
        # if the value is 0, the timeout is disabled, otherwise it is enabled if the value is equal to 1
        test_timeout = bool(int(request_data.get('TestTimeout')))
        
    # Determine the OMR lab code of the filler lab by the headers
    OMR_lab_code_filler = determine_filler_lab_OMRLabCode(headers)
    
    # insert the OMR lab code of the filler lab in the request data
    request_data['OMRLabCodeFiller'] = OMR_lab_code_filler
    
    return request_data, test_timeout

def extract_headers(request, request_data, headers_list) -> dict:   
    """
    Extract HTTP headers from the incoming request and add them to the request data.

    Parameters
    ----------
    request : flask.Request
        The incoming request.
    request_data : dict
        The request data to be updated with the extracted headers.
    headers_list : list
        A list of HTTP headers to be extracted.

    Returns
    -------
    A dictionary of the extracted headers and the updated request data.

    Notes
    -----
    If the headers_list is not a list, the function will convert it to a list.
    """
    if type(headers_list) != list:
        headers_list = [headers_list]

    extracted_headers = {key: request.headers.get(key) for key in headers_list}
        
    for key, value in extracted_headers.items():
        request_data[key]=value
    
    return extracted_headers, request_data

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
    """
    Handle a new request sent to ES by processing the incoming data.

    This endpoint listens for POST requests at '/SendNewRequestToES'.
    It extracts the request data and processes it using the FillerLaboratory's
    fillerLabAcceptsAllRequest method to generate a response.

    Returns:
        A JSON response with the processing result and status code.
    """
    return process_request(*extract_request_data(request), filler_lab.fillerLabAcceptsAllRequest)

@app.route('/ESrejectsAllRequests', methods=['POST'])
def handle_new_request_reject_all():
    return process_request(*extract_request_data(request), filler_lab.fillerLabRejectsAllRequest)

@app.route('/ESAcceptsRandomRequests', methods=['POST'])
def handle_new_request_accept_random():
    return process_request(*extract_request_data(request), filler_lab.fillerLabAcceptsRandomRequests)

@app.route('/ERreceivesForward', methods=['POST'])
def handle_forward_request():
    return process_request(*extract_request_data(request), placer_lab.placerSendsPositiveACK)

@app.route('/ESreceivesCancellationReq', methods=['POST'])
def handle_cancellation_request():
    return process_request(*extract_request_data(request), filler_lab.fillerSendsCancellationResponse)

@app.route('/ESreceivesModificationReq', methods=['POST'])
def handle_modification_request():
    return process_request(*extract_request_data(request), filler_lab.fillerSendsModificationResponse)

@app.route('/ERreceivesNotification', methods=['POST'])
def handle_checkIn_notification():
    return process_request(*extract_request_data(request), placer_lab.placerSendsCheckInOutResponse)

@app.route('/ERreceivesResultsOrReport', methods=['POST'])
def handle_results():
    return process_request(*extract_request_data(request), placer_lab.placerManageResultsAndReports)

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
