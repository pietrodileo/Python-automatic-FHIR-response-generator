# this code is to test how to remove all the references to a list of FHIR resources

import json

def find_reference_paths(entry, path=[], reference_info=[]):
    if isinstance(entry, dict):
        for key, value in entry.items():
            if key == "reference" and isinstance(value, str):
                reference_info.append({"path": path + [key], "value": value})
            elif isinstance(value, dict):
                find_reference_paths(value, path + [key], reference_info)
            elif isinstance(value, list):
                for i, item in enumerate(value):
                    find_reference_paths(item, path + [key, i], reference_info)
    elif isinstance(entry, list):
        for i, item in enumerate(entry):
            find_reference_paths(item, path + [i], reference_info)
    return reference_info

def remove_value_at_path(data, path):
    """
    Remove the value at the specified path in the JSON-like data structure.

    Args:
    - data: JSON-like data structure (dict, list)
    - path: List representing the path to the value to be removed

    Returns:
    - None
    """
    # Traverse the data structure using the path
    current = data
    for key_or_index in path[:-1]:
        if isinstance(current, dict):
            current = current.get(key_or_index, {})
        elif isinstance(current, list):
            try:
                current = current[key_or_index]
            except IndexError:
                # Handle index out of range
                return None

    # Remove the value at the last key/index in the path
    last_key = path[-1]
    if isinstance(current, dict):
        value = current.pop(last_key, None)
    elif isinstance(current, list):
        try:
            value = current.pop(last_key)
        except IndexError:
            # Handle index out of range
            return None

    # Remove empty objects if current is now empty
    if not current:
        last_key_parent = path.pop()
        parent = data
        for key_or_index in path[:-1]:
            if isinstance(parent, dict):
                parent = parent.get(key_or_index, {})
            elif isinstance(parent, list):
                try:
                    parent = parent[key_or_index]
                except IndexError:
                    # Handle index out of range
                    return value  # Return the removed value if the path is invalid
        # check if the parent property is empty
        if not parent[path[-1]]: 
            parent.pop(path[-1])

# Define a function to get the value at the specified path in the data structure
def get_value_at_path(data, segments):
    current = data
    try:
        # Traverse each segment in the path
        for segment in segments:
            # If the current segment is an integer, treat it as an index for a list
            if isinstance(segment, int):
                current = current[segment]
            # If the current segment is a string, treat it as a key for a dictionary
            elif isinstance(segment, str):
                current = current.get(segment)
            # If the current segment is not an integer or string, return None (invalid path)
            else:
                return None
    except (KeyError, IndexError, TypeError):
        # Handle exceptions if the path is invalid or the structure does not match the path
        return None
    return current

# Define the function to remove filtered paths from JSON data
def remove_element_at_paths(json_data, ref_paths):
    # Make a copy of the original data
    filtered_data = json_data.copy()
    # Iterate through reference paths
    for path_info in ref_paths:
        # Get the path
        if isinstance(path_info, dict):
            path = path_info['path']
        elif isinstance(path_info, list):
            path = path_info
        # Get the value at the path
        #value = get_value_at_path(json_data, path)
        # Remove the value from filtered data
        remove_value_at_path(filtered_data, path)
        # Get the value at the path
        #value = get_value_at_path(json_data, path)

    return filtered_data

def find_paths_with_single_property(filtered_data, property_name):
    """
    Find paths of objects in the filtered data that have only a single property with the specified name.

    Args:
    - filtered_data: JSON-like filtered data structure (dict, list)
    - property_name: Name of the property to search for

    Returns:
    - List of paths to objects with a single property with the specified name
    """
    paths = []

    def traverse(obj, current_path):
        if isinstance(obj, dict):
            # Check if the object has only one property
            if len(obj) == 1 and property_name in obj:
                paths.append(current_path[:])
            else:
                # Traverse each property
                for key, value in obj.items():
                    traverse(value, current_path + [key])
        elif isinstance(obj, list):
            # Traverse each element of the list
            for i, item in enumerate(obj):
                traverse(item, current_path + [i])

    traverse(filtered_data, [])

    return paths

if __name__ == "__main__":
    # Load JSON data from the file
    with open('test_input.json', 'r') as file:
        data = json.load(file)

    full_url_to_remove = []
    idx_to_remove = []

    # Define a list of the resources that should be skipped 
    resource_to_skip = ["Binary","Condition","AllergyIntolerance","RelatedPerson","Observation","Practitioner","Specimen"]
    for idx, entry in enumerate(data['entry']):
        resource = entry['resource']
        full_url = entry['fullUrl']
        resource_type = resource['resourceType']
        
        # Process different resource types
        if resource_type in resource_to_skip:
            # remove the reference to this resource from each part of the dictionary
            idx_to_remove.append(idx)
            full_url_to_remove.append(full_url)

    # find all reference paths contained in the message
    ref_paths = find_reference_paths(data)
    # Filter the reference paths
    filtered_ref_paths = [item for item in ref_paths if any(resource == item['value'].split('/')[0] for resource in resource_to_skip)]

    # Remove filtered paths from the JSON data
    filtered_data = remove_element_at_paths(data, filtered_ref_paths)
    # define a list of the single properties that has been left after cleaning the references to be removed
    sp_list = ["url","display","system","rank"]
    sp_paths = []
    for prop_name in sp_list:
        sp_paths.append(find_paths_with_single_property(filtered_data,prop_name))
    # flatten sp_paths, which is a list of lists
    sp_paths_flat = [path for sublist in sp_paths for path in sublist]
    # Remove element at sp_paths_flat paths from the JSON data
    filtered_data = remove_element_at_paths(filtered_data, sp_paths_flat)

    # Remove the elements at the specified indices
    # Using reverse ensures that we start removing elements from the end of the list to avoid index shifting issues
    for idx in sorted(idx_to_remove, reverse=True): 
        del data['entry'][idx]

    # Save the processed result as prettified JSON
    output_file = 'test_remove_output.json'
    with open(output_file, 'w', encoding='utf-8') as output_file:
        json.dump(data, output_file, ensure_ascii=False, indent=4)

    # Print a message indicating the file where the result is saved
    print(f'Result saved to {output_file}')