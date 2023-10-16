
# **[Python-automatic-FHIR-response-generator](https://github.com/pietrodileo/Python-automatic-FHIR-response-generator)**

## Project Name

**Description:**
This project implements a FHIR (Fast Healthcare Interoperability Resources) API for managing laboratory-related data. It includes modules for creating and processing FHIR resources such as `Bundle`, `FillerLaboratory`, `GenericFHIRresource`, `MessageHeader`, `Organization`, `ServiceRequest`, `Specimen`, `Task`, and other related entities.

## Table of Contents

- [Bundle](#bundle)
- [FillerLaboratory](#fillerlaboratory)
- [GenericFHIRresource](#genericfhirresource)
- [MessageHeader](#messageheader)
- [Organization](#organization)
- [ServiceRequest](#servicerequest)
- [Specimen](#specimen)
- [Task](#task)
- [Requirements](#requirements)
- [Usage](#usage)
- [Endpoints](#endpoints)
- [Testing](#testing)

## Bundle

### `bundle.py`

The `Bundle` class represents a FHIR Bundle, a collection of resources.

## FillerLaboratory

### `fillerLaboratory.py`

The `FillerLaboratory` class contains methods for processing incoming FHIR messages, generating appropriate responses, and managing laboratory-related resources.

## GenericFHIRresource

### `genericFHIRresource.py`

The `GenericFHIRresource` class provides a basic structure for creating FHIR resources.

## MessageHeader

### `messageHeader.py`

The `MessageHeader` class represents a FHIR MessageHeader resource and includes methods for extracting information from the resource.

## Organization

### `organization.py`

The `Organization` class represents a FHIR Organization resource. It includes two subclasses, `OrganizationL1` and `OrganizationL2`, for specific types of organizations.

## ServiceRequest

### `serviceRequest.py`

The `ServiceRequest` class represents a FHIR ServiceRequest resource. It includes methods for updating the resource with a unique identifier.

## Specimen

### `specimen.py`

The `Specimen` class represents a FHIR Specimen resource. It includes methods for updating the resource with labels.

## Task

### `task.py`

The `Task` class represents a FHIR Task resource associated with a linked service request. It includes methods for creating the task with specific parameters.

## Requirements

### `requirements.txt`

The `requirements.txt` file lists the project dependencies. These include Flask, Gunicorn, and other necessary libraries.

## Usage

### `retiResponseAPI.py`

The main application file `retiResponseAPI.py` sets up a Flask web server with endpoints for handling incoming FHIR messages. It utilizes the `FillerLaboratory` class to process requests and generate responses.

### Deploying on Render

1. **Render Framework:**
   * This code is designed to run on the Render framework, a cloud hosting provider used to build web applications.
2. **Accessing the Web App:**
   * The web application deployed via Render can be accessed through an HTTP request at the specific Render endpoint.
3. **Render Setup:**
   * **Name:** `pythonFHIRresponseAPI`
   * **Region:** EU
   * **Repository:** [GitHub Repository](https://github.com/pietrodileo/Python-automatic-FHIR-response-generator)
   * **Branch:** main
   * **Build Command:** `pip install --upgrade pip && pip install -r requirements.txt`
   * **Start Command:** `gunicorn retiResponseAPI:app`
   * **Auto-deploy:** Yes
   * **Environment:**
     * Key: `PYTHON_VERSION`
     * Value: `3.10.4`

**Note:**

* Ensure that the Render environment is set up according to the provided configuration.
* Access the deployed web application through the Render endpoint after deployment.

## Endpoints

- **GET `/`**
  - Returns a simple greeting message for a GET request.
- POST `/`
  - Returns a simple greeting message for a POST and also the body of the request.
- **POST `/SendNewRequestToES`**
  - Handles new FHIR requests, processes them using the `FillerLaboratory`, and returns an appropriate response.
- **POST `/ERreceivesForward`**
  - Handles FHIR requests related to forwarding, processes them using the `FillerLaboratory`, and returns a positive acknowledgment.

## Testing

### `test_local.py`

The `test_local.py` script is used for testing the local processing logic of the `FillerLaboratory`. It loads sample data from `test_input.json`, processes it, and saves the result as `test_output.json`. Adjust the input file and review the output for testing purposes.

**Instructions:**

1. Modify `test_input.json` with your desired sample data.
2. Run the script: `python test_local.py`.
3. Review the generated `test_output.json` file for the processed result.

Feel free to enhance this README with additional sections such as Installation, Configuration, or any other information relevant to users or contributors.
