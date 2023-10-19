import json

def indent_json_from_path(input_file_path, output_file_path, indent=4):
    """
    Indent a JSON file with the specified number of spaces and save the result to a new file.

    Args:
    - input_file_path (str): Path to the input JSON file.
    - output_file_path (str): Path to the output file for the indented JSON.
    - indent (int, optional): Number of spaces for indentation. Default is 4.
    """
    try:
        with open(input_file_path, 'r') as input_file:
            json_data = json.load(input_file)

        indented_json = json.dumps(json_data, indent=indent)

        with open(output_file_path, 'w') as output_file:
            output_file.write(indented_json)

        print(f"Indented JSON saved to: {output_file_path}")

    except Exception as e:
        print(f"Error: {e}")

# Example usage:
input_file_path = 'test3.json'
output_file_path = 'test3_indented.json'

indent_json_from_path(input_file_path, output_file_path)
