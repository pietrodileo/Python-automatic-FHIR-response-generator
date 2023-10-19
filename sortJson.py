import json

def ordina_e_salva_json(input_file):
    """
    Ordina un JSON in ordine alfabetico per chiavi e salva il risultato in un nuovo file JSON.

    Args:
    - input_file (str): Il percorso del file JSON da ordinare.

    Returns:
    - str: Il percorso del nuovo file JSON ordinato.
    """
    with open(input_file, 'r') as f:
        json_data = json.load(f)

    json_ordinato = {k: v for k, v in sorted(json_data.items())}

    output_file = input_file.replace('.json', '_sorted.json')
    
    with open(output_file, 'w') as f:
        json.dump(json_ordinato, f, indent=4)

    return output_file

# Esempio di utilizzo:
input_file_path = 'test3.json'
input_file_path2 = 'test_input2.json'
nuovo_file_ordinato = ordina_e_salva_json(input_file_path)
print(f'Il nuovo file ordinato è stato salvato in: {nuovo_file_ordinato}')
nuovo_file_ordinato2 = ordina_e_salva_json(input_file_path2)
print(f'Il nuovo file ordinato è stato salvato in: {nuovo_file_ordinato2}')
