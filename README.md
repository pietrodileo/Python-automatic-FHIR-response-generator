# Project Documentation

This project processes FHIR resources from a JSON file and generates a FHIR Bundle.

## Project Structure

add tree


## File Descriptions

- **main.py:** Main script to process FHIR resources and generate a FHIR Bundle.
- **bundle.py:** Contains the implementation of the FHIR Bundle class.
- **genericFHIRresource.py:** Defines the GenericFHIRresource class used as a base class for other resources.
- **organization.py:** Implements Organization, OrganizationL1, and OrganizationL2 classes.
- **messageHeader.py:** Defines the MessageHeader class.
- **specimen.py:** Implements the Specimen class.
- **serviceRequest.py:** Contains the implementation of the ServiceRequest class.
- **task.py:** Implements the Task class.
- **data.json:** Input file containing FHIR resources.
- **censimentoEnti.json:** JSON file with data about laboratories.

## Usage

To run the project, execute `main.py`. Ensure that `data.json` and `censimentoEnti.json` are present in the project folder.

### main.py

This will generate a FHIR Bundle and print it in JSON format.

## Dependencies

The project uses Python and assumes a working knowledge of FHIR resources and their structure.

## License

This project is licensed under the [MIT License](LICENSE).
