from flask import Flask, request, jsonify
from fillerLaboratory import FillerLaboratory
from placerLaboratory import PlacerLaboratory 
import json

# Create a new Flask application
app = Flask(__name__)
app.config['JSON_SORT_KEYS'] = False

# Create an instance of FillerLaboratory and PlacerLaboratory
filler_lab = FillerLaboratory()
placer_lab = PlacerLaboratory()

# Define the Error Handling procedure
def handle_error(error_message, status_code=404):
    response = {"error": error_message}
    return jsonify(response), status_code

# Define a method to process the incoming request with a custom processing function
def process_request(data, processing_function):
    try:
        response = processing_function(data)
        status_code = 200
        return jsonify(response), status_code

    except ValueError as ve:
        return handle_error(f"Invalid JSON format: {str(ve)}")

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

@app.route('/ERreceivesForward', methods=['POST'])
def handle_forward_request():
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
    return process_request(request_data, filler_lab.fillerSendsPositiveACK)

@app.route('/ERreceivesNotification', methods=['POST'])
def handle_checkIn_notification():
    # Get the raw JSON data from the request
    request_data_raw = request.data.decode('latin-1')

    # Prettify the incoming POST bodies for improved readability and to avoid potential errors
    prettified_data = json.dumps(json.loads(request_data_raw), indent=4)

    # Extract the data from the prettified JSON
    request_data = json.loads(prettified_data)
    return process_request(request_data, placer_lab.sendsCheckInConfirmation)

#main driver function
if __name__ == '__main__':
    # run() method of Flask class runs the application 
    # on the local development server
    app.run()
