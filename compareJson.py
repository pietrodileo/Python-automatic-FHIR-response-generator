from jsondiff import diff
import json

def compare_and_save_differences(file_path1, file_path2, output_file_path):
    """
    Compare two JSON files using jsondiff and save the differences to an output file.

    Args:
    - file_path1 (str): Path to the first JSON file.
    - file_path2 (str): Path to the second JSON file.
    - output_file_path (str): Path to the file where differences will be saved.

    Returns:
    - dict: Differences between the two JSON files.
    """
    with open(file_path1, 'r') as f:
        json_data1 = json.load(f)

    with open(file_path2, 'r') as f:
        json_data2 = json.load(f)

    differences = diff(json_data1, json_data2)

    with open(output_file_path, 'w') as f:
        json.dump(differences, f, indent=4)

    return differences

# Example usage:
input_file_path1 = 'test_input_sorted.json'
input_file_path2 = 'test_input2_sorted.json'
output_file_path = 'differences_output.json'

differences = compare_and_save_differences(input_file_path1, input_file_path2, output_file_path)
print(f'Differences have been saved to: {output_file_path}')
print(differences)
