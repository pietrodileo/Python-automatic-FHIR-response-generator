from flask import Flask, request, jsonify
from fillerLaboratory import FillerLaboratory

# Create a new Flask application
app = Flask(__name__)
app.config['JSON_SORT_KEYS'] = False

# Create an instance of FillerLaboratory
filler_lab = FillerLaboratory()

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

@app.route('/', methods=['GET','POST'])
# '/' URL is bound with hello_world() function
def hello_world():
    if request.method == 'GET':
        # Handle GET request
        response = {
            "property1": "Hello from Flask!",
            "property2": "This is a GET request."
        }
    elif request.method == 'POST':
        # Handle POST request
        data = request.json
        response = {
            "property1": "Hello from Flask!",
            "property2": "If you're seeing this message, the application is running correctly",
            "received_data": data
        }
    else:
        response = {"error": "Invalid request method"}

    return jsonify(response)

@app.route('/SendNewRequestToES', methods=['POST'])
def handle_new_request():
    request_data = request.json
    return process_request(request_data, filler_lab.fillerLabAcceptsAllRequest)

@app.route('/ERreceivesForward', methods=['POST'])
def handle_forward_request():
    request_data = request.json
    return process_request(request_data, filler_lab.fillerSendsPositiveACK)

#main driver function
if __name__ == '__main__':
    # run() method of Flask class runs the application 
    # on the local development server
    app.run()
