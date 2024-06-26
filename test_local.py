import json
from fillerLaboratory import FillerLaboratory
from placerLaboratory import PlacerLaboratory 

# Create an instance of FillerLaboratory
filler_lab = FillerLaboratory()
placer_lab = PlacerLaboratory()

# Load JSON data from the file
with open('test_input.json', 'r') as file:
    request_data = json.load(file)

# Process the data using the logic from FillerLaboratory
result = placer_lab.placerManageResultsAndReports(request_data)

# Save the processed result as prettified JSON
output_file = 'test_output.json'
with open(output_file, 'w', encoding='utf-8') as output_file:
    json.dump(result, output_file, ensure_ascii=False, indent=4)

# Print a message indicating the file where the result is saved
print(f'Result saved to {output_file}')
